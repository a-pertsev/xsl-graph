# -*- coding: utf-8 -*-

import os
import logging

from lxml import etree
from collections import defaultdict

import config


logger = logging.getLogger(name='parsingLogger')

XSL_NS_TEXT = 'http://www.w3.org/1999/XSL/Transform'
XSL_NS = '{http://www.w3.org/1999/XSL/Transform}'
FUNC_NS = 'http://exslt.org/functions'
NS_MAP = {'xsl': XSL_NS_TEXT}


def get_xsls_in_dir(dir_name):
    return [os.path.join(dir,file) for dir,_,files in os.walk(dir_name) for file in files if 'xsl' in file]

def is_xsl_tag(element, tag_name):
    return element.tag == '{0}{1}'.format(XSL_NS, tag_name)

def get_tree(xsl_name):
    if not os.path.exists(xsl_name):
        logger.error(['No such a file', xsl_name])
        return None
    try:
        return etree.parse(xsl_name)
    except:
        print xsl_name
        raise


def parse_file(xsl_file_name, from_file):
    tree = get_tree(xsl_file_name)

    current_dir = os.path.dirname(xsl_file_name)

    result = defaultdict(list)

    for el in tree.getiterator():
        if is_xsl_tag(el, 'import'):
            result['imports'].append(os.path.abspath(os.path.join(current_dir, el.get('href'))))

        elif is_xsl_tag(el, 'template'):
            mode = el.get('mode', None)
            name = el.get('name', None)

            result['templates'].append({
                'match': el.get('match', None),
                'mode': mode,
                'name': name})

            if mode is not None:
                result['modes'].append(mode)

            if name is not None:
                result['names'].append(name)

        elif is_xsl_tag(el, 'apply-templates'):
            mode = el.get('mode', None)

            if mode is not None:
                result['applied_modes'].append(mode)

        elif is_xsl_tag(el, 'call-template'):
            result['called-templates'].append(el.get('name'))

        elif is_xsl_tag(el, 'key'):
            result['keys'].append({
                'name': el.get('name', None),
                'match': el.get('match', None),
                'use': el.get('use', None)})

        elif is_xsl_tag(el, 'variable'):
            result['variables'].append(el.get('name'))

        elif el.tag == '{{0}}{1}'.format(FUNC_NS, 'function'):
            result['functions'].append(el.get('name'))

    return result



def parse_files(start_dir, file_list, from_file=None):
    for file_name in file_list:
        parse_results = parse_file(file_name, from_file=from_file)

        if parse_results is None:
            return

        parse_results.update(short_path=os.path.relpath(file_name, start_dir))

        for pair in parse_files(start_dir, parse_results['imports'], from_file=file_name):
            yield pair

        yield (file_name, parse_results)


def get_data(start_files=[], start_dir=config.ROOT_DIR):
    logger.debug('Parsing dirs...')
    files = start_files[:]

    root_dir = start_dir or config.ROOT_DIR

    if start_dir is not None:
        files = files + get_xsls_in_dir(start_dir)

    logger.debug('Dirs data collecting...')
    data = dict(parse_files(root_dir, files))

    return data


def get_data_and_index(start_files=[], start_dir=config.ROOT_DIR):

    data = get_data(start_files, start_dir)

    index = defaultdict(list)

    for file, stats in data.iteritems():
        for imp in stats.get('imports'):
            index[imp].append(file)

    return data, index


def cmp_xsl_tags(el1, el2):
    if el1.tag != el2.tag:
        return 1 if el1.tag > el2.tag else -1

    if el1.get('match', None) != el2.get('match', None):
        return 1 if el1.get('match', None) > el2.get('match', None) else -1

    if el1.get('mode', None) != el2.get('mode', None):
        return 1 if el1.get('mode', None) > el2.get('mode', None) else -1

    if el1.get('name', None) != el2.get('name', None):
        return 1 if el1.get('mode', None) > el2.get('mode', None) else -1

    return 1


def get_all_inner_xsl(xsl_name):
    tree = get_tree(xsl_name)

    current_dir = os.path.dirname(xsl_name)

    result = []

    for el in tree.getroot():
        if is_xsl_tag(el, 'import'):
            import_path = os.path.abspath(os.path.join(current_dir, el.get('href')))
            result.extend(get_all_inner_xsl(import_path))
        else:
            result.append(el)

    return sorted(result, cmp=cmp_xsl_tags)


def get_all_ancestors(xsl_name, index):
    ancestors = index.get(xsl_name, [])

    for ancestor in ancestors:
        for far_ancestor in get_all_ancestors(ancestor, index):
            yield far_ancestor

    if not ancestors:
        yield xsl_name