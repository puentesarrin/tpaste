# -*- coding: utf-8 *-*
import os
import motor
import tornado.web

from tornado.options import options
from tornado.template import Loader
from tpaste import routes, ui_modules, helpers


class TPasteApplication(tornado.web.Application):

    def __init__(self):
        settings = {
            'static_path': os.path.join(options.theme_path, 'static'),
            'template_path': os.path.join(options.theme_path, 'templates'),
            "ui_modules": ui_modules,
            "cookie_secret": options.cookie_secret,
            "login_url": "/login",
            "xsrf_cookies": True,
            'debug': options.debug
            }
        if options.static_url_prefix:
            settings['static_url_prefix'] = options.static_url_prefix
        urls = routes.urls + \
            [(r"/(favicon\.ico)", tornado.web.StaticFileHandler,
                 {"path":settings['static_path']})]
        self._con = motor.MotorClient(options.db_uri)
        self._db = self._con.open_sync()[options.db_name]
        tornado.web.Application.__init__(self, urls, **settings)

    @property
    def db(self):
        return self._db

    @property
    def template_loader(self):
        if not hasattr(self, "_template_loader"):
            self._template_loader = Loader(os.path.join(options.theme_path,
                "messages"))
        return self._template_loader

    @property
    def smtp(self):
        if not hasattr(self, "_smtp"):
            self._smtp = helpers.mailhelper.BaseEmailBackend(
                host=options.smtp_host,
                port=options.smtp_port,
                username=options.smtp_username,
                password=options.smtp_password,
                use_tls=options.smtp_use_tls,
                template_loader=self.template_loader,
                url=options.base_url
            )
        return self._smtp
