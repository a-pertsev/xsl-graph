# -*- coding: utf-8 -*-



class DataCacher(object):
    __data = {}
    __index = {}

    def get_data(self):
        return self.__data

    def get_index(self):
        return self.__index

    def set_data(self):
        raise TypeError('data does not support item assignment')

    def set_index(self):
        raise TypeError('index does not support item assignment')

    data = property(get_data, set_data)
    index = property(get_index, set_index)


    def invalidate(self, data, index):
        self.__data = data
        self.__index = index



