# -*- coding: utf-8 -*-


from copy import deepcopy

from pyproc.match import Match
from pyproc.common import is_xsl_tag, require


class ApplyTemplates(object):
    def __init__(self, element, context):
        self.context = context
        self.element = element
        self.select = Match(element.get('select', '*'), context.match)
        self.mode = element.get('mode')

    def __repr__(self):
        return '<Apply-Templates: {}>'.format(
            ' '.join('{}="{}"'.format(attr, getattr(self, attr, ''))
                                        for attr in ['select', 'mode']
                                            if getattr(self, attr, None)))

class CallTemplate(object):
    def __init__(self, element, context):
        self.context = context
        self.element = element
        self.name = element.get('name')

    def __repr__(self):
        return '<Call-Template: name="{0}"'.format(self.name)


class Template(object):
    def __init__(self, element):
        self.element = element
        self.name = element.get('name')
        self.mode = element.get('mode')
        self.priority = element.get('priority', 0)
        self.i_priority = [0]
        self.__external_links = []

        match_string = element.get('match')
        self.match = Match(match_string) if match_string else None

    def __init_external_links(self):
        for sub_element in self.element.iter():
            if is_xsl_tag(sub_element, 'apply-templates'):
                self.__external_links.append(ApplyTemplates(sub_element, self))

            elif is_xsl_tag(sub_element, 'call-template'):
                self.__external_links.append(CallTemplate(sub_element, self))


    @require(__init_external_links)
    def get_external_links(self):
        return self.__external_links

    external_links = property(get_external_links)


    def add_i_priority_index(self, index):
        self.i_priority.insert(0, index)
        return self

    def copy(self):
        return deepcopy(self)

    def __repr__(self):
        return '<Template: {}>'.format(
            ' '.join('{}="{}"'.format(attr, getattr(self, attr, ''))
                                        for attr in ['name', 'match', 'mode']
                                            if getattr(self, attr, None)))