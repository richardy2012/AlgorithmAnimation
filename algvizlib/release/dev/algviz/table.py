#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

from . import svg_table
from . import utility

'''
表格对象中指定某一行的迭代器。
'''
class TableRowIter():
    '''
    r:int 指定对哪一行进行迭代。
    tab:Table 绑定的表格对象。
    '''
    def __init__(self, r, tab):
        self._r = r
        self._c = 0
        self._tab = tab
        
    def __iter__(self):
        self._c = 0
        return self
    
    def __next__(self):
        if self._c >= self._tab._col:
            raise StopIteration
        else:
            res = self._tab.getItem(self._r, self._c)
            self._c += 1
            return res

'''
用于操作表格中指定行的元素。
'''
class TableRowOperator():
    def __init__(self, r, tab):
        self._r = r
        self._tab = tab
        
    def __getitem__(self, c):
        return self._tab.getItem(self._r, c)
        
    def __setitem__(self, c, val):
        self._tab.setItem(self._r, c, val)

class Table():
    '''
    row:int 表格行数。
    col:int 表格列数。
    data:list(list(...)) 初始化数据。
    cell_size:float 单元格宽度。
    show_index:bool 是否显示表格行列标签。
    '''
    def __init__(self, row, col, data, cell_size, show_index=True):
        if row <=0 or col <=0:
            raise Exception('Table row/col error!')
        self._row = row
        self._col = col
        self._cell_tcs = dict()           # (cell trace color stack)记录所有单元格的轨迹访问信息（节点索引：ColorStack）信息。
        self._frame_trace_old = list()    # 缓存上一帧需要清除的单元格相关信息（节点索引，轨迹颜色值）。
        self._frame_trace = list()        # 记录下一帧待刷新的单元格相关信息(节点索引，轨迹颜色值，是否持久化)。
        self._delay = 0                   # 用于适配Visualizer，无实际用途。
        self._next_row = 0                # 用于表格的行迭代中标记当前迭代到哪一行。
        self._data = [[None for _ in range(col)] for _ in range(row)]
        label_font_size = int(min(12, cell_size/len(str(max(row,col)-1))))
        table_margin = 3
        svg_width = col*cell_size + table_margin*2
        svg_height = row*cell_size + table_margin*2
        if show_index:
            svg_width += len(str(row-1))*label_font_size
            svg_height += label_font_size
        self._svg = svg_table.SvgTable(svg_width, svg_height)
        for r in range(self._row):
            for c in range(self._col):
                if data is not None:
                    self._data[r][c] = data[r][c]
                rect = (c*cell_size+table_margin, r*cell_size+table_margin, cell_size, cell_size)
                self._svg.add_rect_element(rect, self._data[r][c], angle=False)
                self._cell_tcs[r*col+c] = utility.TraceColorStack()
        if show_index:
            for r in range(row):
                pos = (col*cell_size+table_margin*2, (r+0.5)*cell_size+label_font_size*0.5+table_margin)
                self._svg.add_text_element(pos, r, font_size=label_font_size)
            for c in range(col):
                pos = ((c+0.5)*cell_size-label_font_size*len(str(c))*0.25+table_margin, row*cell_size+1+label_font_size+table_margin)
                self._svg.add_text_element(pos, c, font_size=label_font_size)
    
    '''
    color:(R, G, B) 标记的颜色。
    r/c:int 标记所在的行列索引。
    hold:bool 是否持久化标记。
    '''
    def mark(self, color, r, c, hold=True):
        if r < 0 or r >= self._row or c < 0 or c >= self._col:
            raise Exception("Table index out of range!")
        gid = r*self._col + c
        self._cell_tcs[gid].add(color)
        self._frame_trace.append((gid, color, hold))
    
    '''
    color:(R, G, B) 将要被删除的颜色标记对象。
    '''
    def removeMark(self, color):
        for gid in range(self._row*self._col):
            if self._cell_tcs[gid].remove(color):
                self._svg.update_rect_element(gid, fill=self._cell_tcs[gid].color())
    
    '''
    r/c:int 要访问元素在表格中的行列位置。
    '''
    def getItem(self, r, c):
        if r < 0 or r >= self._row or c < 0 or c >= self._col:
            raise Exception("Table index out of range!")
        gid = r*self._col + c
        self._cell_tcs[gid].add(utility._getElemColor)
        self._frame_trace.append((gid, utility._getElemColor, False))
        return self._data[r][c]
    
    '''
    r/c:int 要修改的元素在表格中的行列位置。
    val:... 修改的元素的新的值。
    '''
    def setItem(self, r, c, val):
        if r < 0 or r >= self._row or c < 0 or c >= self._col:
            raise Exception("Table index out of range!")
        gid = r*self._col + c
        self._cell_tcs[gid].add(utility._setElemColor)
        self._frame_trace.append((gid, utility._setElemColor, False))
        label = val
        if val is None:
            label = ''
        self._svg.update_rect_element(gid, text=label)
        self._data[r][c] = val
    
    '''
    r:int 要访问的行索引。
    返回：TabRowIter 迭代器对象。
    '''
    def __getitem__(self, r):
        return TableRowOperator(r, self)
    
    def __iter__(self):
        self._next_row = 0
        return self
    
    def __next__(self):
        if self._next_row >= self._row:
            raise StopIteration
        else:
            res = TableRowIter(self._next_row, self)
            self._next_row += 1
            return res
    
    '''
    返回:str 表格当前状态下的SVG表示。
    '''
    def _repr_svg_(self):
        for (gid, color) in self._frame_trace_old:
            if (gid, color, True) not in self._frame_trace and (gid, color, False) not in self._frame_trace:
                self._cell_tcs[gid].remove(color)
            self._svg.update_rect_element(gid, fill=self._cell_tcs[gid].color())
        self._frame_trace_old.clear()
        for (gid, color, hold) in self._frame_trace:
            self._svg.update_rect_element(gid, fill=self._cell_tcs[gid].color())
            if not hold:
                self._frame_trace_old.append((gid, color))
        self._frame_trace.clear()
        return self._svg._repr_svg_()
