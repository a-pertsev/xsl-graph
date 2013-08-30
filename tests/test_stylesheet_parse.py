# -*- coding: utf-8 -*-

import os.path
import unittest

from pyproc.match import clean_from_predicates, split_predicates, parse_match_string, BadLocation
from pyproc.match import Match
from pyproc.stylesheet import Stylesheet

from pyproc.analyze import get_not_used_templates, compare_import_priorities


XSL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'xsl'))


def get_xsl_path(name):
    return os.path.join(XSL_DIR, name)

class TestStyleSheetParsing(unittest.TestCase):
    def test_includes(self):
        templates = Stylesheet(get_xsl_path('include_test/1.xsl')).templates
        matches = map(lambda template: template.match.string, templates)
        self.assertEqual(matches, ['some_node_from_2', 'some_node_from_3', '/'])


class TestStylesheetAnalyze(unittest.TestCase):
    @unittest.skip
    def test_not_used_templates(self):
        ss = Stylesheet(get_xsl_path('template_modes_test/1.xsl'))
        not_used_templates = get_not_used_templates(ss)
        self.assertEqual(len(not_used_templates), 3)

    def test_import_priorities_compare(self):
        self.assertEqual(compare_import_priorities([0], [0]), 0)
        self.assertEqual(compare_import_priorities([2], [0]), -1)
        self.assertEqual(compare_import_priorities([0, 1], [0]), -1)
        self.assertEqual(compare_import_priorities([0, 1], [0, 1]), 0)
        self.assertEqual(compare_import_priorities([0], [0, 1]), 1)
        self.assertEqual(compare_import_priorities([0, 1, 1], [0, 1, 1]), 0)
        self.assertEqual(compare_import_priorities([0], [1]), 1)
        self.assertEqual(compare_import_priorities([0], [1000]), 1)
        self.assertEqual(compare_import_priorities([0, 0, 0, 1], [0, 0, 0, 2]), 1)


class TestMatches(unittest.TestCase):
    def test_predicates(self):
        self.assertEqual(split_predicates('*'), ('*', None))
        self.assertEqual(split_predicates('*/*'), ('*/*', None))
        self.assertEqual(split_predicates('//*/*'), ('//*/*', None))
        self.assertEqual(split_predicates('@*'), ('@*', None))
        self.assertEqual(split_predicates('*[]'), ('*', '[]'))
        self.assertEqual(split_predicates('*[node()]'), ('*', '[node()]'))
        self.assertEqual(split_predicates('*[/doc/vacancy]'), ('*', '[/doc/vacancy]'))
        self.assertEqual(split_predicates('*[/doc/vacancy]["1"]'), ('*', '[/doc/vacancy]["1"]'))
        self.assertEqual(split_predicates('*[/doc/vacancy[@id]]'), ('*', '[/doc/vacancy[@id]]'))

        with self.assertRaises(BadLocation) as cm:
            split_predicates('')


    @unittest.skip
    def test_match_sum(self):
        self.assertEqual(Match('/') + Select('//item'), '//item')
        self.assertEqual(Match('/item1') + Select('//item'), '/item1//item')
        self.assertEqual(Match('/item1') + Select('/item'), '/item')
        self.assertEqual(Match('*') + Select('/item'), '/item')
        self.assertEqual(Match('*') + Select('item'), '*/item')
        self.assertEqual(Match('*') + Select('item'), '?/item')
        self.assertEqual(Match('//item') + Select('item1'), 'item/item1')
        self.assertEqual(Match('//item/sometag') + Select('item1'), 'item/sometag/item1')


    def test_predicates_cleaning(self):
        self.assertEqual(clean_from_predicates('*'), '*')
        self.assertEqual(clean_from_predicates('*/*'), '*/*')
        self.assertEqual(clean_from_predicates('//*/*'), '//*/*')
        self.assertEqual(clean_from_predicates('@*'), '@*')
        self.assertEqual(clean_from_predicates('*[]'), '*')
        self.assertEqual(clean_from_predicates('*[node()]'), '*')
        self.assertEqual(clean_from_predicates('*[/doc/vacancy]'), '*')
        self.assertEqual(clean_from_predicates('*[/doc/vacancy]["1"]'), '*')
        self.assertEqual(clean_from_predicates('*[/doc/vacancy[@id]]'), '*')
        self.assertEqual(clean_from_predicates('*[/doc/vacancy[@id]]/node[@id2]'), '*/node')
        self.assertEqual(clean_from_predicates('//*[/doc/vacancy[@id]]/node[@id2/id3]/some'), '//*/node/some')
        self.assertEqual(clean_from_predicates('*[node1 | node2]'), '*')
        self.assertEqual(clean_from_predicates('*[node1|node2]|node3'), '*|node3')

    def test_parsing_match_string(self):
        self.assertEqual(parse_match_string('* | key()'), ['*', 'key()'])
        self.assertEqual(parse_match_string('*|node'), ['*', 'node'])
        self.assertEqual(parse_match_string('*[sim]|node1|node2'), ['*', 'node1', 'node2'])
        self.assertEqual(parse_match_string('*[sim]|node1[a | b]|node2'), ['*', 'node1', 'node2'])
