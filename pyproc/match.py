# -*- coding: utf-8 -*-

import string


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

def parse_match_string(match_string):
    location_path_patterns = map(string.strip, clean_from_predicates(match_string).split('|'))
    return location_path_patterns



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



class Match(object):
    def __init__(self, match_string, context=None):
        self.string = match_string
        self.match_nodes = parse_match_string(match_string)
        self.context = context

    def __get__(self):
        return self.string

    def __repr__(self):
        return self.string

    def __add__(self, other):
        left_part = self.string if self.string != '/' else ''
        union = '/' if not other.string.startswith('//') else ''
        return left_part + union + other.string

    def __eq__(self, other_string):
        pass