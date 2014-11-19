# -*- coding: utf-8 -*-

import logging
import os
from lxml import etree

from pyproc.common import XSL_NS, require
from pyproc.templates import Template


def get_templates_ignore_duplicates(stylesheets, used_imports, result):
    for import_index, imported_ss in enumerate(reversed(stylesheets)):
        if imported_ss in used_imports:
            logging.warn('Duplicated import: {0}'.format(imported_ss))
            continue

        used_imports.append(imported_ss)

        imported_templates = map(lambda temp: temp.add_i_priority_index(import_index), imported_ss.templates)
        result.extend(imported_templates)
        get_templates_ignore_duplicates(imported_ss.imports, used_imports, result)

    return result


class MetaStylesheet(type):
    '''
       Returns Stylesheet singleton for every xsl file.
    '''
    stylesheets = {}

    def __call__(self, xsl_file_name, *args, **kwargs):
        if xsl_file_name in MetaStylesheet.stylesheets:
            return MetaStylesheet.stylesheets[xsl_file_name]

        if not os.path.exists(xsl_file_name):
            raise Exception('No such stylesheet: {}'.format(xsl_file_name))
            return None

        new_stylesheet = type.__call__(self, xsl_file_name, *args, **kwargs)
        MetaStylesheet.stylesheets[xsl_file_name] = new_stylesheet

        return new_stylesheet


class Stylesheet(object):

    __metaclass__ = MetaStylesheet

    def __init__(self, xsl_file_name):
        self.path = xsl_file_name
        self.__imports = []
        self.__templates = []
        self.__all_templates = []


    def __init_stylesheet(self):
        try:
            tree = etree.parse(self.path)
        except:
            print self.path
            raise

        dir_name = os.path.dirname(self.path)

        for node in tree.getroot():
            if isinstance(node, etree._Comment):
                continue

            tag_name = node.tag.replace(XSL_NS, '')

            if tag_name == node.tag:
                continue

            if tag_name == 'template':
                self.__templates.append(Template(node, self))
            elif tag_name == 'import':
                path = os.path.abspath(os.path.join(dir_name, node.get('href')))
                self.__imports.append(Stylesheet(path))
            elif tag_name == 'include':
                path = os.path.abspath(os.path.join(dir_name, node.get('href')))
                include_stylesheet = Stylesheet(path)
                self.__templates.extend(include_stylesheet.all_templates)


    def __init_full_templates_structure(self):
        templates = self.templates[:]

        for import_index, imported_ss in enumerate(reversed(self.imports)):
            imported_templates = map(lambda temp: temp.copy().add_i_priority_index(import_index), imported_ss.all_templates)
            templates.extend(imported_templates)

#        get_templates_ignore_duplicates(self.imports, [], templates)

        self.__all_templates = templates


    @require(__init_stylesheet)
    def __get_templates(self):
        return self.__templates

    @require(__init_full_templates_structure)
    def __get_all_templates(self):
        return self.__all_templates

    @require(__init_stylesheet)
    def __get_imports(self):
        return self.__imports

    @require(__init_stylesheet)
    def __get_all_imports(self):
        return {self.path: [imp.get_all_imports() for imp in self.__imports]}

    def get_all_imports(self):
        return self.__get_all_imports()

    imports = property(__get_imports)
    all_templates = property(__get_all_templates)
    templates = property(__get_templates)


    def __repr__(self, *args, **kwargs):
        return '<Stylesheet: {0}>'.format(os.path.split(self.path)[-1])
