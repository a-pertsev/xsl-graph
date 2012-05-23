# -*- coding: utf-8 -*-

import os
import logging

import gv 

from lxml import etree
from itertools import chain
from collections import defaultdict

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

ROOT_DIR = "/home/apertsev/workspace/hh.ru/xhh/xsl"
start_dir = "/home/apertsev/workspace/hh.ru/xhh/xsl/ambient"
XSL_NS = "{http://www.w3.org/1999/XSL/Transform}"

modes_searcher = defaultdict(int)


def parse_file(xsl_file_name, get_imports, get_stars, modes_dict, from_file):
    result = {}
    if not os.path.exists(xsl_file_name):
        logging.error('No such a file: {0} -> {1}'.format(from_file, xsl_file_name))
        return None
    tree = etree.parse (xsl_file_name)
    if get_imports is True:
        current_dir = os.path.dirname(xsl_file_name)
        imports=[os.path.abspath(os.path.join(current_dir, i.get('href'))) for i in tree.findall(XSL_NS + 'import')]
        result.update(imports=imports)
    if get_stars is True:
        result.update(stars=len(tree.findall(XSL_NS + 'template[@match="*"]')))
    if modes_dict is not None:
        modes = set(template_desc.get('mode') for template_desc in tree.findall(XSL_NS + 'template[@mode]'))
        for mode in modes:
            modes_dict[mode] += len(tree.findall('//{0}apply-templates[@mode="{1}"]'.format(XSL_NS, mode)))
    return result

def parse_files(file_list, get_imports=True, get_stars=False, modes_dict=None, recursive=True, from_file=None, short_paths=True):
    for file_name in file_list:
        parse_results = parse_file(file_name, get_imports=get_imports, get_stars=get_stars, modes_dict=modes_dict, from_file=from_file)
        if parse_results is None:
            return
        if short_paths is True:
            parse_results.update(short_path=os.path.relpath(file_name, start_dir))
        if recursive is True:
            for pair in parse_files(parse_results.get('imports'), recursive=recursive, from_file=file_name):
                yield pair
        yield (file_name, parse_results)
        

def search_inside():
    logging.debug('Parsing dirs...')
    files = [[os.path.join(dir, file) for file in files if 'xsl' in file] for (dir,_,files) in os.walk(start_dir)]
    files = list(chain.from_iterable(files))
    
    logging.debug('Dirs data collecting...')
    data = dict(parse_files(files, modes_dict=modes_searcher))
    
    logging.debug('Creating graph...')
    graph = gv.graph('xsls')
    gv.setv(graph, 'charset', 'utf-8')
    gv.setv(graph, 'rankdir', 'LR')
    
    item = gv.protoedge(graph)
    gv.setv(item, 'minlen', '10')
    gv.setv(item, 'dir', 'forward')
    
    for file_name, props in data.iteritems():
        gv.node(graph, '{0}  ({1})'.format(props.get('short_path'), props.get('stars')))
        for imp in props.get('imports'):
            gv.edge(graph, props.get('short_path'), os.path.relpath(imp, start_dir))
    
    
    logging.debug('Drawing graph...')
    gv.layout(graph, 'dot')
    gv.render(graph, 'svg', 'test.svg')
    
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
    gv.render(graph, 'svg', 'test2.svg')
    
    logging.debug('End')

search_outside("/home/apertsev/workspace/hh.ru/xhh/xsl/global/common/variables.xsl")