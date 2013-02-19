# -*- coding: utf-8 -*-

import gv
import os
import logging

import config
from parse import get_xsls_in_dir


def create_graph():
    logging.debug('Creating graph...')

    graph = gv.graph('xsls')
    gv.setv(graph, 'charset', 'utf-8')
    gv.setv(graph, 'rankdir', 'LR')

    item = gv.protoedge(graph)
    gv.setv(item, 'minlen', '10')
    gv.setv(item, 'dir', 'forward')

    return graph


def render_graph(graph, name):
    logging.debug('Drawing graph...')
    gv.layout(graph, 'dot')
    gv.render(graph, 'svg', os.path.join(config.RESULTS_DIR, name))

    logging.debug('End')


def draw_inside(data, search_files=None, start_dir=None, filename='inside'):
    def draw_related(data, files, drawn_nodes, drawn_edges):
        for xsl_file in files:
            file_data = data.get(xsl_file)
            if file_data is None:
                continue

            if xsl_file not in drawn_nodes:
                gv.node(graph, '{0}'.format(os.path.relpath(xsl_file, config.ROOT_DIR)))
                drawn_nodes.append(xsl_file)

            imports = file_data.get('imports')
            if not imports:
                continue

            for xsl_import in imports:
                if (xsl_file, xsl_import) not in drawn_edges:
                    gv.edge(graph, os.path.relpath(xsl_file, config.ROOT_DIR), os.path.relpath(xsl_import, config.ROOT_DIR))
                    drawn_edges.append((xsl_file, xsl_import))

            draw_related(data, imports, drawn_nodes, drawn_edges)

    graph = create_graph()

    files = []

    if search_files is not None:
        files += search_files

    if start_dir is not None:
        files += get_xsls_in_dir(start_dir)

    draw_related(data, files, [], [])

    render_graph(graph, '{0}.svg'.format(filename))


def draw_outside(index, search_files=None, start_dir=None):
    def draw_related(index, search_files, drawn_nodes, drawn_edges):

        for search_file in search_files:
            imported_by = index.get(search_file)
            if imported_by is None:
                continue

            if search_file not in drawn_nodes:
                gv.node(graph, '{0}'.format(os.path.relpath(search_file, config.ROOT_DIR)))
                drawn_nodes.append(search_file)

            imported_by = set(imported_by)

            for imp in imported_by:
                if imp not in drawn_nodes:
                    gv.node(graph, '{0}'.format(os.path.relpath(imp, config.ROOT_DIR)))
                    drawn_nodes.append(imp)
                if (imp, file) not in drawn_edges:
                    gv.edge(graph, os.path.relpath(imp, config.ROOT_DIR), os.path.relpath(search_file, config.ROOT_DIR))
                    drawn_edges.append((imp,file))

            draw_related(index, imported_by, drawn_nodes, drawn_edges)

    graph = create_graph()

    if search_files is not None:
        draw_related(index, search_files, [], [])

    else:
        for file_name, imported_by in index.iteritems():
            gv.node(graph, '{0}'.format(file_name))
            for imp in set(imported_by):
                gv.edge(graph, os.path.relpath(file_name, start_dir), os.path.relpath(imp, start_dir))


    render_graph(graph, 'outside.svg')
