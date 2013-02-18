# -*- coding: utf-8 -*-

import pickle
import config


def pickle_data_and_index(data, index):
    with open(config.PICKLE_NAME, 'w') as f:
        pickle.dump((data, index), f)


def get_data_index_from_pickle():
    with open(config.PICKLE_NAME) as f:
        return pickle.load(f)