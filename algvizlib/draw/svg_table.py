#!/usr/bin/env python3

import xml.dom.minidom as xmldom
import utility as util

class SvgTable():
    '''
    width:SVG的宽度；heigt:SVG的高度。
    创建一个SVG的XML结构对象。
    '''
    def __init__(self, width, height):
        self._dom = xmldom.Document()
        self._cur_id = 0
        self._svg = self._dom.createElement('svg')
        self._svg.setAttribute('width', '{:.0f}pt'.format(width))
        self._svg.setAttribute('height', '{:.0f}pt'.format(height))
        self._svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
        self._dom.appendChild(self._svg)

    '''
    rect:(x, y, w, h)矩形左下角坐标和矩形尺寸。
    text:矩形内部文本字符串。
    fill:(R,G,B)矩形填充颜色。
    stroke:(R,G,B)矩形边框颜色。
    angle:bool代表矩形四个角是否为圆角。
    返回:int该矩形元素的id值。
    '''
    def add_rect_element(self, rect, text=None, fill=(255,255,255), stroke=(123,123,123), angle=True):
        gid = str(self._cur_id)
        self._cur_id += 1
        g = self._dom.createElement('g')
        g.setAttribute('id', gid)
        self._svg.appendChild(g)
        r = self._dom.createElement('rect')
        r.setAttribute('x', str(rect[0]))
        r.setAttribute('y', str(rect[1]))
        r.setAttribute('width', str(rect[2]))
        r.setAttribute('height', str(rect[3]))
        if angle is True:
            r.setAttribute('rx', str(rect[2]*0.1))
            r.setAttribute('ry', str(rect[3]*0.1))
        r.setAttribute('fill', util.rgbcolor2str(fill))
        r.setAttribute('stroke', util.rgbcolor2str(stroke))
        g.appendChild(r)
        if text is not None:
            t = self._dom.createElement('text')
            t.setAttribute('alignment-baseline', 'middle')
            t.setAttribute('text-anchor', 'middle')
            t.setAttribute('x', str(rect[0]+rect[2]*0.5))
            t.setAttribute('y', str(rect[1]+rect[3]*0.5))
            t.setAttribute('fill', util.auto_text_color(fill))
            tt = self._dom.createTextNode('{}'.format(text))
            t.appendChild(tt)
            g.appendChild(t)
        return int(gid)
    
    '''
    gid:int要更新的矩形元素的ID值。
    text:矩形内部文本字符串。
    fill:(R,G,B)矩形填充颜色。
    stroke:(R,G,B)矩形边框颜色。
    '''
    def update_rect_element(self, gid, text=None, fill=None, stroke=None):
        g = util.find_tag_by_id(self._svg, 'g', str(gid))
        if g is None:
            return
        r = g.getElementsByTagName('rect')[0]
        t = g.getElementsByTagName('text')
        if fill is not None:
            r.setAttribute('fill', util.rgbcolor2str(fill))
            if len(t):
                t[0].setAttribute('fill', util.auto_text_color(fill))
        if text is not None:
            if len(t) == 0:
                rx = int(r.getAttribute('x'))
                ry = int(r.getAttribute('y'))
                width = int(r.getAttribute('width'))
                height = int(r.getAttribute('height'))
                fc = util.str2rgbcolor(r.getAttribute('fill'))
                t = self._dom.createElement('text')
                g.appendChild(t)
                t.setAttribute('alignment-baseline', 'middle')
                t.setAttribute('text-anchor', 'middle')
                t.setAttribute('x', str(rx+width*0.5))
                t.setAttribute('y', str(ry+height*0.5))
                t.setAttribute('fill', util.auto_text_color(fc))
            else:
                t = t[0]
                for t_child in t.childNodes:
                    t.removeChild(t_child)
            tt = self._dom.createTextNode('{}'.format(text))
            t.appendChild(tt)
        if stroke is not None:
            r.setAttribute('stroke', util.rgbcolor2str(stroke))
    
    '''
    gid:int要删除的矩形元素的ID值。
    '''
    def delete_rect_element(self, gid):
        g = util.find_tag_by_id(self._svg, 'g', str(gid))
        if g is not None:
            self._svg.removeChild(g)
    
    '''
    gid:int对应显示单元元素的id。
    move:(delt_x, delt_y)对象分别沿x和y轴的移动。
    time:(begin, end)动画开始和结束时间。
    bessel:代表是否沿贝塞尔曲线路径运动。
    '''
    def add_animate_move(self, gid, move, time, bessel=True):
        g = util.find_tag_by_id(self._svg, 'g', str(gid))
        if g is not None:
            animate = self._dom.createElement('animateMotion')
            util.add_animate_move_into_node(g, animate, move, time, bessel)
    
    '''
    gid:int对应显示单元元素的id。
    time:(begin, end)动画开始和结束时间。
    appear:代表是出现动画还是消失动画。
    '''
    def add_animate_appear(self, gid, time, appear=True):
        g = util.find_tag_by_id(self._svg, 'g', str(gid))
        if g is not None:
            animate = self._dom.createElement('animate')
            util.add_animate_appear_into_node(g, animate, time, appear)
    
    '''
    清除该SVG中所有的动画效果。
    '''
    def clear_animates(self):
        util.clear_svg_animates(self._svg)
    
    '''
    返回：该SVG对应的XML字符串，用于notebook中的显示。
    '''
    def _repr_svg_(self):
        return self._dom.toxml()
