# -*- coding: utf-8 -*-

import os
import simplejson


XSL_NS = '{http://www.w3.org/1999/XSL/Transform}'
XSL_NS_TEXT = 'http://www.w3.org/1999/XSL/Transform'
FUNC_NS = 'http://exslt.org/functions'


def is_xsl_tag(element, tag_name):
    return element.tag == '{0}{1}'.format(XSL_NS, tag_name)

def get_xsls_in_dir(dirname):
    return [os.path.join(dir_name,file) for dir_name,_,files in os.walk(dirname) for file in files if 'xsl' in file]

def require(require_f):
    def inner_decorator(func):
        def wrapped_func(self, *args, **kwargs):
            if not hasattr(self, '__inited'):
                self.__inited = []

            if require_f not in self.__inited:
                self.__inited.append(require_f)
                require_f(self)

            return func(self, *args, **kwargs)
        return wrapped_func
    return inner_decorator



class JSONEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if hasattr(o, '__to_json'):
            return o.__to_json()

        return simplejson.JSONEncoder.default(self, o)

