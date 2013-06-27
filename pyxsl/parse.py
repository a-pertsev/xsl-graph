# -*- coding: utf-8 -*-

import os
import logging

from lxml import etree
from collections import defaultdict

import config

XSL_NS = "{http://www.w3.org/1999/XSL/Transform}"


def get_xsls_in_dir(dirname):
    return [os.path.join(dir,file) for dir,_,files in os.walk(dirname) for file in files if 'xsl' in file]

def parse_file(xsl_file_name, get_imports, get_templates, get_modes, from_file, get_keys):
    result = {}
    if not os.path.exists(xsl_file_name):
        logging.error('No such a file: {0} -> {1}'.format(from_file, xsl_file_name))
        return None
    tree = etree.parse(xsl_file_name)
    if get_imports:
        current_dir = os.path.dirname(xsl_file_name)
        imports = [os.path.abspath(os.path.join(current_dir, i.get('href'))) for i in tree.findall(XSL_NS + 'import')]
        result.update(imports=imports)
    if get_templates:
        templates = tree.findall(XSL_NS + 'template[@match]')
        templates = map(lambda template: {'match': template.get('match'), 'mode': template.get('mode', None)}, templates)
        result.update(templates = templates)
    if get_keys:
        keys = tree.findall('//{0}key'.format(XSL_NS))
        keys = map(lambda key: {'name': key.get('name'), 'match': key.get('match'), 'use': key.get('use')}, keys)
        result.update(keys=keys)

    if get_modes:
        modes = set(template_desc.get('mode') for template_desc in tree.findall(XSL_NS + 'template[@mode]'))
        result.update(modes = modes)
        applied_modes = set(template_desc.get('mode') for template_desc in tree.findall(XSL_NS + 'apply-templates[@mode]'))
        result.update(applied_modes = modes)
    return result


def parse_files(start_dir, file_list, get_imports=True, get_templates=False, get_modes=True, from_file=None, get_keys=False):
    for file_name in file_list:
        parse_results = parse_file(file_name, get_imports=get_imports, get_templates=get_templates, get_modes=get_modes, from_file=from_file, get_keys=get_keys)
        if parse_results is None:
            return
        parse_results.update(short_path=os.path.relpath(file_name, start_dir))
        for pair in parse_files(start_dir, parse_results.get('imports'), get_modes=get_modes, from_file=file_name, get_templates=get_templates, get_imports=get_imports, get_keys=get_keys):
            yield pair
        yield (file_name, parse_results)


def get_data(start_files=[], start_dir=config.ROOT_DIR):
    logging.debug('Parsing dirs...')
    files = start_files[:]

    root_dir = start_dir or config.ROOT_DIR

    if start_dir is not None:
        files = files + get_xsls_in_dir(start_dir)

    logging.debug('Dirs data collecting...')
    data = dict(parse_files(root_dir, files))

    return data


def get_data_and_index(start_files=[], start_dir=config.ROOT_DIR):

    data = get_data(start_files, start_dir)

    index = defaultdict(list)

    for file, stats in data.iteritems():
        for imp in stats.get('imports'):
            index[imp].append(file)

    return data, index

