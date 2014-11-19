# -*- coding: utf-8 -*-

from collections import defaultdict
from pyproc.draw import render_templates_tree

from pyproc.stylesheet import Stylesheet
from pyproc.analyze import get_applies_tree
from pyproc.templates import compare_import_priorities
from pyxsl import draw

if __name__ == "__main__":
    xsl = '/home/apertsev/workspace/frontik/xhh/xsl/sochi/index.xsl'
#    xsl = '/home/apertsev/workspace/xsl-graph/tests/xsl/template_modes_test/1.xsl'
#    stylesheet = Stylesheet(xsl)
#    templates = stylesheet.all_templates
#
#    called_templates = defaultdict(list)
#    name_templates = defaultdict(list)
#
#    for template in templates:
#        for item in template.external_links:
#            template_name = getattr(item, 'name', None)
#            if template_name is not None:
#                called_templates[template_name].append(item)
#
#        if template.name is not None:
#            name_templates[template.name].append(template)
#
#
#    links = []
#
#    for name, templates in called_templates.iteritems():
#        if len(name_templates[name]) > 1:
#            sorted_templates = sorted(name_templates[name],
#                                      reverse=True,
#                                      cmp=lambda x,y: compare_import_priorities(x.i_priority, y.i_priority))
#            links.append((sorted_templates[0], templates))
#
#    print links

    from pyproc import analyze
    from lxml import etree

    stylesheet = Stylesheet(xsl)

    a = get_applies_tree(xsl)
    print a
    s


    with open('test.svg', 'w') as f:
        f.write(get_applies_tree(xsl))

#    print etree.tostring(analyze.get_full_xml(xsl), pretty_print=True)
