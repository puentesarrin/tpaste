# -*- coding: utf-8 *-*
from wtforms import Form, TextField, PasswordField, TextAreaField, SelectField
from wtforms.validators import Required, Email, EqualTo
from tpaste import messages


class RegistrationForm(Form):

    username_reg = TextField(u"Username",
        [Required(message=u"Username is missing.")])
    email_reg = TextField(u"Email",
        [Required(message=u"Email is missing."),
            Email(message=u"Email is not valid.")])
    password_reg = PasswordField(u"Password",
        [Required(message=u"Password is missing.")])
    password_match = PasswordField(u"Confirm password",
        [Required(message=u"Password missing."),
        EqualTo('password_reg', message="Passwords doesn't match.")])


class NewSnippetForm(Form):

    title = TextField(u"Title", [Required(message=u"Title is missing.")])
    author = TextField(u"Author", [])
    content = TextAreaField(u"Content",
        [Required(message=u"Content is missing.")])
    syntax = SelectField(u"Syntax",
        [Required(message=u"Syntax is missing.")])

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        if "lang" in kwargs:
            kwargs.setdefault("syntax", kwargs["lang"])
        Form.__init__(self, formdata, obj, prefix, **kwargs)
        self.syntax.choices = list(messages.languages.items())


class SearchSnippetForm(Form):

    term = TextField(u"Term", [Required(message=u"Term is missing.")])
