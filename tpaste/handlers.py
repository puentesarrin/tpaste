# -*- coding: utf-8 *-*
import re
import motor
import bcrypt
import datetime
import traceback
import tornado.gen
import tornado.web
import simplejson as json
from bson import json_util
from tpaste import messages, forms
from tpaste.helpers import stringhelper, mailhelper


class BaseMultiDict(object):

    def __init__(self, handler):
        self.handler = handler

    def __iter__(self):
        return iter(self.handler.request.arguments)

    def __len__(self):
        return len(self.handler.request.arguments)

    def __contains__(self, name):
        return (name in self.handler.request.arguments)

    def getlist(self, name):
        return self.handler.get_arguments(name, strip=False)


class TPasteHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    @property
    def smtp(self):
        return self.application.smtp

    def __init__(self, *args, **kwargs):
        super(TPasteHandler, self).__init__(*args, **kwargs)

    def get_dict_arguments(self):
        return BaseMultiDict(self)

    def write_error(self, status_code, **kwargs):
        params = {}
        if self.settings.get('debug') and 'exc_info' in kwargs:
            params['stack_trace'] = ''.join([line for line in
                traceback.format_exception(*kwargs['exc_info'])])
        if status_code in messages.errors.keys():
            self.render('error.html', message=messages.errors[status_code],
                **params)
        else:
            self.write('Error no manejado. ' + str(self._status_code))

    def write_json(self, content):
        self.write(json.dumps(content, default=json_util.default))

    def write_ajax_response(self, message, action="content"):
        self.write_json({"action": action, "message": message})

    def write_ajax_redirect(self, url):
        self.write_ajax_response(url, action="redirect")

    def write_ajax_error(self, error):
        self.write_ajax_response(error, action="error")


class NotFoundHandler(TPasteHandler):

    def get(self):
        raise tornado.web.HTTPError(404)


class HomeHandler(TPasteHandler):

    def get(self):
        lang = self.get_argument('lang', None)
        if lang not in messages.languages.keys() + [None]:
            raise tornado.web.HTTPError(404)
        self.render('home.html', lang=lang)


class SupportedLanguagesHandler(TPasteHandler):

    def get(self):
        self.render("languages.html", languages=messages.languages)


class LanguageHandler(TPasteHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, language):
        language = language.replace(' ', '+')
        if language not in messages.languages:
            raise tornado.web.HTTPError(404,
                '%s is a unsupported language.' % language)
        cursor = self.db.snippets.find({'syntax': language},
            sort=[('date', -1)], limit=20)
        snippets = yield motor.Op(cursor.to_list)
        self.render('language.html', snippets=snippets, lang_code=language,
            lang_name=messages.languages[language])


class NewSnippetHandler(TPasteHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        form = forms.NewSnippetForm(self.get_dict_arguments())
        if not form.validate():
            self.write(form.errors)
            self.finish()
        else:
            while True:
                token = stringhelper.random_base62()
                s = yield motor.Op(self.db.snippets.find_one, {'token': token},
                    fields={'_id': 1})
                if not s:
                    break
            snippet = {'title': self.get_argument('title'),
                'syntax': self.get_argument('syntax'),
                'content': self.get_argument('content'),
                'token': token,
                'date': datetime.datetime.now()}
            if self.current_user:
                snippet['author'] = self.current_user['']
            else:
                snippet['author'] = self.get_argument('author')
            yield motor.Op(self.db.snippets.insert, snippet)
            self.redirect('/%s' % token)


class SnippetHandler(TPasteHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, token=None):
        if token:
            snippet = yield motor.Op(self.db.snippets.find_one,
                {'token': token})
        else:
            snippet = yield motor.Op(self.db.snippets.find_one, {},
                sort=[('date', -1)])
        if not 'html' in snippet:
            from pygments import highlight
            from pygments.lexers import get_lexer_by_name
            from pygments.formatters import HtmlFormatter
            lexer = get_lexer_by_name(snippet['syntax'], stripall=True)
            formatter = HtmlFormatter(linenos=True, cssclass='source')
            snippet['html'] = highlight(snippet['content'], lexer, formatter)
            yield motor.Op(self.db.snippets.save, snippet)
        self.render('snippet.html', snippet=snippet)


class RawSnippetHandler(TPasteHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, token):
        snippet = yield motor.Op(self.db.snippets.find_one, {'token': token})
        if not snippet:
            raise tornado.web.HTTPError(404)
        else:
            self.set_header('Content-Type', 'text/plain')
            self.write(snippet['content'])
            self.finish()


class SearchSnippetHandler(TPasteHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        term = self.get_argument('term', '')
        if not term:
            self.render('search.html', snippets=[])
            self.finish()
        regex = re.compile('.*' + term + '.*', re.IGNORECASE)
        cursor = self.db.snippets.find({'title': regex}, sort=[('title', 1)])
        snippets = yield motor.Op(cursor.to_list)
        self.render('search.html', snippets=snippets)


class RegistrationHandler(TPasteHandler):

    def get(self):
        if self.current_user:
            self.redirect('/')
        self.render('registration.html')

    @tornado.web.asynchronous
    @tornado.gen.engine
    def post(self):
        if self.current_user:
            self.redirect('/')
        form = forms.RegistrationForm(self.get_dict_arguments())
        if form.validate():
            user = {
                'username': self.get_argument('username_reg'),
                'email': self.get_argument('email_reg'),
                'password': self.get_argument('password_reg'),
                'status': 'registered',
                'join': {
                    'date': datetime.datetime.now(),
                    'token': stringhelper.generate_md5()
                    },
                "recover": {}
                }
            u = yield motor.Op(self.db.users.find_one,
                {'$or': [{'username': user['username']},
                    {'email': user['email']}]}, fields={'_id': 1})
            if u:
                self.write_ajax_error(
                    {'email_reg': [messages.registered_email]})
                self.finish()
            else:
                user['password'] = bcrypt.hashpw(user['password'],
                    bcrypt.gensalt())
                message = mailhelper.BaseEmailMessage(user['email'],
                    messages.confirm_registration,
                    'registration.html',
                    connection=self.smtp,
                    user=user
                )
                yield tornado.gen.Task(message.send)
                yield motor.Op(self.db.users.insert, user)
                self.render("showmessage.html",
                    message=messages.confirmregistration)
        else:
            self.write_ajax_error(form.errors)
            self.finish()


class RegistrationSuccessfullyHandler(TPasteHandler):

    def get(self):
        if self.current_user:
            self.redirect('/')
        self.render('showmessage.html',
            message=messages.registrationsuccessfully)


class LoginHandler(TPasteHandler):

    def get(self):
        if self.current_user:
            self.redirect('/')
        self.render('login.html', email=None, message=None,
            _next=self.get_argument('next', '/'))

    @tornado.web.asynchronous
    def post(self):
        pass


class LogoutHandler(TPasteHandler):

    def get(self):
        self.redirect('/')

    def post(self):
        if self.current_user:
            self.clear_cookie('current_user')
        self.redirect('/')


class RecoverPasswordHandler(TPasteHandler):

    def get(self):
        if not self.current_user:
            self.render('recoverpassword.html')
        else:
            self.redirect('/')

    def post(self):
        pass
