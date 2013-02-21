# -*- coding: utf-8 -*-

import os
import logging

from itertools import groupby, imap
from copy import deepcopy
from lxml import etree


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

ROOT_DIR = "/home/apertsev/workspace/xhh2/xhh/xsl"
XSL_NS = "{http://www.w3.org/1999/XSL/Transform}"


class Match(object):
    def __init__(self, match_string):
        self.string = match_string

    def __get__(self):
        return self.string

    def __repr__(self):
        return self.string


class Template(object):
    ''''
       Simple xsl:template serialized representation
    '''
    def __init__(self, el):
        self.match = Match(el.get('match', ''))
        self.name = el.get('name', '')
        self.mode = el.get('mode', '')
        self.priority = el.get('priority', 0)
        self.i_priority = [0]

    def __repr__(self):
        return '<Template: {}>'.format(
            ' '.join('{}="{}"'.format(attr, getattr(self, attr, ''))
                                     for attr in ['name', 'match', 'mode']
                                     if getattr(self, attr, None) != ''))

    def copy(self):
        return deepcopy(self)
    
    def add_i_priority_index(self, index):
        self.i_priority.insert(0, index)
        return self 



class MetaStylesheet(type):
    '''
       Metaclass provides Stylesheet Factory. Returns Stylesheet singleton for every xsl file.
    '''
    stylesheets = {}

    def __call__(self, xsl_file_name, *args, **kwargs):
        if xsl_file_name in MetaStylesheet.stylesheets:
            return MetaStylesheet.stylesheets[xsl_file_name]

        new_stylesheet = type.__call__(self, xsl_file_name, *args, **kwargs)
        MetaStylesheet.stylesheets[xsl_file_name] = new_stylesheet

        return new_stylesheet


class Stylesheet(object):
    ''''
       Simple xsl:stylesheet serialized representation
    '''

    __metaclass__ = MetaStylesheet

    def __init__(self, xsl_file_name):
        self.name = xsl_file_name
        self.imports = []
        
        tree = etree.parse(xsl_file_name)
        dir_name = os.path.dirname(xsl_file_name)

        self.__init_imports(tree, dir_name)

        self.templates = map(Template, tree.findall('{xsl}template'.format(xsl=XSL_NS)))


    def __init_structure(self, tree, dir_name):
        for node in tree:
            pass

    def __init_imports(self, tree, dir_name):
        imports_paths = map(lambda xsl_import: os.path.abspath(os.path.join(dir_name, xsl_import.get('href'))), tree.findall('{xsl}import'.format(xsl=XSL_NS)))
        for path in imports_paths:
            if not os.path.exists(path):
                logging.warn('Bad import: {} -> {}'.format(self.name, path))
                continue
            self.imports.append(Stylesheet(path))


    def group_templates(self):
        pass

    
    def init_full_templates_structure(self):
        self.templates = self._get_all_templates()

    
    def _get_all_templates(self):
        templates = map(lambda template: template.copy(), self.templates)
        
        for import_index, imported_ss in enumerate(reversed(self.imports)):
            imported_templates = map(lambda temp: temp.add_i_priority_index(import_index), imported_ss._get_all_templates())
            templates.extend(imported_templates)
            
        return templates

    def __repr__(self, *args, **kwargs):
        return '<Stylesheet: {0}>'.format(os.path.split(self.name)[-1])


xsl = '/home/apertsev/workspace/frontik/xhh/xsl/hh/blocks/page.xsl'
xsl2 = '/home/apertsev/workspace/frontik/xhh/xsl/ambient/searchvacancyresult.xsl'


dirname = '/home/apertsev/workspace/frontik/xhh/xsl'

xsls = [os.path.join(dir, file) for dir,_,files in os.walk(dirname) for file in files if file.endswith('.xsl')]

stylesheets = dict(imap(lambda xsl: (xsl, Stylesheet(xsl)), xsls))

stylesheet = Stylesheet(xsl2)
stylesheet2 = Stylesheet(xsl2)


#stylesheet2.init_full_templates_structure()
#print stylesheet2.templates

def groupfunc(template):
    return template.mode.lower()
