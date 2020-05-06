#!/usr/bin/env python3

import svg_table as svgtab
import utility as util

class TableTrace():
    '''
    table:Table 跟踪器所跟踪的表格对象。
    color:(R,G,B) 跟踪器所在单元格的RGB背景颜色。
    hold:bool 是否一直保留轨迹。
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
            self._table.delete_trace(self._color)

class Table():
    '''
    row:int 表格行数。
    col:int 表格列数。
    data:list(list(...)) 初始化数据。
    cell_size:float 单元格宽度。
    display_id:int 刷新显示所用的id值。
    '''
    def __init__(self, row, col, data, cell_size):
        self._row = row
        self._col = col
        self._cell_tcs = dict()           # (cell trace color stack)记录所有单元格的轨迹访问信息（节点索引：ColorStack）信息。
        self._frame_trace_old = list()    # 缓存上一帧需要清除的单元格相关信息（节点索引，轨迹颜色值）。
        self._frame_trace = list()        # 记录下一帧待刷新的单元格相关信息(节点索引，轨迹颜色值，是否持久化)。
        self._nb_trace = 0                # 记录跟踪器的数目（方便为其分配颜色）。
        if data is None:
            self._data = [[None for _ in range(col)] for _ in range(row)]
        else:
            self._data = data
        self._svg = svgtab.SvgTable(col*cell_size+10, row*cell_size+10)
        for r in range(self._row):
            for c in range(self._col):
                rect = (c*cell_size+5, (r+1)*cell_size+5, cell_size, cell_size)
                self._svg.add_rect_element(rect, self._data[r][c], angle=False)
                self._cell_tcs[r*col+c] = util.TraceColorStack()
        # TODO 添加行号和列号的索引【当vector长度增加时，尾部索引加一，减少时尾部索引减一】。
    
    '''
    trace:TableTrace 表格的跟踪器对象。
    返回： 跟踪器对应位置的值。
    '''
    def __getitem__(self, trace):
        if trace.r < 0 or trace.r >= self._row or trace.c < 0 or trace.c >= self._col:
            raise Exception("Table trace out of range!")
        gid = trace.r*self._col + trace.c
        self._cell_tcs[gid].add(trace._color)
        self._frame_trace.append((gid, trace._color, trace._hold))
        return self._data[trace.r][trace.c]
    
    '''
    trace:TableTrace 表格的跟踪器对象。
    val: 为表格中跟踪器所在单元所赋的值。
    '''
    def __setitem__(self, trace, val):
        if trace.r < 0 or trace.r >= self._row or trace.c < 0 or trace.c >= self._col:
            raise Exception("Table trace out of range!")
        gid = trace.r*self._col + trace.c
        self._cell_tcs[gid].add(trace._color)
        self._frame_trace.append((gid, trace._color, trace._hold))
        self._svg.update_rect_element(gid, text=val)
        self._data[trace.r][trace.c] = val
    
    '''
    返回:str 表格当前状态下的SVG表示。
    '''
    def _repr_svg_(self):
        for (gid, color) in self._frame_trace_old:
            self._cell_tcs[gid].remove(color)
            self._svg.update_rect_element(gid, fill=self._cell_tcs[gid].color())
        self._frame_trace_old.clear()
        for (gid, color, hold) in self._frame_trace:
            self._svg.update_rect_element(gid, fill=self._cell_tcs[gid].color())
            if not hold:
                self._frame_trace_old.append((gid, color))
        self._frame_trace.clear()
        return self._svg._repr_svg_()
    
    '''
    trace_color:(R,G,B) 将要被删除的表格跟踪器对象的颜色。
    '''
    def delete_trace(self, trace_color):
        for gid in range(self._row*self._col):
            if self._cell_tcs[gid].remove(trace_color):
                self._svg.update_rect_element(gid, fill=self._cell_tcs[gid].color())