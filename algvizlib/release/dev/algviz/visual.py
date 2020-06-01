#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

import weakref
import time
from IPython import display

from . import table
from . import vector
from . import graph
from . import tree
from . import link_list
from . import svg_graph
from . import svg_table
from . import utility
from . import logger

class _NoDisplay():
    def _repr_svg_(self):
        return ''

_next_display_id = 0
    
class Visualizer(): 
    '''
    delay:float 延时时间长度。
    wait:bool 是否等待按键输入后继续代码。
    '''
    def __init__(self, delay=3.0, wait=False):
        self._delay = 3.0         # 动画延时时长。
        if delay > 0:
            self._delay = delay
        self._wait = wait         # 每帧刷新后是否等待。
        self._element2display = weakref.WeakKeyDictionary() # 显示对象到显示id的映射关系。
        self._displayed = set()        # 记录已经被显示的id，若id未被显示，调用display接口，否则调用update接口。
        self._displayid2name = dict()  # 记录对象显示id和对象名称之间的映射关系。
        
    '''
    功能：刷新所有已创建的显示对象。
    delay:float 刷新时的动画延迟。
    '''
    def display(self, delay=None):
        if delay == None:
            delay = self._delay
        if self._wait == False:
            for elem in self._element2display.keyrefs():
                did = self._element2display[elem()]
                if did not in self._displayed:
                    if did in self._displayid2name:
                        svg_title = svg_table.SvgTable(400, 17)
                        title_name = '{}:'.format(self._displayid2name[did])
                        svg_title.add_text_element((4, 14), title_name, font_size=14, fill=(0,0,0))
                        display.display(svg_title, display_id='algviz_{}'.format(did))
                    elem()._delay = delay
                    display.display(elem(), display_id='algviz{}'.format(did))
                    self._displayed.add(did)
                else:
                    if did in self._displayid2name:
                        svg_title = svg_table.SvgTable(400, 17)
                        title_name = '{}:'.format(self._displayid2name[did])
                        svg_title.add_text_element((4, 14), title_name, font_size=14, fill=(0,0,0))
                        display.update_display(svg_title, display_id='algviz_{}'.format(did))
                    elem()._delay = delay
                    display.update_display(elem(), display_id='algviz{}'.format(did))
            temp_displayed = list(self._displayed)
            for did in temp_displayed:
                if did not in self._element2display.values():
                    if did in self._displayid2name:
                        display.update_display(_NoDisplay(), display_id='algviz_{}'.format(did))
                    display.update_display(_NoDisplay(), display_id='algviz{}'.format(did))
                    self._displayed.remove(did)
            time.sleep(delay)
            return None
        else:
            display.clear_output(wait=True)
            for elem in self._element2display.keyrefs():
                did = self._element2display[elem()]
                if did in self._displayid2name:
                    svg_title = svg_table.SvgTable(400, 17)
                    title_name = '{}:'.format(self._displayid2name[did])
                    svg_title.add_text_element((4, 14), title_name, font_size=14, fill=(0,0,0))
                    display.display(svg_title, display_id='algviz_{}'.format(did))
                elem()._delay = delay
                display.display(elem(), display_id='algviz{}'.format(did))
                self._displayed.add(did)
            return input('回车键继续：')
        
    '''
    row:int 表格行数；col:int 表格列数。
    data:list(...) 表格中初始化的数据。
    name:str 表格的名字。
    cell_size:float 表格中单元格的长宽尺寸。
    show_index:bool 是否显示表格行列标签。
    返回：创建的表格对象。
    '''
    def createTable(self, row, col, data=None, name=None, cell_size=40, show_index=True):
        global _next_display_id
        tab = table.Table(row, col, data, cell_size, show_index)
        self._element2display[tab] = _next_display_id
        if name is not None:
            self._displayid2name[_next_display_id] = name
        _next_display_id += 1
        return tab

    '''
    data:list(...) 向量中初始化的数据。
    name:str 表格的名字。
    cell_size:float 向量中单元格的长宽尺寸。
    bar:float 如果bar值小于零则忽略，否则以柱状图形式显示数据。
    show_index:bool 是否显示向量下标索引标签。
    返回：创建的向量对象。
    '''
    def createVector(self, data=None, name=None, cell_size=40, bar=-1, show_index=True):
        global _next_display_id
        vec = vector.Vector(data, self._delay, cell_size, bar, show_index)
        self._element2display[vec] = _next_display_id
        if name is not None:
            self._displayid2name[_next_display_id] = name
        _next_display_id += 1
        return vec

    '''
    data:... 拓扑图的初始化数据。
    name:str 拓扑图的显示名称。
    directed:bool 是否为有向图。
    horizontal:bool 图是否横向排版。
    返回：创建的拓扑图可视化对象。
    '''
    def createGraph(self, data=None, name=None, directed=True, horizontal=True):
        global _next_display_id
        gra = svg_graph.SvgGraph(data, directed, self._delay, horizontal)
        self._element2display[gra] = _next_display_id
        if name is not None:
            self._displayid2name[_next_display_id] = name
        _next_display_id += 1
        return gra

    '''
    buffer_lines:int 记录器最大缓存行数。
    '''
    def createLogger(self, buffer_lines=10, name=None):
        global _next_display_id
        logg = logger.Logger(buffer_lines)
        self._element2display[logg] = _next_display_id
        if name is not None:
            self._displayid2name[_next_display_id] = name
        _next_display_id += 1
        return logg
