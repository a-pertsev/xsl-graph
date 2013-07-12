# -*- coding: utf-8 -*-

import os
import subprocess

from itertools import chain
from collections import defaultdict
from operator import itemgetter
from copy import deepcopy


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


    imports = xsl_data.get('imports', None)
    if imports is None:
        return data_dict

    for xsl_import in imports:
        imported_data = extend_one_file_templates(xsl_import, data_dict)




def get_all_file_imports(name, data_dict):
    single_file_data = data_dict.get(name, {})
    keys = single_file_data.get('imports', [])
    return keys + list(chain.from_iterable(get_all_file_imports(import_name, data_dict) for import_name in single_file_data.get('imports', [])))


def get_duplicated_imports(data_dict):
    result = defaultdict(dict)
    for file_name in data_dict:
        temp = defaultdict(int)
        for imported_file in get_all_file_imports(file_name, data_dict):
            temp[imported_file] += 1
            if temp[imported_file] > 4:
                result[file_name][imported_file] = temp[imported_file]
    return result


def analyze_modes_usage(data_dict):
    result = defaultdict(int)

    for file_name in data_dict:
        for mode in data_dict[file_name].get('applied_modes'):
            result[mode] += 1

    result = sorted(result.iteritems(), key=itemgetter(1))
    return result


def get_not_used_xsls(data, index):
        data = deepcopy(data)

        del data['/home/apertsev/workspace/hh.sites.main/xhh/xsl/hh-precompile.xsl']

        res = [f for f in data if f not in index]
        res = map(lambda path: os.path.relpath(path, '/home/apertsev/workspace/hh.sites.main/xhh/xsl').split('/', 1)[-1], res)

        os.chdir('/home/apertsev/workspace/hh.sites.main')

        empty = []

        for xsl in sorted(list(set(res))):
            try:
                subprocess.check_output(['fgrep', '-R', '--exclude-dir=\.git', '--exclude-dir=\.idea', xsl, '.'])
            except:
                empty.append(xsl)

        return empty