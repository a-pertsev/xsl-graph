#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import simplejson
import logging
import logging.handlers

from functools import partial
from itertools import chain, imap, groupby
from operator import itemgetter

import tornado.ioloop
import tornado.autoreload
import tornado.web

import config
import cache

import pyxsl.analyze as analyze
from pyxsl.parse import get_data_and_index, get_data
from pyxsl.draw import render_graph, create_graph, Drawer
from pyxsl.pick import pickle_data_and_index, get_data_index_from_pickle


data_cache = cache.DataCacher()

try:
    data_cache.invalidate(*get_data_index_from_pickle())
except IOError:
    data, index = get_data_and_index()
    pickle_data_and_index(data, index)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/main.html')


class SVGImportsHandler(tornado.web.RequestHandler):
    def get(self):
        file = str(os.path.join(config.ROOT_XSL_DIR, self.get_argument('file', 'ambient/blocks/page.xsl')))

        limit = self.get_argument('limit_out', None)

        drawer = Drawer(data_cache.data, data_cache.index)

        graph = create_graph()

        drawer.draw_inside(graph, [file])
        drawer.draw_outside(graph, [file], limit=limit)

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
        suggests = list(chain.from_iterable(
                         [list(g) for k,g in
                            groupby(sorted(files, key=sort_func_partial), sort_func_partial)][1:]))

        self.set_header('Content-Type', 'application/json')

        self.finish(simplejson.dumps(suggests[:15]))


class InvalidateHandler(tornado.web.RequestHandler):
    def get(self):
        data_cache.invalidate(*get_data_and_index())
        pickle_data_and_index(data_cache.data, data_cache.index)



def get_errors_from_log(handler):
    records = filter(lambda record: record.levelname == 'ERROR', handler.buffer)
    grouped = groupby(sorted(map(lambda record: record.msg, records), key=itemgetter(0)), key=itemgetter(0))

    return dict((key, map(AnalyzeHandler.clean_records, group)) for key, group in grouped)


class AnalyzeHandler(tornado.web.RequestHandler):

    @staticmethod
    def clean_records(records):
        return map(lambda xsl_name: xsl_name.replace(config.ROOT_XSL_DIR, '').lstrip('/'), records[1:])


    def get(self):
        logger = logging.getLogger(name='parsingLogger')
        handler = logging.handlers.MemoryHandler('hndlr')
        logger.addHandler(handler)

        data = get_data()

        result = {
            'Not used XSLS': analyze.get_not_used_xsls(data_cache.data, data_cache.index),
            'Duplicated imports':  analyze.get_duplicated_imports(data)
        }

        result.update(get_errors_from_log(handler))

        self.finish(simplejson.dumps(result))



if __name__ == "__main__":

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/svg", SVGImportsHandler),
        (r"/file_suggest", SuggestHandler),
        (r"/cache_invalidate", InvalidateHandler),
        (r"/analyze", AnalyzeHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),

    ])

    port = os.environ.get('PORT', config.PORT)
    application.listen(port)
    io_loop = tornado.ioloop.IOLoop.instance()
    logging.getLogger(name='appLogger').info('instance started at http://localhost:{}'.format(port))

    tornado.autoreload.start(io_loop, 1000)
    io_loop.start()
