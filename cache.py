# -*- coding: utf-8 -*-

from itertools import imap

import config


class DataCacher(object):
    __data = {}
    __index = {}
    __file_names = []

    def get_data(self):
        return self.__data

    def get_index(self):
        return self.__index

    def set_data(self):
        raise TypeError('data does not support item assignment')

    def set_index(self):
        raise TypeError('index does not support item assignment')

    def get_file_names(self):
        return self.__file_names

    def set_file_names(self):
        raise TypeError('file_names does not support item assignment')

    data = property(get_data, set_data)
    index = property(get_index, set_index)
    file_names = property(get_file_names, set_file_names)



    def invalidate(self, data, index):
        self.__data = data
        self.__index = index

        self.__file_names = map(lambda file: file.replace(config.ROOT_DIR, '').lstrip('/'), self.__data.iterkeys())




