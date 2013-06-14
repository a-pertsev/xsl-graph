#!/usr/bin/python
# -*- coding: utf-8 -*-

import config

from functools import partial
from optparse import OptionParser, OptionConflictError

from pyxsl.parse import get_data_and_index
from pyxsl.draw import complete_search, draw_outside, draw_inside
from pyxsl.pick import pickle_data_and_index, get_data_index_from_pickle



if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--inside",  action="store_true", dest="i", help="draw inside")
    parser.add_option("-o", "--outside", action="store_true", dest="o", help="draw inside")
    parser.add_option("-c", "--complex", action="store_true", dest="c", help="draw inside and outside")

    parser.add_option("-f", "--file", action="append", dest="files", help="files to analyze")
    parser.add_option("-d", "--dir", action="store", dest="dir", help="directory to analyze")
    parser.add_option("-p", "--pickle", action="store_true", dest="use_pickle", help="use")


    (options, args) = parser.parse_args()

    if options.use_pickle:
        data, index = get_data_index_from_pickle()
    else:
        data, index = get_data_and_index(start_dir=config.ROOT_DIR)
        pickle_data_and_index(data, index)

    if options.c:
        complete_search(data, index, options.files, options.dir)
    if options.i:
        draw_inside(data, options.files, options.dir)
    if options.o:
        draw_outside(index, options.files, options.dir)

