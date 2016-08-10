# -*- coding: utf-8 -*-

import os
import pickle
import config

if not os.path.exists(config.PICKLE_DIR):
    os.makedirs(config.PICKLE_DIR)


def pickle_data_and_index(data, index):
    with open(config.PICKLE_NAME, 'w') as f:
        pickle.dump((data, index), f)


def get_data_index_from_pickle():
    if not os.path.isdir(config.PICKLE_DIR):
        os.mkdir(config.PICKLE_DIR)

    with open(config.PICKLE_NAME) as f:
        return pickle.load(f)