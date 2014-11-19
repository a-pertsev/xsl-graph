# -*- coding: utf-8 -*-

from lxml import etree
from itertools import imap
from collections import defaultdict

from pyproc.common import XSL_NS
from pyproc.tree import ResultTree
from pyproc.stylesheet import Stylesheet
from pyproc.templates import CallTemplate


def get_not_used_templates(stylesheet):
    templates = stylesheet.all_templates
    return templates


def build_external_links_tree(node, modes, templates, processed):
    if node in processed:
        return

    processed.append(node)

    tree = {node: []}

    for link in node.external_links:
        if isinstance(link, CallTemplate):
            continue

        mode_eqal_nodes = modes.get(link.mode)
        if not mode_eqal_nodes:
            print 'O_O', node, link
            continue

        for linked_node in mode_eqal_nodes:
            if linked_node.match in link.select:
                links_tree = build_external_links_tree(linked_node, modes, templates, processed)
                if links_tree is not None:
                    tree[node].append(links_tree)

    return tree


def cut_not_used_templates(all_templates):
    modes = defaultdict(list)

    for template in all_templates:
        if template.match is not None:
            modes[template.mode].append(template)

    for mode, templates in modes.iteritems():
        result = []
        for template in templates:
            result.append(template)


def get_applies_tree(xsl):
    stylesheet = Stylesheet(xsl)

    modes = defaultdict(list)
    root = None

    #cut_not_used_templates(stylesheet.all_templates)

    for template in stylesheet.all_templates:
        if template.match is not None:
            modes[template.mode].append(template)
            if template.mode is None and template.match.string == 'doc':
                root = template

    assert root != None, 'No "doc" root element in xsl'

    tree = ResultTree(root, modes, stylesheet.all_templates)

    return tree


def get_full_xml(xsl):
    stylesheet = Stylesheet(xsl)

    result = etree.fromstring("""<xsl:stylesheet
                                     version="1.0"
                                     xmlns:hh="http://schema.reintegration.hh.ru/types"
                                     exclude-result-prefixes="hh func"
                                     xmlns:func="http://exslt.org/functions"
                                     xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                                     xmlns="http://www.w3.org/1999/xhtml">\n</xsl:stylesheet>  """)

    for template in stylesheet.all_templates:
        new_template = etree.Element('{0}template'.format(XSL_NS))
        for attr, value in template.element.attrib.items():
            new_template.set(attr, value)
            new_template.set('import-priority', '.'.join(imap(str,template.i_priority)))

        have_xsl_applying = False
        empty = not template.element.text and not any(template.element.iter())

        for node in template.element.iter(tag=etree.Element):
            node_tag = node.tag.replace(XSL_NS, '')

            if node_tag == node.tag or node_tag not in ['apply-templates', 'call-template', 'apply-imports']:
                continue

            node.tail = '\n'
            new_template.append(node)
            have_xsl_applying = True


        if have_xsl_applying:
            new_template.text = '\n'
        elif not empty:
            new_template.append(etree.Comment('some stuff'))

        new_template.tail = '\n\n'

        result.append(new_template)

    return result



