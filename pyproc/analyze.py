# -*- coding: utf-8 -*-
from lxml import etree
from pyproc.common import XSL_NS
from pyproc.stylesheet import Stylesheet


def get_not_used_templates(stylesheet):
    templates = stylesheet.all_templates
    return templates


def get_full_xml(xsl):
    stylesheet = Stylesheet(xsl)

    result = etree.fromstring(""" <xsl:stylesheet
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


    return etree.tostring(result, pretty_print=True)


def compare_import_priorities(priority1, priority2):
    l1 = len(priority1)
    l2 = len(priority2)

    if l1 != l2:
        return 1 if l1 < l2 else -1

    for index in xrange(l1):
        if priority1[index] != priority2[index]:
            return 1 if priority1[index] < priority2[index] else -1
    return 0