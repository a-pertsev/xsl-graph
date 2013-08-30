#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import etree, objectify


import config

from pyxsl.parse import get_data_and_index, get_all_inner_xsl, get_all_ancestors
from pyxsl.analyze import search_cross_platform_imports, get_not_used_xsls, analyze_modes_usage, analyze_funcs_usage
from pyxsl.pick import pickle_data_and_index, get_data_index_from_pickle


if __name__ == "__main__":
#    result = etree.fromstring(""" <xsl:stylesheet
#                                        version="1.0"
#                                        xmlns:hh="http://schema.reintegration.hh.ru/types"
#                                        exclude-result-prefixes="hh func"
#                                        xmlns:func="http://exslt.org/functions"
#                                        xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
#                                        xmlns="http://www.w3.org/1999/xhtml"></xsl:stylesheet>  """)
#
#    result.extend(get_all_inner_xsl('/home/apertsev/workspace/hh.sites.main/xhh/xsl/ambient/similar-vacancy-result.xsl'))
#    print etree.tostring(result, pretty_print=True)
#    x

    if 1:
        data, index = get_data_and_index(start_dir=config.ROOT_DIR)
        pickle_data_and_index(data, index)
    else:
        data, index = get_data_index_from_pickle()

    search_cross_platform_imports(index, config.ROOT_DIR + '/hh')
    print analyze_modes_usage(data)

    print get_not_used_xsls(data, index)