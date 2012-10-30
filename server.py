# -*- coding: utf-8 *-*
import logging

from tornado import httpserver, ioloop
from tpaste import options, TPasteApplication

if __name__ == "__main__":
    opts = options.get_options()
    http_server = httpserver.HTTPServer(TPasteApplication())
    http_server.listen(opts.port)
    logging.info('Listening on %s port.' % opts.port)
    ioloop.IOLoop.instance().start()
