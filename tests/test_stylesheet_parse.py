# -*- coding: utf-8 -*-

import os.path
import unittest

from pyproc.match import Match, Select, clean_from_predicates, split_predicates, select_nodes_in_match_nodes, \
                         BadLocation, split_and_simplify_xpath, ANY_NUMBER_OF_NODES, ROOT_NODE

from pyproc.stylesheet import Stylesheet

from pyproc.analyze import get_not_used_templates
from pyproc.templates import compare_import_priorities


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
        self.assertEqual(compare_import_priorities([1, 2, 0, 0], [1, 2, 0]), -1)


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


    def test_clean_matches(self):
        select = Select('.[@="1"] | node', context=Match('doc | notDoc'))
        self.assertEqual(set(select.match_nodes), set(['doc', 'notDoc', 'doc/node', 'notDoc/node']))

        select = Select('.[@="1"]', context=Match("doc[current()=.]/key | notDoc"))
        self.assertEqual(select.match_nodes, ['doc/key', 'notDoc'])

        select = Select('current()', context=Match("/doc"))
        self.assertEqual(select.match_nodes, ['/doc'])

        select = Select('node', context=Match("/doc"))
        self.assertEqual(select.match_nodes, ['/doc/node'])


    def test_split_xpath(self):
        self.assertEqual(split_and_simplify_xpath('/'), [ROOT_NODE])
        self.assertEqual(split_and_simplify_xpath('//'), [ANY_NUMBER_OF_NODES])
        self.assertEqual(split_and_simplify_xpath('/doc/hoho'), [ROOT_NODE, 'doc', 'hoho'])
        self.assertEqual(split_and_simplify_xpath('//doc'), [ANY_NUMBER_OF_NODES, 'doc'])
        self.assertEqual(split_and_simplify_xpath('//doc/node//subnode'),
                        [ANY_NUMBER_OF_NODES, 'doc', 'node', ANY_NUMBER_OF_NODES, 'subnode'])
        self.assertEqual(split_and_simplify_xpath('..//doc'), ['..', ANY_NUMBER_OF_NODES, 'doc'])


    def test_select_overlay_match(self):
        def assert_overlay(match1, match2):
            self.assertTrue(select_nodes_in_match_nodes(Select(match1).parsed_match_nodes[0], Match(match2).parsed_match_nodes[0]), (Select(match1).parsed_match_nodes[0], Match(match2).parsed_match_nodes[0]))

        def assert_not_overlay(match1, match2):
            self.assertFalse(select_nodes_in_match_nodes(Select(match1).parsed_match_nodes[0], Match(match2).parsed_match_nodes[0]), (Select(match1).parsed_match_nodes[0], Match(match2).parsed_match_nodes[0]))

        assert_overlay('*', '*')
        assert_overlay('doc', 'doc')
        assert_overlay('doc', '*')
        assert_overlay('doc/node', '*/node')
        assert_overlay('/doc/node', '/*/node')
        assert_overlay('doc/select/*', 'select/*')
        assert_overlay('doc/select/node', '*')
        assert_overlay('//node', 'node')
        assert_overlay('//node', '*')
        assert_overlay('node', '*//node')
        assert_overlay('doc', '//doc')
        assert_overlay('node//doc', 'node//doc')

        assert_not_overlay('*', 'doc')
        assert_not_overlay('node/*', 'node/doc')
        assert_not_overlay('node/*/doc', 'node/somenode/doc')
        assert_not_overlay('node//doc', 'node/somenode/doc')

    def test_matches_equal(self):
        def assert_matches_equal(m1, m2):
            match1 = Match(m1)
            match2 = Match(m2)
            self.assertTrue(match1 == match2, '{0} != {1}'.format(match1.parsed_match_nodes, match2.parsed_match_nodes))

        assert_matches_equal('doc', 'doc')
        assert_matches_equal('doc', 'doc2')


