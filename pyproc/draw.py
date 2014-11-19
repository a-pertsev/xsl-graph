# -*- coding: utf-8 -*-

import gv
import logging

from pyproc.analyze import get_applies_tree
from pyxsl.draw import create_graph


def draw_tree(tree, graph, processed):

    for item, values in tree.iteritems():
        for value in values:
            if not value:
                continue
            gv.edge(graph, item, value.keys()[0])

        if item in processed:
                continue

        processed.append(item)
        gv.node(graph, item)

        for value in values:
            draw_tree(value, graph, processed)


def render_templates_tree(xsl):
    graph = create_graph()

    logging.debug('TRYING TO RENDER')

    gv.layout(graph, 'dot')

    tree = get_applies_tree(xsl)

    draw_tree(tree, graph, [])
    gv.layout(graph, 'dot')

    data = gv.renderdata(graph, 'svg')

    logging.debug('RENDERED!!!')

    return data