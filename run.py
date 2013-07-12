#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
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
from pyxsl.draw import draw_outside, draw_inside, render_graph, create_graph
from pyxsl.pick import pickle_data_and_index, get_data_index_from_pickle



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
        return map(lambda xsl_name: xsl_name.replace(config.ROOT_DIR, '').lstrip('/'), records[1:])


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
        (r"/svg", SvgHandler),
        (r"/file_suggest", SuggestHandler),
        (r"/cache_invalidate", InvalidateHandler),
        (r"/analyze", AnalyzeHandler),
    ])

    application.listen(8888)
    io_loop = tornado.ioloop.IOLoop.instance()

    #tornado.autoreload.start(io_loop, 1000)
    io_loop.start()
