# -*- coding: utf-8 -*-

import os
import logging

from itertools import groupby
from copy import deepcopy
from lxml import etree


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

ROOT_DIR = "/home/apertsev/workspace/xhh2/xhh/xsl"
XSL_NS = "{http://www.w3.org/1999/XSL/Transform}"


class Template(object):
    def __init__(self, el):
        self.match = el.get('match', '')
        self.name = el.get('name', '')
        self.mode = el.get('mode', '')
        self.priority = el.get('priority', 0)
        self.i_priority = [0]

    def __repr__(self):
        return '<Template: name="{0}" match="{1}" mode="{2}">'.format(self.name, self.match, self.mode)

    def copy(self):
        return deepcopy(self)
    
    def add_i_priority_index(self, index):
        self.i_priority.insert(0, index)
        return self 
    

class Stylesheet(object):
    def __init__(self, xsl_file_name):
        self.name = xsl_file_name
        self.imports = []
        
        tree = etree.parse(xsl_file_name)
        dirname = os.path.dirname(xsl_file_name)
        
        imports_paths = map(lambda xsl_import: os.path.abspath(os.path.join(dirname, xsl_import.get('href'))), tree.findall('{xsl}import'.format(xsl=XSL_NS)))
        for path in imports_paths:
            if not os.path.exists(path):
                logging.error('No such a file: {0}'.format(xsl_file_name))
                continue
            self.imports.append(Stylesheet(path))
            
        self.templates = map(Template, tree.findall('{xsl}template'.format(xsl=XSL_NS)))


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
        

xsl = '/home/apertsev/workspace/xhh2/xhh/xsl/hh/employer/vacancytemplates/blocks/vacancytemplates.xsl'
xsl2 = '/home/apertsev/workspace/frontik/xhh/xsl/ambient/searchvacancyresult.xsl'

stylesheet = Stylesheet(xsl2)
stylesheet.init_full_templates_structure()

def groupfunc(template):
    return template.mode.lower()

stylesheet.templates.sort(key=groupfunc)

for k, g in groupby(stylesheet.templates, groupfunc):
    print k, len([a for a in g])

