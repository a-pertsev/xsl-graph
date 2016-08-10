# -*- coding: utf-8 -*-

import gv
import os
import logging
from copy import deepcopy

import config
from pyxsl.parse import get_xsls_in_dir

logger = logging.getLogger(name='drawingLogger')


def create_graph():
    logger.debug('Creating graph...')

    graph = gv.graph('xsls')
    gv.setv(graph, 'charset', 'utf-8')
    gv.setv(graph, 'rankdir', 'LR')

    item = gv.protoedge(graph)
    gv.setv(item, 'minlen', '10')
    gv.setv(item, 'dir', 'forward')

    return graph


def render_graph(graph):
    logger.debug('Drawing graph...')
    gv.layout(graph, 'dot')
    data = gv.renderdata(graph, 'svg')
    logger.debug('End')
    return data


def reinit_wrap(func):
    def new_func(self, *args, **kwargs):
        self.reinit()
        result = func(self, *args, **kwargs)
        self.reinit()
        return result
    return new_func


class Drawer(object):
    def __init__(self, data, index, xsl_root=config.ROOT_XSL_DIR):
        self.data = deepcopy(data)
        self.index = deepcopy(index)
        self.xsl_root = xsl_root

    def reinit(self):
        self.__drawn_nodes = set([])
        self.__drawn_edges = set([])
        self.__depth = 0
        self.__limit = None
        self.__squash = False

    def get_relative_path(self, file_path):
        return os.path.relpath(file_path, self.xsl_root)

    @reinit_wrap
    def draw_inside(self, graph, search_files=None, draw_dir=None):
        files = []

        if search_files is not None:
            files += search_files

        if draw_dir is not None:
            files += get_xsls_in_dir(draw_dir)

        self.__draw_related_inside(graph, files)

        return graph

    def __draw_related_inside(self, graph, files):
        for xsl_file in files:
            file_data = self.data.get(xsl_file)
            if file_data is None:
                continue

            if xsl_file not in self.__drawn_nodes:
                gv.node(graph, '{0}'.format(self.get_relative_path(xsl_file)))
                self.__drawn_nodes.add(xsl_file)

            imports = file_data.get('imports')
            if not imports:
                continue

            for xsl_import in imports:
                if (xsl_file, xsl_import) not in self.__drawn_edges:
                    gv.edge(graph, self.get_relative_path(xsl_file), self.get_relative_path(xsl_import))
                    self.__drawn_edges.add((xsl_file, xsl_import))

            self.__draw_related_inside(graph, imports)

    @reinit_wrap
    def draw_outside(self, graph, search_files=None, draw_dir=None, limit=None, squash=True):
        self.__squash = squash
        self.__limit = limit

        if search_files is not None:
            self.__draw_related_outside(graph, search_files)
        elif draw_dir is not None:
            self.__draw_related_outside(graph, get_xsls_in_dir(draw_dir))
        else:
            for file_name, imported_by in self.index.iteritems():
                gv.node(graph, file_name)
                for imp in set(imported_by):
                    gv.edge(graph, self.get_relative_path(file_name), self.get_relative_path(imp))
        return graph

    def __draw_related_outside(self, graph, search_files):
        for search_file in search_files:
            if search_file not in self.__drawn_nodes:
                gv.node(graph, self.get_relative_path(search_file))
                self.__drawn_nodes.add(search_file)

            imported_by = self.index.get(search_file)

            if imported_by is None:
                continue

            imported_by = set(imported_by)

            squashed = get_squashed(imported_by, self.index) if len(imported_by) > 8 and self.__squash else []
            squashed = squashed if len(squashed) > 6 else []

            file_rel_path = self.get_relative_path(search_file)

            for imp in imported_by:
                if imp not in self.__drawn_nodes:
                    self.__drawn_nodes.add(imp)
                    if imp not in squashed:
                        gv.node(graph, self.get_relative_path(imp))

                if (imp, file_rel_path) not in self.__drawn_edges:
                    self.__drawn_edges.add((imp, file))
                    if imp not in squashed:
                        gv.edge(graph, self.get_relative_path(imp), file_rel_path)

            if squashed:
                name = '{} files importing {}'.format(len(squashed), file_rel_path)
                if name not in self.__drawn_nodes:
                    self.__drawn_nodes.add(name)
                    n = gv.node(graph, name)
                    gv.setv(n, 'fontsize', '25')
                    gv.setv(n, 'tooltip', '\n'.join(map(self.get_relative_path, squashed)))

                if (name, file_rel_path) not in self.__drawn_edges:
                    self.__drawn_edges.add((name, file_rel_path))
                    gv.edge(graph, name, file_rel_path)

            self.__depth += 1

            if self.__limit is None or self.__depth < self.__limit:
                self.__draw_related_outside(graph, imported_by)


def get_squashed(files, index):
    return [file_name for file_name in files if index.get(file_name) is None]



