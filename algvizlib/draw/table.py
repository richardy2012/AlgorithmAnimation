#!/usr/bin/env python3

import copy
import utility

class TableTrace():
    '''
    table:Table 跟踪器所跟踪的表格对象。
    color:(R,G,B) 跟踪器所在单元格的RGB背景颜色。
    r:int 跟踪器起点所在行坐标。
    c:int 跟踪器起点所在列坐标。
    '''
    def __init__(self, table, color, hold, r, c):
        self._table = table
        self._color = color
        self._hold = hold
        self.r = r
        self.c = c

    def __del__(self):
        if self._hold:
            self._table.delete_trace(self)

class Table():
    '''
    row:int 表格行数。
    col:int 表格列数。
    display_id:int 刷新显示所用的id值。
    '''
    def __init__(self, row, col, data, cell_size):
        self._row = row
        self._col = col
        self._hold_visit = dict()     # 记录被访问单元格的所有（节点：颜色列表）信息。
        self._old_visit = list()      # 记录上一轮临时显示的所有节点信息。
        self._new_visit = dict()     # 记录上一轮临时显示的所有(节点：颜色)信息。
        if data is None:
            self._data = [[None for _ in range(col)] for _ in range(row)]
        else:
            self._data = data
        self._svg = utility.Svgxml(col*cell_size+10, row*cell_size+10)
        for r in range(self._row):
            for c in range(self._col):
                rect = (c*cell_size+5, (r+1)*cell_size+5, cell_size, cell_size)
                self._svg.add_rect_element(rect, self._data[r][c], angle=False)
                self._hold_visit[r*col+c] = [(255,255,255)]
    
    '''
    trace:TableTrace 表格的跟踪器对象。
    返回： 跟踪器对应位置的值。
    '''
    def __getitem__(self, trace):
        gid = trace.r*self._col + trace.c
        if trace._hold:
            if trace._color != self._hold_visit[gid][-1]:
                self._svg.update_rect_element(gid, fill=trace._color)
                self._hold_visit[gid].append(trace._color)
        else:
            self._new_visit[trace._color] = gid
        return self._data[trace.r][trace.c]
    
    '''
    trace:TableTrace 表格的跟踪器对象。
    val: 为表格中跟踪器所在单元所赋的值。
    '''
    def __setitem__(self, trace, val):
        gid = trace.r*self._col + trace.c
        if trace._hold:
            if trace._color != self._hold_visit[gid][-1]:
                self._svg.update_rect_element(gid, text=val, fill=trace._color)
                self._hold_visit[gid].append(trace._color)
        else:
            self._new_visit[trace._color] = gid
        self._data[trace.r][trace.c] = val
    
    '''
    返回:str 表格当前状态下的SVG表示。
    '''
    def _repr_svg_(self):
        for gid in self._old_visit:
            old_color = self._hold_visit[gid][-1]
            self._svg.update_rect_element(gid, fill=old_color)
        self._old_visit.clear()
        for (color, gid) in self._new_visit.items():
            self._svg.update_rect_element(gid, fill=color)
            self._old_visit.append(gid)
        self._new_visit.clear()
        return self._svg._repr_svg_()
    
    '''
    trace:TableTrace将要被删除的表格跟踪器对象。
    '''
    def delete_trace(self, trace):
        for gid in self._hold_visit.keys():
            for color in self._hold_visit[gid]:
                if color == trace._color:
                    self._hold_visit[gid].remove(color)
            self._svg.update_rect_element(gid, fill=self._hold_visit[gid][-1])
