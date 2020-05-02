#!/usr/bin/env python3

import svg_table as svgtab
import utility as util

class ArrayTrace():
    '''
    array:Array 跟踪器所跟踪的表格对象。
    color:(R,G,B) 跟踪器所在单元格的RGB背景颜色。
    hold:bool 是否一直保留轨迹。
    i:int 跟踪器初始索引位置。
    '''
    def __init__(self, array, color, hold, i):
        self._array = array
        self._color = color
        self._hold = hold
        self.i = i
        
    def __del__(self):
        if self._hold:
            self._array.delete_trace(self._color)

class Array():
    '''
    data:list(...) 初始化数据。
    bar:bool 单元格矩形高度是否和数值有关。
    svg_size:(width:float, height:float) 显示的svg的宽度和高度
    '''
    def __init__(self, data, bar, svg_size):
        self._data = list()
        if data:
            self._data = data
        self._bar = bar
        self._cell_width = 50           # 单元格宽度默认为50个像素点。
        self._svg_width = svg_size[0]
        self._svg_height = svg_size[1]
        self._cell_tcs = dict()         # (cell trace color stack)记录所有单元格的轨迹访问信息（节点索引：ColorStack）信息。
        self._frame_trace_old = list()  # 缓存上一帧需要清除的单元格相关信息（节点索引，轨迹颜色值）。
        self._frame_trace = list()      # 记录下一帧待刷新的单元格相关信息(节点索引，轨迹颜色值，是否持久化)。
        self._frame_animate = list()    # 记录每个索引位置的插入（i），删除（d）和移动（delt值）动画。
    
    '''
    trace:ArrayTrace 数组的跟踪器对象。
    返回：跟踪器对应位置的值。
    '''
    def __getitem__(self, trace):
        pass
    
    '''
    trace:ArrayTrace 数组的跟踪器对象。
    返回：跟踪器对应位置的值。
    '''
    def __setitem__(self, trace, val):
        pass
    
    '''
    trace:ArrayTrace 数组跟踪器对象，在其前方插入元素。
    val:... 要插入的值。
    '''
    def insert(self, trace, val):
        pass
    
    '''
    trace:ArrayTrace 要删除的元素的位置。
    '''
    def pop(self, trace):
        pass
    
    '''
    trace1,trace2:ArrayTrace 要交换的两个跟踪器的位置。
    '''
    def swap(self, trace1, trace2):
        pass
    
    '''
    返回值：int 数组长度。
    '''
    def __len__(self):
        pass
    
    '''
    返回：str 数组当前状态下的SVG表示。
    '''
    def _repr_svg_(self):
        pass
    
    '''
    trace_color:(R,G,B) 将要被删除的数组跟踪器对象的颜色。
    '''
    def delete_trace(self, trace_color):
        pass
