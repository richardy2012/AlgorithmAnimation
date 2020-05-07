#!/usr/bin/env python3

import weakref
import time
from IPython import display
import table
import vector
import graph

class _NoDisplay():
    def _repr_svg_(self):
        return ''

class Visualizer():
    
    def __init__(self):
        self._next_display_id = 0
        self._animate_delay = 3.0
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
        self._displayed = set()    # 记录已经被显示的id，若id未被显示，调用display接口，否则调用update接口。

    '''
    val:float 设置动画延时时长。
    '''
    def setAnimateDelay(self, val):
        self._animate_delay = val
        
    '''
    功能：刷新所有已创建的显示对象。
    '''
    def refresh(self):
        for elem in self._element2display.keyrefs():
            did = self._element2display[elem()]
            if did not in self._displayed:
                display.display(elem(), display_id='algviz{}'.format(did))
                self._displayed.add(did)
            else:
                display.update_display(elem(), display_id='algviz{}'.format(did))
        temp_displayed = list(self._displayed)
        for did in temp_displayed:
            if did not in self._element2display.values():
                display.update_display(_NoDisplay() ,display_id='algviz_{}'.format(did))
                display.update_display(_NoDisplay() ,display_id='algviz{}'.format(did))
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
        tab = table.Table(row, col, data, cell_size, name)
        self._element2display[tab] = self._next_display_id
        self._next_display_id += 1
        return tab

    '''
    data:list(...) 向量中初始化的数据。
    cell_size:float 向量中单元格的长宽尺寸。
    name:str 表格的名字。
    返回：创建的向量对象。
    '''
    def createVector(self, data, cell_size=50, name=None):
        vec = vector.Vector(data, self._animate_delay, cell_size, name)
        self._element2display[vec] = self._next_display_id
        self._next_display_id += 1
        return vec

    '''
    返回：创建的单向列表对象。
    '''
    def createForwardList(self):
        pass
    
    '''
    返回：创建的双向列表对象。
    '''
    def createDoubleList(self):
        pass

    '''
    返回：创建的二叉树对象。
    '''
    def createBinaryTree(self):
        pass

    '''
    返回：创建的拓扑图对象。
    '''
    def createGraph(self):
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
