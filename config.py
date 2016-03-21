# -*- coding: utf-8 -*-

import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


PORT = 8888
ROOT_XHH_DIR = '/home/apertsev/workspace/hh.sites.main/xhh'
ROOT_XSL_DIR = ROOT_XHH_DIR + '/xsl'
RESULTS_DIR = 'results'
PICKLE_DIR = 'pickled'
PICKLE_NAME = PICKLE_DIR + '/xsl_data.pckl'
