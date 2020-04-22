import xml.dom.minidom

'''
width:SVG宽度; height:SVG高度。
返回:SVG的开始标签字符串。
'''
def svg_begin(width, height)：
    pass

'''
返回:SVG的结束标签字符串。
'''
def svg_end():
    pass

'''
rect:(x, y, w, h)矩形左下角坐标和矩形尺寸。
text:矩形内部文本字符串。
fill_color:(R,G,B)矩形填充颜色。
stroke_color:(R,G,B)矩形边框线条颜色。
返回:SVG中的一个带文字的矩形描述字符串。
'''
def svg_rect(name, rect, text=None, fill_color=(255,255,255), stroke_color=(0,0,0)):
    pass

'''
from:(x1, y1)起点坐标。
to:(x2, y2)终点坐标。
time:(begin, end)动画开始和结束时间。
bessel:代表是否沿贝塞尔曲线路径运动。
返回:SVG中描述运动动画的字符串。
'''
def svg_move(form, to, time, bessel=False):
    pass

'''
time:(begin, end)动画开始和结束时间。
appear:代表是出现动画还是消失动画。
返回:SVG中描述透明度变换的字符串。
'''
def svg_opacity(time, appear=False):
    pass
