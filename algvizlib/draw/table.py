#!/usr/bin/env python3

import utility

class TableTrace():
    '''
    _id:int跟踪器在所在表格中的id值。
    table:Table跟踪器所跟踪的表格对象。
    color:str跟踪器所在单元格的背景颜色（如：'#FF0000'）。
    hold:bool是否在表格中保留跟踪器经过的轨迹。
    r:int跟踪器起点所在行坐标。
    c:int跟踪器起点所在列坐标。
    '''
    def __init__(self, _id, table, color, hold, r, c):
        self._id = _id
        self._table = table
        self._color = color
        self._hold = hold
        self.r = r
        self.c = c

    '''
    跟踪器被销毁时自动调用的回调函数。
    '''
    def callback(self):
        pass

    
class Table():
    '''
    row:int表格行数。
    col:int表格列数。
    display_id:int刷新显示所用的id值。
    '''
    def __init__(self, row, col, display_id, data = None):
        self._row = row
        self._col = col
        self._display_id = display_id
        self._next_traceid = 0
        self._traceid2color = dict()
        self._visit_info = dict()
        if data is None:
            self._data = [['' for _ in col] for _ in row]
        else:
            self._data = data
        self._svg = utility.Svgxml()
        self.init_svg()
        
    def init_svg(self):
        pass
    
    def __getitem__(self, trace):
        pass
    
    def __setitem__(self, trace, val):
        pass
    
    def update_animate(self):
        pass
    
    def del_trace(self, traceid):
        pass
  
    
        