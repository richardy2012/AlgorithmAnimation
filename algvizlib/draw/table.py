#!/usr/bin/env python3

import copy
import utility

class Table():
    '''
    table:list(list())二维列表，内含用来显示的数据。
    trace:[row, col]表示当前所在行和列的索引值。
    '''
    def __init__(self, table, trace):
        self._table = table
        self._old_table = copy.deepcopy(table)
        self._trace = trace
        for row in self._table:
            self._visited.append([False for _ in len(row)])

    def _repr_svg_(self):
        pass
