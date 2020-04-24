#!/usr/bin/env python3

import draw.table
import draw.array
import draw.graph

COLOR_LIST = []
NEXT_DISPLAY_ID = 0
ANIMATE_DELAY = 3.0

'''
row:表格行数；col:表格列数。
返回：创建的表格对象。
'''
def create_table(row, col):
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
'''
def create_table_trace(table, hold=False)
    pass
