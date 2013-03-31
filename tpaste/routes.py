# -*- coding: utf-8 *-*
from tpaste import handlers

urls = [
    (r"/", handlers.HomeHandler),
    (r"/new", handlers.NewSnippetHandler),
    (r"/languages", handlers.SupportedLanguagesHandler),
    (r"/register", handlers.RegistrationHandler),
    (r"/registersucessfully", handlers.RegistrationSuccessfullyHandler),
    (r"/login", handlers.LoginHandler),
    (r"/recoverpassword", handlers.RecoverPasswordHandler),
    (r"/logout", handlers.LogoutHandler),
    (r"/search", handlers.SearchSnippetHandler),
    (r"/last", handlers.SnippetHandler),
    (r"/raw/(?P<token>[a-zA-Z0-9]+)", handlers.RawSnippetHandler),
    (r"/lang/(?P<language>[a-z0-9-+]+)", handlers.LanguageHandler),
    (r"/(?P<token>[a-zA-Z0-9]+)", handlers.SnippetHandler),
    (r"/.*", handlers.NotFoundHandler)]
