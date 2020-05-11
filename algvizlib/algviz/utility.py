#!/usr/bin/env python3

import xml.dom.minidom as xmldom

'''
管理一个元素上的多个颜色，执行颜色融合操作等。
'''
class TraceColorStack():
    def __init__(self):
        self.colors = list()
    
    '''
    color:(R,G,B)待添加的颜色值，stack中已有的颜色值将不能添加进去。
    '''
    def add(self, color):
        if color not in self.colors:
            self.colors.append(color)
    
    '''
    color:(R,G,B)待删除的颜色值。
    返回值：(bool)False：color不在列表中；True：成功删除颜色。
    '''
    def remove(self, color):
        if color in self.colors:
            self.colors.remove(color)
            return True
        else:
            return False
    
    '''
    返回：融合后的颜色值(R,G,B)。
    '''
    def color(self):
        r, g, b = 255, 255, 255
        for (rr, gg, bb) in self.colors:
            r *= rr / 255
            g *= gg / 255
            b *= bb / 255
        return (int(r), int(g), int(b))

'''
将无序的ID值映射到连续的整数空间。
'''
class ConsecutiveIdMap():
    '''
    offset:int 初始映射ID的起始值。
    '''
    def __init__(self, offset=0):
        self._offset = offset
        self._next_id = offset
        self._attr2id = dict()
        self._id2atrr = list()
    
    '''
    attr_id:... 无序ID值。
    返回:int 连续ID值。
    '''
    def toConsecutiveId(attr_id):
        if attr_id in self._attr2id.values():
            return self._attr2id[attr_id]
        else:
            self._attr2id[attr_id] = self._next_id
            self._id2attr.append(attr_id)
            self._next_id += 1
            return self._next_id - 1
    
    '''
    cons_id:int 连续ID值。
    返回:... 无序ID值。
    '''
    def toAttributeId(cons_id):
        return self._id2key[cons_id - self._offset]
    
'''
node:在node的子树中查找满足条件的节点。
tag_name:要查找元素的tag名称。
tag_id:要查找元素的id值。
返回：找到的元素对象或None。
'''
def find_tag_by_id(node, tag_name, tag_id):
    tags = node.getElementsByTagName(tag_name)
    for tag in tags:
        if tag.getAttribute('id') == tag_id:
            return tag
    return None

'''
svg:清除SVG中的所有"<g>...</g>"元素内的动画效果。
'''
def clear_svg_animates(svg):
    gg = svg.getElementsByTagName('g')
    for g in gg:
        animates_appear = g.getElementsByTagName('animate')
        if len(animates_appear):
            g.removeAttribute('style')
        animates_move = g.getElementsByTagName('animateMotion')
        for animate in animates_appear + animates_move:
            g.removeChild(animate)

'''
g:要添加动画的节点。
move:(delt_x, delt_y)对象分别沿x和y轴的移动。
time:(begin, end)动画开始和结束时间。
bessel:代表是否沿贝塞尔曲线路径运动。
'''
def add_animate_move_into_node(g, animate, move, time, bessel):
    g.appendChild(animate)
    if bessel:
        animate.setAttribute('path', 'm0,0 q{:.2f},{:.2f} {:.2f},{:.2f}'.format(move[0]*0.5-move[1]*0.2, move[1]*0.5+move[0]*0.2, move[0], move[1]))
    else:
        animate.setAttribute('path', 'm0,0 l{:.2f},{:.2f}'.format(move[0], move[1]))
    animate.setAttribute('begin', '{:.2f}s'.format(time[0]))
    animate.setAttribute('dur', '{:.2f}s'.format(time[1]-time[0]))
    animate.setAttribute('fill', 'freeze')

'''
g:要添加动画的节点。
time:(begin, end)动画开始和结束时间。
appear:代表是出现动画还是消失动画。
'''
def add_animate_appear_into_node(g, animate, time, appear=True):
    g.setAttribute('style', 'opacity:{:.0f}'.format(not appear))
    g.appendChild(animate)
    animate.setAttribute('attributeName', 'opacity')
    animate.setAttribute('from', '{:.0f}'.format(not appear))
    animate.setAttribute('to', '{:.0f}'.format(appear))
    animate.setAttribute('begin', '{:.2f}s'.format(time[0]))
    animate.setAttribute('dur', '{:.2f}s'.format(time[1]-time[0]))
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

'''
color_str:#F0F0F0格式的字符串。
返回：10进制的RGB颜色元组。
'''
def str2rgbcolor(color_str):
    color_str = color_str.strip('#')
    return (int(color_str[0:2], 16), int(color_str[2:4], 16), int(color_str[4:6], 16))

'''
text_width:float 文本框宽度。
text:str 文本内容（中英文混合都支持）。
返回值：float 理想字体大小。
'''
def text_font_size(text_width, text):
    display_len = 0
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            display_len += 2
        else:
            display_len += 1
    return min(16, text_width*1.5/display_len)
