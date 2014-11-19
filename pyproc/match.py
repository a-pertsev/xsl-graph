# -*- coding: utf-8 -*-

import string
from itertools import imap

CURRENT_NODE_SHORTCUT = '.'
ANY_NODE_SHORTCUT = '*'
ANY_NUMBER_OF_NODES_SHORTCUT = '//'
ROOT_NODE_SHORTCUT = '/'
ROOT_NODE = 'ROOT_NODE'
CURRENT_NODE_EXPRESSION = 'current()'
ANY_NUMBER_OF_NODES = 'ANY_NUMBER_OF_NODES'

class BadLocation(Exception):
    pass


def clean_from_predicates(location_path):
    clean_location = ''
    predicates_depth = 0

    for ch in location_path:
        if ch == '[':
            predicates_depth += 1
        else:
            if predicates_depth == 0:
                clean_location += ch
            if ch == ']':
                predicates_depth -= 1

    return clean_location


def parse_match_string(match_string, context=None):
    location_path_patterns = map(string.strip, clean_from_predicates(match_string).split('|'))
    if context is not None:
        location_path_patterns = clean_matches(location_path_patterns, context)
    return location_path_patterns


def clean_matches(match_strings, context):
    matches = []
    current_nodes = context.match_nodes
    for current_node in current_nodes:
        for match_string in match_strings:
            if match_string.startswith(CURRENT_NODE_EXPRESSION):
                match_string = match_string.replace(CURRENT_NODE_EXPRESSION, current_node)
            elif match_string.startswith(CURRENT_NODE_SHORTCUT):
                match_string = match_string.replace(CURRENT_NODE_SHORTCUT, current_node)
            else:
                match_string = '{0}/{1}'.format(current_node, match_string)
            matches.append(match_string)

    return matches


def split_predicates(location_path_pattern):
    if not location_path_pattern:
        raise BadLocation(location_path_pattern)

    if '[' in location_path_pattern:
        predicate_index = location_path_pattern.index('[')
        location = location_path_pattern[:predicate_index]
        predicates = location_path_pattern[predicate_index:]
    else:
        location = location_path_pattern
        predicates = None

    return location, predicates


def split_and_simplify_xpath(xpath):
    """Terrible algorithm"""""

    if not xpath.startswith(ANY_NUMBER_OF_NODES_SHORTCUT) and xpath.startswith(ROOT_NODE_SHORTCUT):
        xpath = xpath.replace(ROOT_NODE_SHORTCUT, '{0}/'.format(ROOT_NODE), 1)
    if xpath.startswith(ANY_NUMBER_OF_NODES_SHORTCUT):
        xpath = xpath.replace(ANY_NUMBER_OF_NODES_SHORTCUT, '{0}/'.format(ANY_NUMBER_OF_NODES), 1)

    return filter(None, xpath.replace(ANY_NUMBER_OF_NODES_SHORTCUT, '/{0}/'.format(ANY_NUMBER_OF_NODES)).split('/'))


def select_nodes_in_match_nodes(select_nodes, match_nodes):
    select_nodes = select_nodes[:]
    match_nodes = match_nodes[:]

    while match_nodes:
        match = match_nodes.pop()

        if not select_nodes:
            return True

        select = select_nodes.pop()

        if match == select:
            continue

        if select == ANY_NUMBER_OF_NODES:
            return False

        if match == '*':
            continue

        return False

    return True

def select_overlay_match(select_match, match_match):
    return [select_parsed_node for
                select_parsed_node in select_match.parsed_match_nodes
                    for match_parsed_node in match_match.parsed_match_nodes
                        if select_nodes_in_match_nodes(select_parsed_node, match_parsed_node)]


def check_match_nodes_eqal(match_node1, match_node2):
    return match_node1.parsed_match_nodes == match_node2.parsed_match_nodes


class Match(object):
    def __init__(self, match_string, context=None):
        self.context = context
        self.string = match_string
        self.match_nodes = parse_match_string(match_string, context)
        self.parsed_match_nodes = map(split_and_simplify_xpath, self.match_nodes)

    def __get__(self):
        return self.string

    def __repr__(self):
        return self.string

    def __add__(self, other):
        left_part = self.string if self.string != '/' else ''
        union = '/' if not other.string.startswith('//') else ''
        return left_part + union + other.string

    def __eq__(self, other_match):
        #TODO: fix match system, is match have many match_nodes, but only 1 match/select equals,
        #      and match should use only 1 node inside
        #      Get_match_intercept mb ?
        return check_match_nodes_eqal(self, other_match)

class Select(Match):
    def __contains__(self, match):
        return select_overlay_match(self, match)