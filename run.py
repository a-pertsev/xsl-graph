#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import simplejson
from functools import partial
from itertools import chain, imap, groupby

import config
import cache

from pyxsl.parse import get_data_and_index
from pyxsl.draw import draw_outside, draw_inside, render_graph, create_graph
from pyxsl.pick import pickle_data_and_index, get_data_index_from_pickle


import tornado.ioloop
import tornado.autoreload
import tornado.web

data_cache = cache.DataCacher()

data_cache.invalidate(*get_data_index_from_pickle())




class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/main.html')


class SvgHandler(tornado.web.RequestHandler):
    def get(self):
        file = str(os.path.join(config.ROOT_DIR, self.get_argument('file', 'hh/blocks/page.xsl')))

        graph = create_graph()

        graph = draw_inside(
            graph=graph,
            data=data_cache.data,
            search_files=[file],
        )

        graph = draw_outside(
            graph=graph,
            index=data_cache.index,
            search_files=[file],
        )

        result = render_graph(graph)

        self.set_header('Content-Type', 'image/svg+xml')
        self.finish(result)


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


class InvalidateHandler(tornado.web.RequestHandler):
    def get(self):
        data_cache.invalidate(*get_data_and_index())
        pickle_data_and_index(data_cache.data, data_cache.index)


if __name__ == "__main__":

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/svg", SvgHandler),
        (r"/file_suggest", SuggestHandler),
        (r"/cache_invalidate", InvalidateHandler),
    ])

    application.listen(8888)
    io_loop = tornado.ioloop.IOLoop.instance()

    #tornado.autoreload.start(io_loop, 1000)
    io_loop.start()
