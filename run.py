#!/usr/bin/python
# -*- coding: utf-8 -*-

import config
import cache

from pyxsl.parse import get_data_and_index
from pyxsl.draw import draw_outside, draw_inside
from pyxsl.pick import pickle_data_and_index, get_data_index_from_pickle


import tornado.ioloop
import tornado.autoreload
import tornado.web

data_cache = cache.DataCacher()

data_cache.invalidate(*get_data_index_from_pickle())
#data_cache.invalidate(*get_data_and_index())




class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/main.html')


class SvgHandler(tornado.web.RequestHandler):
    def get(self):

        x = draw_inside(data = data_cache.data,
                    draw_dir=config.ROOT_DIR + '/hh/catalog',
        )

    #    y = draw_outside(index,
    #                 draw_dir=config.ROOT_DIR + '/hh/catalog',
    #                 search_files=[config.ROOT_DIR + '/hh/blocks/searchresult/search-vacancy-result-oldstyle.xsl'],
    #    )

        self.set_header('Content-Type', 'image/svg+xml')
        self.finish(x)

if __name__ == "__main__":

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/svg", SvgHandler),
    ])

    application.listen(8888)
    io_loop = tornado.ioloop.IOLoop.instance()

    #tornado.autoreload.start(io_loop, 1000)
    io_loop.start()
