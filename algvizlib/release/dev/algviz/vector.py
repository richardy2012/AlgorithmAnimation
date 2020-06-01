#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

from . import svg_table
from . import utility as util

class Vector():
    '''
    data:list(...) 初始化数据。
    delay:float 动画延时。
    cell_size:float 单元格宽度。
    bar:float 如果bar值小于零则忽略，否则以柱状图形式显示数据。
    show_index:bool 是否显示下标标签。
    '''
    def __init__(self, data, delay, cell_size, bar=-1, show_index=True):
        self._data = list()             # 保存数组中的数据。
        if data is not None:
            for i in range(len(data)):
                self._data.append(data[i])
        self._delay = delay             # 动画延迟时间。
        self._cell_size = cell_size     # 单元格的宽度。
        self._bar = bar                 # 是否以柱状图形式显示数值高度（也包含SVG的高度信息）。
        self._show_index = show_index   # 是否显示下标标签。
        self._cell_margin = 3           # 矩形框之间的边距。
        self._cell_tcs = dict()         # (cell trace color stack)记录所有单元格的轨迹访问信息（节点索引：ColorStack）信息。
        self._frame_trace_old = list()  # 缓存上一帧需要清除的单元格相关信息（节点索引，轨迹颜色值）。
        self._frame_trace = list()      # 记录下一帧待刷新的单元格相关信息(节点索引，轨迹颜色值，是否持久化)。
        self._rect_move = dict()        # 记录下一帧动画中移动的矩形索引和其相对移动距离。
        self._rect_disappear = list()   # 记录下一帧动画中消失的矩形索引。
        self._rect_appear = list()      # 记录下一帧动画中出现的矩形索引。
        self._index2rect = dict()       # 数组下标到显示矩形对象id的映射关系。
        self._index2text = list()       # 数组下标到下标显示文本对象id的映射关系。
        self._label_font_size = int(min(12, cell_size*0.5))   # 下标索引的字体大小。
        svg_height = cell_size + 2*self._cell_margin
        if self._show_index:
            svg_height += self._label_font_size
        if self._bar > 0:
            svg_height = self._bar
        self._svg = svg_table.SvgTable(len(self._data)*cell_size+(len(self._data)+1)*self._cell_margin, svg_height)
        for i in range(len(self._data)):
            rect = (cell_size*i+self._cell_margin*(i+1), self._cell_margin, cell_size, cell_size)
            rid = self._svg.add_rect_element(rect, text=self._data[i])
            self._cell_tcs[rid] = util.TraceColorStack()
            self._index2rect[i] = rid
        if self._bar > 0:
            self._update_bar_height_()
        if self._show_index:
            for i in range(len(self._data)):
                pos = (cell_size*(i+0.5)+self._cell_margin*(i+1)-self._label_font_size*len(str(i))*0.25, svg_height)
                tid = self._svg.add_text_element(pos, i, font_size=self._label_font_size)
                self._index2text.append(tid)
    
    '''
    index:int 要插入的位置，在其前方插入元素。
    val:... 要插入的值。
    '''
    def insert(self, index, val):
        if len(self._data) == 0:
            return self.append(val)
        if index < 0 or index >= len(self._data):
            index %= len(self._data)
        # 向svg中添加新的矩形节点和动画。
        rect = (self._cell_size*index+self._cell_margin*(index+1), self._cell_margin, self._cell_size, self._cell_size)
        rid = self._svg.add_rect_element(rect, text=val)
        # 记录插入位置以后的矩形的移动。
        for i in range(len(self._data), index, -1):
            rrid = self._index2rect[i-1]
            self._index2rect[i] = rrid
            if rrid in self._rect_move:
                self._rect_move[rrid] += 1
            else:
                self._rect_move[rrid] = 1
        self._index2rect[index] = rid
        self._cell_tcs[rid] = util.TraceColorStack()
        self._rect_appear.append(rid)
        self._data.insert(index, val)
    
    '''
    val:... 要添加的值。
    '''
    def append(self, val):
        index = len(self._data)
        rect = (self._cell_size*index+self._cell_margin*(index+1), self._cell_margin, self._cell_size, self._cell_size)
        rid = self._svg.add_rect_element(rect, text=val)
        self._index2rect[index] = rid
        self._cell_tcs[rid] = util.TraceColorStack()
        self._rect_appear.append(rid)
        self._data.append(val)
    
    '''
    index:int 要删除的元素的位置。
    '''
    def pop(self, index = -1):
        if len(self._data) == 0:
            raise Exception('No item in vector to pop!')
        if index < 0 or index >= len(self._data):
            index %= len(self._data)
        rid = self._index2rect[index]
        for i in range(index, len(self._data)-1):
            rrid = self._index2rect[i+1]
            self._index2rect[i] = rrid
            if rrid in self._rect_move:
                self._rect_move[rrid] -= 1
            else:
                self._rect_move[rrid] = -1
        self._index2rect.pop(len(self._data)-1)
        self._rect_disappear.append(rid)
        return self._data.pop(index)
    
    '''
    功能：清除所有元素。
    '''
    def clear(self):
        for i in range(len(self._data)):
            rid = self._index2rect[i]
            self._rect_disappear.append(rid)
        self._index2rect.clear()
        self._rect_move.clear()
        self._rect_appear.clear()
        self._data.clear()
    
    '''
    功能：交换Vector中两个元素的位置。
    index1/index2:int 要交换的两个索引位置。
    '''
    def swap(self, index1, index2):
        rid1 = self._index2rect[index1]
        rid2 = self._index2rect[index2]
        self._index2rect[index1] = rid2
        self._index2rect[index2] = rid1
        if rid1 in self._rect_move.keys():
            self._rect_move[rid1] += index2 - index1
        else:
            self._rect_move[rid1] = index2 - index1
        if rid2 in self._rect_move.keys():
            self._rect_move[rid2] += index1 - index2
        else:
            self._rect_move[rid2] = index1 - index2
        temp_data = self._data[index2]
        self._data[index2] = self._data[index1]
        self._data[index1] = temp_data
    
    '''
    index:int 添加颜色标记的位置。
    color:(R,G,B) 添加的标记颜色值。
    hold:bool 是否持久化标记。
    '''
    def mark(self, index, color, hold=True):
        if index < 0 or index >= len(self._data):
            index %= len(self._data)
        rid = self._index2rect[index]
        self._cell_tcs[rid].add(color)
        self._frame_trace.append((rid, color, hold))
    
    '''
    color:(R,G,B) 将要被删除的颜色标记对象。
    '''
    def removeMark(self, color):
        for rid in self._index2rect.values():
            if self._cell_tcs[rid].remove(color):
                self._svg.update_rect_element(rid, fill=self._cell_tcs[rid].color())
    
    '''
    index:int 要访问对象的索引位置。
    '''
    def __getitem__(self, index):
        if index < 0 or index >= len(self._data):
            index %= len(self._data)
        rid = self._index2rect[index]
        self._cell_tcs[rid].add(util._getElemColor)
        self._frame_trace.append((rid, util._getElemColor, False))
        return self._data[index]
    
    '''
    index:int 要赋值对象的索引位置。
    val:... 对象的新值。
    '''
    def __setitem__(self, index, val):
        if index < 0 or index >= len(self._data):
            index %= len(self._data)
        rid = self._index2rect[index]
        self._cell_tcs[rid].add(util._setElemColor)
        self._frame_trace.append((rid, util._setElemColor, False))
        label = val
        if val is None:
            label = ''
        self._svg.update_rect_element(rid, text=label)
        self._data[index] = val
    
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
        svg_height = self._cell_size + 2*self._cell_margin
        if self._show_index:
            svg_height += self._label_font_size
        if self._bar > 0:
            svg_height = self._bar
        self._svg.update_svg_size(nb_elem*self._cell_size+(nb_elem+1)*self._cell_margin, svg_height)
        for (rid, color) in self._frame_trace_old:
            if rid not in self._cell_tcs.keys():
                continue
            if (rid, color, False) not in self._frame_trace and (rid, color, True) not in self._frame_trace:
                self._cell_tcs[rid].remove(color)
            self._svg.update_rect_element(rid, fill=self._cell_tcs[rid].color())
        self._frame_trace_old.clear()
        for (rid, color, hold) in self._frame_trace:
            self._svg.update_rect_element(rid, fill=self._cell_tcs[rid].color())
            if not hold:
                self._frame_trace_old.append((rid, color))
        self._frame_trace.clear()
        # 添加矩形出现和消失的动画。
        for rid in self._rect_appear:
            self._svg.add_animate_appear(rid, (0, self._delay))
        for rid in self._rect_disappear:
            self._svg.add_animate_appear(rid, (0, self._delay), appear=False)
        # 添加矩形移动的动画。
        if self._bar > 0:
            self._update_bar_height_()
        for rid in self._rect_move.keys():
            if self._rect_move[rid] == 0:
                continue
            self._svg.add_animate_move(rid, (self._rect_move[rid]*(self._cell_size+self._cell_margin), 0) , (0, self._delay), bessel=False)
        if self._show_index:
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
            if num is None:
                continue
            num = float(num)
            if num < 0:
                mmax_data = min(mmax_data, num)
            else:
                max_data = max(max_data, num)
        if (max_data - mmax_data) < 0.0001:
            ratio = 0
        else:
            useful_height = self._bar - 2*self._cell_margin
            if self._show_index:
                useful_height -= self._label_font_size
            ratio = useful_height/(max_data-mmax_data)
        baseline = max_data*ratio + self._cell_margin
        # 更新矩形的位置坐标。
        for i in range(len(self._data)):
            if self._data[i] is None:
                num = 0
            else:
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
            if self._data[i] is None:
                num = None
            self._svg.update_rect_element(rid, rect=(x, y, self._cell_size, abs(height)), text=num)
