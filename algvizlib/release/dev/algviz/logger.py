#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

'''
用于将字符串输出到屏幕中。
'''
class Logger():
    '''
    buffer_lines:int 记录器最大缓存行数。
    '''
    def __init__(self, buffer_lines):
        self._buffer_lines = buffer_lines
        self._logs = list()
    
    '''
    功能：向日志输出器中写入输出数据。
    data:str 输出的数据内容。
    '''
    def write(self, data):
        data_lines = data.split('\n')
        for line in data_lines:
            if len(self._logs) >= self._buffer_lines:
                self._logs.pop(0)
            self._logs.append(line)
    
    '''
    功能：情况缓存的数据。
    '''
    def clear(self):
        self._logs.clear()
    
    def __repr__(self):
        res = str()
        for s in self._logs:
            res += s + '\n'
        return res
