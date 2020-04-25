#!/usr/bin/env python3

import draw.table
import draw.array
import draw.graph

class Algviz():
    def __init__(self):
        self._next_display_id = 0
        self._animate_delay = 3.0
        self._color_list = [
            (211, 211, 211), # LightGray
            (245, 222, 179), # Wheat
            (255, 182, 193), # LightPink
            (202, 255, 112), # DarkOliveGreen
            (221, 160, 221), # Plum
            (176, 226, 255), # LightSkyBlue
            (144, 238, 144), # LightGreen
            (255, 193, 37),  # Goldenrod
        ]

    '''
    row:表格行数；col:表格列数。
    返回：创建的表格对象。
    '''
    def create_table(row, col, data=None, cell_size=50):
        pass

    '''
    bar:是否以柱状图的形式显示数组。
    返回：创建的数组对象。
    '''
    def create_array(bar=False):
        pass

    '''
    返回：创建的列表对象。
    '''
    def create_list():
        pass

    '''
    返回：创建的二叉树对象。
    '''
    def create_binary_tree():
        pass

    '''
    返回：创建的拓扑图对象。
    '''
    def create_graph():
        pass

    '''
    table:trace将要绑定的table对象。
    hold:是否需要在表格中显示trace经过的路径。
    r,c:初始位置的行列坐标。
    '''
    def create_table_trace(table, hold=False, r=0, c=0)
        pass
