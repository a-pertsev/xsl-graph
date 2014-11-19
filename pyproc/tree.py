# -*- coding: utf-8 -*-

from pyproc.templates import CallTemplate, compare_import_priorities


#class TreeNode(object):
#    def __init__(self, template, parent):
#        self.template = template
#        self.parent = parent
#        self.children = []
#
#
#def build_result_tree(root_node, modes, templates):
#    root_node = TreeNode(root_node, None)
#
#    result = []
#
#    for apply_template in template.external_links:
#        if isinstance(apply_template, CallTemplate):
#            continue
#
#        mode_equal_nodes = self.modes.get(apply_template.mode)
#        if not mode_equal_nodes:
#            print 'O_O', template, apply_template
#            continue
#
#        children = []
#
#        for template_looks_similar in mode_equal_nodes:
#            if template_looks_similar.match not in apply_template.select:
#                continue
#
#            if children:
#                compare_result = compare_import_priorities(children[0][0].i_priority, template_looks_similar.i_priority)
#                if compare_result > 0:
#                    continue
#                elif compare_result < 0:
#                    children = []
#
#            children.append((template_looks_similar, apply_template))
#
#        result.extend(children)
#
#
#    return None





class TemplateNode(object):
    def __init__(self, template, apply_template, parent, children=[]):
        self.parent = parent
        self.apply_template = apply_template
        self.template = template
        self.children = children



class ResultTree(object):
    def __init__(self, root_template, modes, templates):
        self.modes = modes
        self.templates = templates

        self.root_node = self.build_tree(root_template, parent=None, apply_template=None)


    def build_tree(self, template, parent, apply_template):

        tree_node = TemplateNode(template, parent, apply_template)

        children = self.find_children(template)

        tree_node.children.extend(self.build_tree(child, tree_node, apply_template) for child, apply_template in children)

        print template, tree_node, tree_node.children

        return tree_node



    def find_children(self, template):
        result = []

        for apply_template in template.external_links:
            if isinstance(apply_template, CallTemplate):
                continue

            mode_equal_nodes = self.modes.get(apply_template.mode)

            if not mode_equal_nodes:
                print 'no applieable templates', template, apply_template
                continue

            children = [template_looks_similar
                            for template_looks_similar in mode_equal_nodes
                                if template_looks_similar.match in apply_template.select]

            children.sort(cmp=sort_by_priority)

            print children

        return result

def sort_by_priority(template1, template2):
    return compare_import_priorities(template1.i_priority, template2.i_priority)