# -*- coding: utf-8 -*-


from pyproc.match import Select, Match
from pyproc.common import is_xsl_tag, require


class ApplyTemplates(object):
    def __init__(self, element, context):
        self.context = context
        self.element = element
        self.select = Select(element.get('select', '*'), context.match)
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
    def __init__(self, element, stylesheet):
        self.element = element
        self.stylesheet = stylesheet
        self.name = element.get('name')
        self.mode = element.get('mode')
        self.priority = element.get('priority', 0)
        self.i_priority = [0]
        self.__external_links = []
        self.apply_imports = False

        match_string = element.get('match')
        self.match = Match(match_string) if match_string else None

    def __init_external_links(self):
        for sub_element in self.element.iter():
            if is_xsl_tag(sub_element, 'apply-templates'):
                self.__external_links.append(ApplyTemplates(sub_element, self))

            elif is_xsl_tag(sub_element, 'call-template'):
                self.__external_links.append(CallTemplate(sub_element, self))

            elif is_xsl_tag(sub_element, 'apply-imports'):
                self.apply_imports = True


    @require(__init_external_links)
    def get_external_links(self):
        return self.__external_links

    external_links = property(get_external_links)


    def add_i_priority_index(self, index):
        self.i_priority.insert(0, index)
        return self

    def copy(self):
        template = Template(self.element, self.stylesheet)
        template.i_priority = self.i_priority[:]
        return template

    def __repr__(self):
        return '<Template: {attrs} ({stylesheet})>'.format(
            attrs=' '.join('{}="{}"'.format(attr, getattr(self, attr, ''))
                                        for attr in ['name', 'match', 'mode']
                                            if getattr(self, attr, None) is not None),
            stylesheet=self.stylesheet.path.replace('/home/apertsev/workspace/frontik/xhh/xsl', ''))

    def to_json(self):
        json_data = dict((attr, getattr(self, attr))
                            for attr in ('name', 'match', 'mode', 'priotity', 'i_priority')
                                if getattr(self, attr, None) is not None)
        json_data['stylesheet'] = self.stylesheet.path
        return json_data


def compare_import_priorities(priority1, priority2):
    l1 = len(priority1)
    l2 = len(priority2)

    if l1 != l2:
        return 1 if l1 < l2 else -1

    for index in xrange(l1):
        if priority1[index] != priority2[index]:
            return 1 if priority1[index] < priority2[index] else -1
    return 0