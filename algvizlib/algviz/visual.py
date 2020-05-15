#!/usr/bin/env python3

import weakref
import time
from IPython import display

import table
import vector
import graph
import tree
import link_list
import svg_graph
import svg_table

class _NoDisplay():
    def _repr_svg_(self):
        return ''

class Visualizer():
    
    '''
    delay:float 延时时间长度。
    '''
    def __init__(self, delay = 3.0):
        self._next_display_id = 0
        self._animate_delay = delay
        self._trace_color_list = [
            (211, 211, 211), # LightGray
            (245, 222, 179), # Wheat
            (255, 182, 193), # LightPink
            (202, 255, 112), # DarkOliveGreen
            (221, 160, 221), # Plum
            (176, 226, 255), # LightSkyBlue
            (144, 238, 144), # LightGreen
            (255, 193, 37),  # Goldenrod
        ]
        self._element2display = weakref.WeakKeyDictionary() # 显示对象到显示id的映射关系。
        self._displayed = set()        # 记录已经被显示的id，若id未被显示，调用display接口，否则调用update接口。
        self._displayid2name = dict()  # 记录对象显示id和对象名称之间的映射关系。
        
    '''
    功能：刷新所有已创建的显示对象。
    '''
    def refresh(self):
        for elem in self._element2display.keyrefs():
            did = self._element2display[elem()]
            if did not in self._displayed:
                if did in self._displayid2name:
                    svg_title = svg_table.SvgTable(200, 20)
                    svg_title.add_text_element((3, 16), '{}:'.format(self._displayid2name[did]), font_size=16, fill=(0,0,0))
                    display.display(svg_title, display_id='algviz_{}'.format(did))
                display.display(elem(), display_id='algviz{}'.format(did))
                self._displayed.add(did)
            else:
                display.update_display(elem(), display_id='algviz{}'.format(did))
        temp_displayed = list(self._displayed)
        for did in temp_displayed:
            if did not in self._element2display.values():
                if did in self._displayid2name:
                    display.update_display(_NoDisplay(), display_id='algviz_{}'.format(did))
                display.update_display(_NoDisplay(), display_id='algviz{}'.format(did))
                self._displayed.remove(did)
        time.sleep(self._animate_delay)
        
    '''
    row:int 表格行数；col:int 表格列数。
    data:list(...) 表格中初始化的数据。
    cell_size:float 表格中单元格的长宽尺寸。
    name:str 表格的名字。
    返回：创建的表格对象。
    '''
    def createTable(self, row, col, data=None, cell_size=40, name=None):
        tab = table.Table(row, col, data, cell_size)
        self._element2display[tab] = self._next_display_id
        if name is not None:
            self._displayid2name[self._next_display_id]=name
        self._next_display_id += 1
        return tab

    '''
    data:list(...) 向量中初始化的数据。
    cell_size:float 向量中单元格的长宽尺寸。
    name:str 表格的名字。
    返回：创建的向量对象。
    '''
    def createVector(self, data, cell_size=50, name=None):
        vec = vector.Vector(data, self._animate_delay, cell_size)
        self._element2display[vec] = self._next_display_id
        if name is not None:
            self._displayid2name[self._next_display_id]=name
        self._next_display_id += 1
        return vec

    '''
    返回：创建的拓扑图可视化对象。
    '''
    def createGraph(self, directed=True, horizontal=False, data=None):
        pass
    
    '''
    返回：创建的单向列表跟踪器对象。
    '''
    def createForwardListTrace(self):
        pass

    '''
    返回：创建的二叉树跟踪器对象。
    '''
    def createBinaryTreeTrace(self):
        pass

    '''
    返回：创建的拓扑图跟踪器对象。
    '''
    def createGraphTrace(self):
        pass

    '''
    table:Table trace将要绑定的table对象。
    hold:bool 是否需要在表格中显示trace经过的路径。
    r,c:int 初始位置的行列坐标。
    返回：TableTrace 跟踪器。
    '''
    def createTableTrace(self, tab, hold=False, r=0, c=0):
        if len(tab._trace_color) >= len(self._trace_color_list):
            raise Exception('Too many traces in table!')
        else:
            pick_color = None
            for i in range(len(self._trace_color_list)):
                pick_color = self._trace_color_list[i]
                if pick_color not in tab._trace_color:
                    break
            tab._trace_color.add(pick_color)
            trace = table.TableTrace(tab, pick_color, hold, r, c)
            return trace

    '''
    vec:Vector trace将要绑定的vector对象。
    hold:bool 是否需要在向量中显示trace经过的路径。
    i:int 跟踪器初始索引位置。
    '''
    def createVectorTrace(self, vec, hold=False, i=0):
        if len(vec._trace_color) >= len(self._trace_color_list):
            raise Exception('Too many traces in vector!')
        else:
            pick_color = None
            for i in range(len(self._trace_color_list)):
                pick_color = self._trace_color_list[i]
                if pick_color not in vec._trace_color:
                    break
            vec._trace_color.add(pick_color)
            trace = vector.VectorTrace(vec, pick_color, hold, i)
            return trace
