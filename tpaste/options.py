# -*- coding: utf-8 *-*
import os
import base64

from tornado import options


def get_options():
    #Application
    options.define("configfilename", default="tpaste.conf", type=str,
        help="Configuration filename")
    options.define('debug', default=True, type=bool,
        help="Turn on autoreload, log to stderr only")
    options.define("port", default=8888, type=int, help="Tornado server port")
    options.define('cookie_secret', default=base64.b64encode(os.urandom(32)),
        type=str, help="Secret seed for cookies")
    options.define('static_url_prefix', default=None, type=str,
        help="Useful for serve static files from separate server.")
    options.define("theme_path", default="theme", type=str,
        help="Theme path with static files and templates")
    options.define("googleanalytics_enabled", default=True, type=bool,
        help="Enable Google Analytics module")
    options.define("googleanalytics_trackercode", default="", type=str,
        help="Set Google Analytics tracker code")
    options.define('base_url', default="http://localhost", type=str,
        help="Base url host")
    options.define('slogan', default="Web application for saving and sharing "
        "text snippets. Using Tornado, MongoDB and Motor.", type=str,
        help="Slogan")

    #MongoDB
    options.define('db_uri', default='mongodb://localhost:27017/?safe=true',
        type=str, help='MongoDB database uri')
    options.define('db_name', default='tpaste', type=str,
        help='MongoDB database name')

    #SMTP
    options.define('smtp_host', default="smtp.gmail.com", type=str,
        help="SMTP server host")
    options.define('smtp_port', default=587, type=int,
        help="SMTP server port")
    options.define('smtp_use_tls', default=True, type=bool,
        help="SMTP use TLS connection")
    options.define('smtp_username', default="fonoavisos@puentesarr.in",
        type=str, help="SMTP username connection")
    options.define('smtp_password', default="fonoavisos", type=str,
        help="SMTP password connection")

    if os.path.exists(options.options.configfilename):
        options.parse_config_file(options.options.configfilename)
    else:
        raise Exception('No config file at %s.' %
            os.path.join(os.getcwd(), options.options.configfilename))

    options.parse_command_line()
    return options.options
