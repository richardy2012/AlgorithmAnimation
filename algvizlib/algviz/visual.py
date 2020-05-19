#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

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
import utility

class _NoDisplay():
    def _repr_svg_(self):
        return ''

next_display_id = 0
    
class Visualizer():
        
    '''
    delay:float 延时时间长度。
    waitkey:bool 是否等待按键输入后继续代码。
    '''
    def __init__(self, delay=3.0, waitkey=False):
        self._animate_delay = 3.0
        if delay > 0:    #对输入数据的范围进行检测。
            self._animate_delay = delay
        self._waitkey = waitkey
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
        if self._waitkey == False:
            for elem in self._element2display.keyrefs():
                did = self._element2display[elem()]
                if did not in self._displayed:
                    if did in self._displayid2name:
                        svg_title = self._createSvgTitle_(self._displayid2name[did], elem()._trace_info)
                        display.display(svg_title, display_id='algviz_{}'.format(did))
                    display.display(elem(), display_id='algviz{}'.format(did))
                    self._displayed.add(did)
            else:
                if did in self._displayid2name:
                    svg_title = self._createSvgTitle_(self._displayid2name[did], elem()._trace_info)
                    display.update_display(svg_title, display_id='algviz_{}'.format(did))
                display.update_display(elem(), display_id='algviz{}'.format(did))
            temp_displayed = list(self._displayed)
            for did in temp_displayed:
                if did not in self._element2display.values():
                    if did in self._displayid2name:
                        display.update_display(_NoDisplay(), display_id='algviz_{}'.format(did))
                    display.update_display(_NoDisplay(), display_id='algviz{}'.format(did))
                    self._displayed.remove(did)
            time.sleep(self._animate_delay)
        else:
            display.clear_output(wait=True)
            for elem in self._element2display.keyrefs():
                did = self._element2display[elem()]
                if did in self._displayid2name:
                    svg_title = self._createSvgTitle_(self._displayid2name[did], elem()._trace_info)
                    display.display(svg_title, display_id='algviz_{}'.format(did))
                display.display(elem(), display_id='algviz{}'.format(did))
                self._displayed.add(did)
            input('任意键继续：')
        
    '''
    row:int 表格行数；col:int 表格列数。
    data:list(...) 表格中初始化的数据。
    cell_size:float 表格中单元格的长宽尺寸。
    name:str 表格的名字。
    返回：创建的表格对象。
    '''
    def createTable(self, row, col, data=None, cell_size=40, name=None):
        global next_display_id
        tab = table.Table(row, col, data, cell_size)
        self._element2display[tab] = next_display_id
        if name is not None:
            self._displayid2name[next_display_id]=name
        next_display_id += 1
        return tab

    '''
    data:list(...) 向量中初始化的数据。
    cell_size:float 向量中单元格的长宽尺寸。
    name:str 表格的名字。
    bar:float 如果bar值小于零则忽略，否则以柱状图形式显示数据。
    返回：创建的向量对象。
    '''
    def createVector(self, data, cell_size=50, name=None, bar=-1):
        global next_display_id
        vec = vector.Vector(data, self._animate_delay, cell_size, bar)
        self._element2display[vec] = next_display_id
        if name is not None:
            self._displayid2name[next_display_id]=name
        next_display_id += 1
        return vec

    '''
    directed:bool 是否为有向图。
    horizontal:bool 图是否横向排版。
    data:... 拓扑图的初始化数据。
    name:str 拓扑图的显示名称。
    返回：创建的拓扑图可视化对象。
    '''
    def createGraph(self, directed=True, horizontal=False, data=None, name=None):
        global next_display_id
        gra = svg_graph.SvgGraph(data, directed, self._animate_delay, horizontal)
        self._element2display[gra] = next_display_id
        if name is not None:
            self._displayid2name[next_display_id]=name
        next_display_id += 1
        return gra
    
    '''
    gra:SvgGraph 与跟踪器绑定的拓扑图显示对象。
    hold:bool 是否需要在链表中显示trace经过的路径。
    node:ForwardListNode 为跟踪器初始化的链表节点。
    name:str 跟踪器名称。
    '''
    def createForwardListTrace(self, gra, hold=False, node=None, name=None):
        pick_color = self._pickTraceColor_(gra, name)
        if pick_color is None:
            raise Exception('Too many traces in graph!')
        else:
            return link_list.ForwardListTrace(node, gra, pick_color, hold)

    '''
    gra:SvgGraph 与跟踪器绑定的拓扑图显示对象。
    hold:bool 是否需要在二叉树中显示trace经过的路径。
    node:BinaryTreeNode 为跟踪器初始化的二叉树节点。
    name:str 跟踪器名称。
    '''
    def createBinaryTreeTrace(self, gra, hold=False, node=None, name=None):
        pick_color = self._pickTraceColor_(gra, name)
        if pick_color is None:
            raise Exception('Too many traces in graph!')
        else:
            return tree.BinaryTreeTrace(node, gra, pick_color, hold)

    '''
    gra:SvgGraph 与跟踪器绑定的拓扑图显示对象。
    hold:bool 是否需要在拓扑图中显示trace经过的路径。
    node:GraphNode 为跟踪器初始化的拓扑图节点。
    name:str 跟踪器名称。
    '''
    def createGraphTrace(self, gra, hold=False, node=None, name=None):
        pick_color = self._pickTraceColor_(gra, name)
        if pick_color is None:
            raise Exception('Too many traces in graph!')
        else:
            return graph.GraphTrace(node, gra, pick_color, hold)

    '''
    table:Table trace将要绑定的table对象。
    hold:bool 是否需要在表格中显示trace经过的路径。
    r,c:int 初始位置的行列坐标。
    name:str 跟踪器名称。
    '''
    def createTableTrace(self, tab, hold=False, r=0, c=0, name=None):
        pick_color = self._pickTraceColor_(tab, name)
        if pick_color is None:
            raise Exception('Too many traces in table!')
        else:
            return table.TableTrace(tab, pick_color, hold, r, c)

    '''
    vec:Vector trace将要绑定的vector对象。
    hold:bool 是否需要在向量中显示trace经过的路径。
    i:int 跟踪器初始索引位置。
    name:str 跟踪器名称。
    '''
    def createVectorTrace(self, vec, hold=False, i=0, name=None):
        pick_color = self._pickTraceColor_(vec, name)
        if pick_color is None:
            raise Exception('Too many traces in vector!')
        else:
            return vector.VectorTrace(vec, pick_color, hold, i)

    '''
    show_obj:... 可视化对象（该函数自动为可视化对象的跟踪器分配颜色）。
    name:str 跟踪器名称。
    '''
    def _pickTraceColor_(self, show_obj, name):
        if len(show_obj._trace_info) >= len(self._trace_color_list):
            return None
        else:
            pick_color = None
            for i in range(len(self._trace_color_list)):
                pick_color = self._trace_color_list[i]
                if pick_color not in show_obj._trace_info.keys():
                    break
            show_obj._trace_info[pick_color] = name
            return pick_color

    '''
    name:str 表示SVG名称的字符串。
    trace_info:dict() 该SVG对象中的跟踪器信息。
    '''
    def _createSvgTitle_(self, name, trace_info):
        width, margin = 40, 4
        svg_title = svg_table.SvgTable(600, 24)
        svg_title.add_text_element((margin, 16), '{}:'.format(name), font_size=16, fill=(0,0,0))
        nb_trace = 0
        offset_x = utility.text_char_num(name)*8 + margin*2
        for color in trace_info.keys():
            if trace_info[color] is not None:
                x_pos = offset_x + nb_trace*(width + margin)
                svg_title.add_rect_element((x_pos, 2, width, 20), text=trace_info[color], fill=color)
                nb_trace += 1
        return svg_title
