#!/usr/bin/env python3

import xml.dom.minidom as xmldom

class Svgxml():
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
    fill_color:(R,G,B)矩形填充颜色。
    stroke_color:(R,G,B)矩形边框线条颜色。
    返回:该矩形元素的id值。
    '''
    def add_rect_element(self, rect, text=None, fill_color=(255,255,255), stroke_color=(0,0,0)):
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
        r.setAttribute('rx', str(rect[2]*0.1))
        r.setAttribute('ry', str(rect[3]*0.1))
        r.setAttribute('stroke', rgbcolor2str(stroke_color))
        r.setAttribute('fill', rgbcolor2str(fill_color))
        g.appendChild(r)
        if text is not None:
            t = self._dom.createElement('text')
            t.setAttribute('alignment-baseline', 'middle')
            t.setAttribute('text-anchor', 'middle')
            t.setAttribute('x', str(rect[0]+rect[2]*0.5))
            t.setAttribute('y', str(rect[1]+rect[3]*0.5))
            t.setAttribute('fill', auto_text_color(fill_color))
            tt = self._dom.createTextNode(text)
            t.appendChild(tt)
            g.appendChild(t)
        return gid
    
    '''
    gid:str对应显示单元元素的id。
    move:(delt_x, delt_y)对象分别沿x和y轴的移动。
    time:(begin, end)动画开始和结束时间。
    bessel:代表是否沿贝塞尔曲线路径运动。
    '''
    def add_animate_move(self, gid, move, time, bessel=True):
        g = self.__find_node__(gid)
        if g is not None:
            animate = self._dom.createElement('animateMotion')
            add_animate_move_into_node(g, animate, move, time, bessel)
    
    '''
    gid:对应显示单元元素的id。
    time:(begin, end)动画开始和结束时间。
    appear:代表是出现动画还是消失动画。
    '''
    def add_animate_appear(self, gid, time, appear=True):
        g = self.__find_node__(gid)
        if g is not None:
            animate = self._dom.createElement('animate')
            add_animate_appear_into_node(g, animate, time, appear)
    
    '''
    返回：该SVG对应的XML字符串。
    '''
    def toxml(self):
        return self._dom.toxml()

    '''
    gid:要查找元素的id值。
    返回：找到的元素对象或None。
    '''
    def __find_node__(self, gid):
        gg = self._svg.getElementsByTagName('g')
        for g in gg:
            if g.getAttribute('id') == gid:
                return g
        return None

'''
g:要添加动画的节点。
move:(delt_x, delt_y)对象分别沿x和y轴的移动。
time:(begin, end)动画开始和结束时间。
bessel:代表是否沿贝塞尔曲线路径运动。
'''
def add_animate_move_into_node(g, animate, move, time, bessel=True):
    g.appendChild(animate)
    if bessel:
        animate.setAttribute('path', 'm0,0 q{},{} {},{}'.format(move[0]*0.5-move[1]*0.1, move[1]*0.5+move[0]*0.1, move[0], move[1]))
    else:
        animate.setAttribute('path', 'm0,0 l{},{}'.format(move[0], move[1]))
    animate.setAttribute('begin', '{}s'.format(time[0]))
    animate.setAttribute('dur', '{}s'.format(time[1]-time[0]))
    animate.setAttribute('fill', 'freeze')

'''
g:要添加动画的节点。
time:(begin, end)动画开始和结束时间。
appear:代表是出现动画还是消失动画。
'''
def add_animate_appear_into_node(g, animate, time, appear=True):
    g.setAttribute('style', 'opacity:{}'.format(not appear))
    g.appendChild(animate)
    animate.setAttribute('attributeName', 'opacity')
    animate.setAttribute('from', '{:.0f}'.format(not appear))
    animate.setAttribute('to', '{:.0f}'.format(appear))
    animate.setAttribute('begin', '{}s'.format(time[0]))
    animate.setAttribute('dur', '{}s'.format(time[1]-time[0]))
    animate.setAttribute('fill', 'freeze')

'''
back_color:三个10进制数字(R,G,B)表示的文本背景颜色。
返回：16进制表示的(#RGB)格式的文本颜色字符串。
'''
def auto_text_color(back_color):
    rgb_sum = back_color[0]+back_color[1]+back_color[2]
    if rgb_sum < 150:
        return '#FFFFFF'
    else:
        return '#000000'

'''
color:三个10进制数字(R,G,B)表示的RGB颜色。
返回：16进制表示的(#RGB)格式字符串。
'''
def rgbcolor2str(color):
    return '#{:0>2x}{:0>2x}{:0>2x}'.format(color[0], color[1], color[2])
