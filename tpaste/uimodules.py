# -*- coding: utf-8 *-*
import tornado.web
from tpaste import forms


class PoweredByModule(tornado.web.UIModule):

    def render(self):
        return self.render_string('modules/poweredby.html')


class RegistrationModule(tornado.web.UIModule):

    def render(self):
        return self.render_string("modules/registration.html",
            form=forms.RegistrationForm())


class LoginModule(tornado.web.UIModule):

    def render(self, email=None, message=None, next_page="/"):
        return self.render_string("modules/login.html",
            email=email,
            message=message,
            next_page=next_page)


class UserMenuModule(tornado.web.UIModule):

    def render(self):
        return self.render_string("modules/usermenu.html")


class RecoverPasswordModule(tornado.web.UIModule):

    def render(self):
        return self.render_string("modules/recoverpassword.html")


class ResetPasswordModule(tornado.web.UIModule):
    def render(self, email="", token=""):
        return self.render_string("modules/resetpassword.html",
            email=email,
            token=token)


class MenuModule(tornado.web.UIModule):

    def render(self):
        return self.render_string("modules/menu.html")


class SnippetModule(tornado.web.UIModule):

    def render(self, snippet=None):
        return self.render_string("modules/snippet.html", snippet=snippet)


class NewSnippetModule(tornado.web.UIModule):

    def render(self, lang=None):
        return self.render_string("modules/newsnippet.html",
            form=forms.NewSnippetForm(lang=lang))


class SearchSnippetModule(tornado.web.UIModule):

    def render(self):
        return self.render_string("modules/searchsnippet.html",
            form=forms.SearchSnippetForm())


class ListSnippetsModule(tornado.web.UIModule):

    def render(self, snippets=[]):
        return self.render_string('modules/listsnippets.html',
            snippets=snippets)


class GoogleAnalyticsModule(tornado.web.UIModule):

    def render(self):
        return self.render_string("modules/googleanalytics.html")
