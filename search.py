# -*- coding: utf-8 -*-

import os
import logging
import pickle
import operator

import gv 

from lxml import etree
from itertools import chain
from collections import defaultdict

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

ROOT_DIR = "/home/apertsev/workspace/xhh2/xhh/xsl"
XSL_NS = "{http://www.w3.org/1999/XSL/Transform}"


modes_searcher = defaultdict(int)

def parse_file(xsl_file_name, get_imports, get_templates, modes_dict, from_file, get_keys):
    result = {}
    if not os.path.exists(xsl_file_name):
        logging.error('No such a file: {0} -> {1}'.format(from_file, xsl_file_name))
        return None
    tree = etree.parse(xsl_file_name)
    if get_imports is True:
        current_dir = os.path.dirname(xsl_file_name)
        imports=[os.path.abspath(os.path.join(current_dir, i.get('href'))) for i in tree.findall(XSL_NS + 'import')]
        result.update(imports=imports)
    if get_templates is True:
        templates = templates=tree.findall(XSL_NS + 'template[@match]')
        templates = map(lambda template: {'match': template.get('match'), 'mode': template.get('mode', None)}, templates)
        result.update(templates = templates)
    if get_keys is True:
        keys = tree.findall('//{0}key'.format(XSL_NS))
        keys = map(lambda key: {'name': key.get('name'), 'match': key.get('match'), 'use': key.get('use')}, keys)
        result.update(keys=keys)
    if modes_dict is not None:
        modes = set(template_desc.get('mode') for template_desc in tree.findall(XSL_NS + 'template[@mode]'))
        for mode in modes:
            modes_dict[mode] += len(tree.findall('//{0}apply-templates[@mode="{1}"]'.format(XSL_NS, mode)))
    return result

def parse_files(file_list, get_imports=True, get_templates=False, modes_dict=None, recursive=True, from_file=None, short_paths=True, get_keys=False):
    for file_name in file_list:
        parse_results = parse_file(file_name, get_imports=get_imports, get_templates=get_templates, modes_dict=modes_dict, from_file=from_file, get_keys=get_keys)
        if parse_results is None:
            return
        if short_paths is True:
            parse_results.update(short_path=os.path.relpath(file_name, start_dir))
        if recursive is True:
            for pair in parse_files(parse_results.get('imports'), recursive=recursive, modes_dict=modes_dict, from_file=file_name, get_templates=get_templates, get_imports=get_imports, get_keys=get_keys):
                yield pair
        yield (file_name, parse_results)
        

def search_inside(start_dir):
    logging.debug('Parsing dirs...')
    if os.path.isfile(start_dir):
        files = [start_dir]
    else:
        files = [[os.path.join(dir, file) for file in files if 'xsl' in file] for (dir,_,files) in os.walk(start_dir)]
        files = list(chain.from_iterable(files))

    
    logging.debug('Dirs data collecting...')
    data = dict(parse_files(files, modes_dict=modes_searcher, get_keys=True, get_templates=True))

    return data

def draw(data, start_dir):
    logging.debug('Creating graph...')
    graph = gv.graph('xsls')
    gv.setv(graph, 'charset', 'utf-8')
    gv.setv(graph, 'rankdir', 'LR')
    
    item = gv.protoedge(graph)
    gv.setv(item, 'minlen', '10')
    gv.setv(item, 'dir', 'forward')
    
    for _, props in data.iteritems():
        gv.node(graph, '{0}  ({1})'.format(props.get('short_path'), props.get('stars')))
        for imp in props.get('imports'):
            gv.edge(graph, props.get('short_path'), os.path.relpath(imp, start_dir))
    
    
    logging.debug('Drawing graph...')
    gv.layout(graph, 'dot')
    gv.render(graph, 'svg', 'inside.svg')
    
    logging.debug('End')


def search_outside(search_file=None):
    def draw_related(index, search_file, drawn_nodes, drawn_edges):
        
        imported_by = index.get(search_file)
        if imported_by is None:
            return

        if search_file not in drawn_nodes:
            gv.node(graph, '{0}'.format(os.path.relpath(search_file, ROOT_DIR)))
            drawn_nodes.append(search_file)
        
        for imp in set(imported_by):
            if imp not in drawn_nodes:
                gv.node(graph, '{0}'.format(os.path.relpath(imp, ROOT_DIR)))
                drawn_nodes.append(imp)
            if (imp, file) not in drawn_edges:
                gv.edge(graph, os.path.relpath(imp, ROOT_DIR), os.path.relpath(search_file, ROOT_DIR))
                drawn_edges.append((imp,file))
            draw_related(index, imp, drawn_nodes, drawn_edges)
    
    
    
    logging.debug('Parsing dirs...')
    
    files = [[os.path.join(dir, file) for file in files if 'xsl' in file] for (dir,_,files) in os.walk(ROOT_DIR)]
    files = chain.from_iterable(files)

    logging.debug('Dirs data collecting...')
    
    data = dict(parse_files(files))
    index = {}
    for file, stats in data.iteritems():
        for imp in stats.get('imports'):
            if imp not in index:
                index[imp] = [file]
            else:
                index[imp].append(file)
    

    logging.debug('Creating graph...')
    graph = gv.graph('xsls')
    gv.setv(graph, 'charset', 'utf-8')
    gv.setv(graph, 'rankdir', 'LR')
    
    item = gv.protoedge(graph)
    gv.setv(item, 'minlen', '10')
    gv.setv(item, 'dir', 'forward')
    
    
    if search_file is not None:
        draw_related(index, search_file, [], [])
    
    else:
        for file_name, imported_by in index.iteritems():
            gv.node(graph, '{0}'.format(file_name))
            for imp in set(imported_by):
                gv.edge(graph, os.path.relpath(file_name, start_dir), os.path.relpath(imp, start_dir))
        
    
    logging.debug('Drawing graph...')
    gv.layout(graph, 'dot')
    gv.render(graph, 'svg', 'outside.svg')
    
    logging.debug('End')


def get_all_imports(name, data_dict):
    single_file_data = data_dict.get(name, {})
    keys = single_file_data.get('keys', [])
    return keys + list(chain.from_iterable(get_all_imports(import_name, data_dict) for import_name in single_file_data.get('imports', [])))
    

def analyze_keys(data_dict):
    result_keys = defaultdict(list)
    for file_name in data_dict:
        result_keys[file_name] = get_all_imports(file_name, data_dict)

    print sorted(result_keys.iteritems(), key=lambda x: len(x[1]))[-1:][0]


def extend_one_file_templates(file_name, data_dict):
    xsl_data = data_dict.get(file_name, None)
    
    if xsl_data is None:
        return data_dict
    
    extended_templates = xsl_data.get('extended_templates', None)
    if extended_templates is not None:
        return data_dict
    
    templates = xsl_data.get('templates', None)
    xsl_data['extended_templates'] = []
    extended_templates = templates.copy()
    for template in extended_templates:
        template['import_priority'] = 0
        
    data_dic
        
    

    imports = xsl_data.get('imports', None)
    if imports is None:
        return data_dict
    
    for xsl_import in imports:
        imported_data = extend_one_file_templates(xsl_import, data_dict)
    
    

def extend_templates(data_dict):
    for file_name in data_dict:
        extend_one_file_templates(file_name, data_dict)


def search_and_pickle(start_dir):
    data = search_inside(start_dir)
    with open('pickled_xsl_'.format(start_dir), 'w') as f:
        pickle.dump(data, f)

def get_data_from_pickle():
    with open('pickled_xsl') as f:
        return pickle.load(f)

start_dir = '/home/apertsev/workspace/xhh2/xhh/xsl/rmr/blocks'

#search_and_pickle(start_dir)
data = search_inside(start_dir=start_dir)

#draw(data, start_dir=start_dir)

#print analyze_keys(get_data_from_pickle())

