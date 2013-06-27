#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import simplejson
from functools import partial
from itertools import chain, imap, groupby

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
        file = self.get_argument('file', 'hh/blocks/page.xsl')

        x = draw_inside(
            data=data_cache.data,
            search_files=[str(os.path.join(config.ROOT_DIR, file))]
        )

    #    y = draw_outside(index,
    #                 draw_dir=config.ROOT_DIR + '/hh/catalog',
    #                 search_files=[config.ROOT_DIR + '/hh/blocks/searchresult/search-vacancy-result-oldstyle.xsl'],
    #    )

        self.set_header('Content-Type', 'image/svg+xml')
        self.finish(x)


def sort_func(text, item):
    variants = item.split('.')
    variants.append(item)
    return max(imap(lambda x: x.find(text), variants))


class SuggestHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument('name')

        files = data_cache.file_names

        sort_func_partial = partial(sort_func, name)
        suggests = list(chain.from_iterable([list(g) for k,g in groupby(sorted(files, key=sort_func_partial), sort_func_partial)][1:]))

        self.set_header('Content-Type', 'application/json')

        self.finish(simplejson.dumps(suggests[:15]))





if __name__ == "__main__":

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/svg", SvgHandler),
        (r"/file_suggest", SuggestHandler),
    ])

    application.listen(8888)
    io_loop = tornado.ioloop.IOLoop.instance()

    #tornado.autoreload.start(io_loop, 1000)
    io_loop.start()
