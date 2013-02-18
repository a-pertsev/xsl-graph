# -*- coding: utf-8 -*-

from itertools import chain
from collections import defaultdict


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




def get_all_imports(name, data_dict):
    single_file_data = data_dict.get(name, {})
    keys = single_file_data.get('keys', [])
    return keys + list(chain.from_iterable(get_all_imports(import_name, data_dict) for import_name in single_file_data.get('imports', [])))


def analyze_keys(data_dict):
    result_keys = defaultdict(list)
    for file_name in data_dict:
        result_keys[file_name] = get_all_imports(file_name, data_dict)

    print sorted(result_keys.iteritems(), key=lambda x: len(x[1]))[-1:][0]
