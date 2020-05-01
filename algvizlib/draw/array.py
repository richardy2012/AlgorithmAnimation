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