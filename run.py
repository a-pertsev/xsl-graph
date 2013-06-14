# -*- coding: utf-8 -*-

import config

from pyxsl.parse import get_data_and_index
from pyxsl.draw import complete_search, draw_outside, draw_inside
from pyxsl.pick import pickle_data_and_index, get_data_index_from_pickle



if __name__ == "__main__":
    '''
       Usage examples:
         data, index = get_data_and_index(start_dir=config.ROOT_DIR)
         pickle_data_and_index(data, index)
         data, index = get_data_index_from_pickle()

         draw_outside(index, files_to_search, draw_dir=config.ROOT_DIR)
         draw_inside(data, draw_dir=config.ROOT_DIR)
    '''

    data, index = get_data_and_index(start_dir=config.ROOT_DIR)
    pickle_data_and_index(data, index)
#    data, index = get_data_index_from_pickle()



    draw_inside(data,
                draw_dir=config.ROOT_DIR + '/hh/catalog',
    )


    draw_outside(index,
                 draw_dir=config.ROOT_DIR + '/hh/catalog'
                 search_files=[config.ROOT_DIR + '/hh/blocks/searchresult/search-vacancy-result-oldstyle.xsl'],
    )


