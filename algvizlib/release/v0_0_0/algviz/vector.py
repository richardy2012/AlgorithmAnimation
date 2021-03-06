#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

from . import svg_table as svgtab
from . import utility as util

class VectorTrace():
    '''
    vector:Vector 跟踪器所跟踪的表格对象。
    color:(R,G,B) 跟踪器所在单元格的RGB背景颜色。
    hold:bool 是否一直保留轨迹。
    i:int 跟踪器初始索引位置。
    '''
    def __init__(self, vector, color, hold, i):
        self._vector = vector
        self._color = color
        self._hold = hold
        self.i = i
        
    def __del__(self):
        self._vector.delete_trace(self)

class Vector():
    '''
    data:list(...) 初始化数据。
    delay:float 动画延时。
    cell_size:float 单元格宽度。
    bar:float 如果bar值小于零则忽略，否则以柱状图形式显示数据。
    '''
    def __init__(self, data, delay, cell_size, bar=-1):
        if not isinstance(data, list):
            return
        self._data = data               # 保存数组中的数据。
        self._delay = delay             # 动画延迟时间。
        self._cell_size = cell_size     # 单元格的宽度。
        self._bar = bar                 # 是否以柱状图形式显示数值高度（也包含SVG的高度信息）。
        self._cell_margin = 3           # 矩形框之间的边距。
        self._cell_tcs = dict()         # (cell trace color stack)记录所有单元格的轨迹访问信息（节点索引：ColorStack）信息。
        self._frame_trace_old = list()  # 缓存上一帧需要清除的单元格相关信息（节点索引，轨迹颜色值）。
        self._frame_trace = list()      # 记录下一帧待刷新的单元格相关信息(节点索引，轨迹颜色值，是否持久化)。
        self._rect_move = dict()        # 记录下一帧动画中移动的矩形索引和其相对移动距离。
        self._rect_disappear = list()   # 记录下一帧动画中消失的矩形索引。
        self._rect_appear = list()      # 记录下一帧动画中出现的矩形索引。
        self._index2rect = dict()       # 数组下标到显示矩形对象id的映射关系。
        self._index2text = list()       # 数组下标到下标显示文本对象id的映射关系。
        self._trace_info = dict()       # 记录现存的所有跟踪器的颜色（方便为下一个跟踪器分配颜色）。
        self._label_font_size = int(min(12, cell_size*0.5))
        svg_height = cell_size + 2*self._cell_margin + self._label_font_size
        if self._bar > 0:
            svg_height = self._bar
        self._svg = svgtab.SvgTable(len(data)*cell_size+(len(data)+1)*self._cell_margin, svg_height)
        for i in range(len(data)):
            rect = (cell_size*i+self._cell_margin*(i+1), self._cell_margin, cell_size, cell_size)
            rid = self._svg.add_rect_element(rect, text=data[i])
            self._cell_tcs[rid] = util.TraceColorStack()
            self._index2rect[i] = rid
        if self._bar > 0:
            self._update_bar_height_()
        for i in range(len(data)):
            pos = (cell_size*(i+0.5)+self._cell_margin*(i+1)-self._label_font_size*len(str(i))*0.25, svg_height)
            tid = self._svg.add_text_element(pos, i, font_size=self._label_font_size)
            self._index2text.append(tid)
    
    '''
    trace:VectorTrace 数组的跟踪器对象。
    返回：跟踪器对应位置的值。
    '''
    def __getitem__(self, trace):
        if trace.i < 0:
            trace.i += len(self._data)
        elif trace.i >= len(self._data):
            trace.i -= len(self._data)
        rid = self._index2rect[trace.i]
        self._cell_tcs[rid].add(trace._color)
        self._frame_trace.append((rid, trace._color, trace._hold))
        return self._data[trace.i]
    
    '''
    trace:VectorTrace 数组的跟踪器对象。
    返回：跟踪器对应位置的值。
    '''
    def __setitem__(self, trace, val):
        if trace.i < 0:
            trace.i += len(self._data)
        elif trace.i >= len(self._data):
            trace.i -= len(self._data)
        rid = self._index2rect[trace.i]
        self._cell_tcs[rid].add(trace._color)
        self._frame_trace.append((rid, trace._color, trace._hold))
        self._svg.update_rect_element(rid, text=val)
        self._data[trace.i] = val
    
    '''
    trace:VectorTrace 数组跟踪器对象，在其前方插入元素。
    val:... 要插入的值。
    '''
    def insert(self, trace, val):
        if trace.i < 0:
            raise Exception('Vector trace out of range!')
        elif trace.i >= len(self._data):
            trace.i = len(self._data)
        # 向svg中添加新的矩形节点和动画。
        rect = (self._cell_size*trace.i+self._cell_margin*(trace.i+1), self._cell_margin, self._cell_size, self._cell_size)
        rid = self._svg.add_rect_element(rect, text=val)
        self._svg.add_animate_appear(rid, (0, self._delay))
        # 记录插入位置以后的矩形的移动。
        for i in range(len(self._data), trace.i, -1):
            rrid = self._index2rect[i-1]
            self._index2rect[i] = rrid
            if rrid in self._rect_move:
                self._rect_move[rrid] += 1
            else:
                self._rect_move[rrid] = 1
        self._index2rect[trace.i] = rid
        self._cell_tcs[rid] = util.TraceColorStack()
        self._rect_appear.append(rid)
        self._data.insert(trace.i, val)
    
    '''
    trace:VectorTrace 要删除的元素的位置。
    '''
    def pop(self, trace):
        if trace.i < 0 or trace.i >= len(self._data):
            raise Exception('Vector trace out of range!')
        rid = self._index2rect[trace.i]
        self._svg.add_animate_appear(rid, (0, self._delay), appear=False)
        for i in range(trace.i, len(self._data)-1):
            rrid = self._index2rect[i+1]
            self._index2rect[i] = rrid
            if rrid in self._rect_move:
                self._rect_move[rrid] -= 1
            else:
                self._rect_move[rrid] = -1
        self._index2rect.pop(len(self._data)-1)
        self._rect_disappear.append(rid)
        self._data.pop(trace.i)
    
    '''
    返回值：int 数组长度。
    '''
    def __len__(self):
        return len(self._data)
    
    '''
    返回：str 数组当前状态下的SVG表示。
    '''
    def _repr_svg_(self):
        # 更新矩形跟踪器的颜色。
        nb_elem = len(self._data) + len(self._rect_disappear)
        svg_height = self._cell_size + 2*self._cell_margin+self._label_font_size
        if self._bar > 0:
            svg_height = self._bar
        self._svg.update_svg_size(nb_elem*self._cell_size+(nb_elem+1)*self._cell_margin, svg_height)
        for (rid, color) in self._frame_trace_old:
            self._cell_tcs[rid].remove(color)
            self._svg.update_rect_element(rid, fill=self._cell_tcs[rid].color())
        self._frame_trace_old.clear()
        for (rid, color, hold) in self._frame_trace:
            self._svg.update_rect_element(rid, fill=self._cell_tcs[rid].color())
            if not hold:
                self._frame_trace_old.append((rid, color))
        self._frame_trace.clear()
        # 添加矩形移动的动画。
        if self._bar > 0:
            self._update_bar_height_()
        for rid in self._rect_move.keys():
            if self._rect_move[rid] == 0:
                continue
            self._svg.add_animate_move(rid, (self._rect_move[rid]*(self._cell_size+self._cell_margin), 0) , (0, self._delay), bessel=False)
        if len(self._index2text) > len(self._data):
            for i in range(len(self._index2text)-len(self._data)):
                self._svg.delete_element(self._index2text[-1])
                self._index2text.pop()
        elif len(self._index2text) < len(self._data):
            for i in range(len(self._index2text), len(self._data)):
                pos = (self._cell_size*(i+0.5)+self._cell_margin*(i+1)-self._label_font_size*0.25*len(str(i)), svg_height)
                tid = self._svg.add_text_element(pos, i, font_size=self._label_font_size)
                self._index2text.append(tid)
        self._rect_move.clear()
        res = self._svg._repr_svg_()
        # 清除动画效果，更新SVG内容，为下一帧做准备。
        self._svg.clear_animates()
        if self._bar > 0:
            self._update_bar_height_()
        else:
            for i in range(len(self._data)):
                rect = (self._cell_size*i+self._cell_margin*(i+1), self._cell_margin, self._cell_size, self._cell_size)
                rid = self._index2rect[i]
                self._svg.update_rect_element(rid, rect=rect)
        for rid in self._rect_disappear:
            self._svg.delete_element(rid)
            self._cell_tcs.pop(rid)
        self._rect_disappear.clear()
        for rid in self._rect_appear:
            self._svg.update_rect_element(rid, opacity=True)
        self._rect_appear.clear()
        return res
    
    '''
    功能：更新柱状图中每个柱子的高度。
    '''
    def _update_bar_height_(self):
        # 根据数据范围调整比率和基线位置。
        mmax_data, max_data = 0, 0
        for num in self._data:
            num = float(num)
            if num < 0:
                mmax_data = min(mmax_data, num)
            else:
                max_data = max(max_data, num)
        ratio = (self._bar - 2*self._cell_margin - self._label_font_size)/(max_data-mmax_data)
        baseline = max_data*ratio + self._cell_margin
        # 更新矩形的位置坐标。
        for i in range(len(self._data)):
            num = float(self._data[i])
            rid = self._index2rect[i]
            x = self._cell_size*i + self._cell_margin*(i+1)
            if rid in self._rect_move.keys():
                x -= self._rect_move[rid] * (self._cell_size+self._cell_margin)
            height = ratio*num
            if num < 0:
                y = baseline
            else:
                y = baseline - height
            if num - int(num) > 0.001:
                num = '{:.2f}'.format(num)
            else:
                num = '{:.0f}'.format(num)
            self._svg.update_rect_element(rid, rect=(x, y, self._cell_size, abs(height)), text=num)
    
    '''
    trace:TableTrace 将要被删除的数组跟踪器对象。
    '''
    def delete_trace(self, trace):
        if trace._hold:
            for rid in self._index2rect.values():
                if self._cell_tcs[rid].remove(trace._color):
                    self._svg.update_rect_element(rid, fill=self._cell_tcs[rid].color())
        self._trace_info.pop(trace._color)
