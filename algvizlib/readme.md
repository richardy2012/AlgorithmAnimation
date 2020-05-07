# algvizlib设计原理

## 文件目录
+ algviz/ 绘图相关代码：
    + `visual.py` 定义基本数据结构（拓扑图、表格）的交互接口。
    + `graph.py` 绘制拓扑图。
    + `table.py` 绘制二维表格。
    + `vector.py` 绘制一维数组。
    + `svg_table.py` 创建矩形列表形式的svg对象。
    + `svg_graph.py` 解析拓扑图的svg对象。
    + `utility.py` 定义一些公共函数。
    + `__init__.py` 表示该文件是一个包。
+ test/ 测试相关代码：
    + `test_svg_table.ipynb` 测试`svg_table.py`中各接口功能是否正常。
    + `test_table.ipynb` 测试`table.py`中各接口功能是否正常。
    + `test_vector.ipynb` 测试`vector.py`中各接口功能是否正常。
    + `test_viusal.ipynb` 测试`visual.py`中各接口功能是否正常。

## 前提条件

+ 假设算法在运行时只执行以下操作：
    + 创建并显示可视化对象。
    + 删除可视化对象。
    + 更新可视化对象：
        + 交换拓扑图中的两节点位置。
        + 添加、删除拓扑图中的节点或边。
        + 强调拓扑图中某些节点或边的颜色。
        + 刷新表格或直方图中的元素（包括添加和删除元素）。
        + 交换表格或直方图中两个元素的位置。
        + 强调表格或直方图中的某些元素。
    + 轨迹标注：
        + 轨迹用来标注当前访问过的（拓扑图、表格、直方图）内的（节点、元素），并对当前（节点、元素）进行强调（改变颜色、闪烁等）。
        + 对于所有探索过（拓扑图、表格、直方图）内的（节点、元素）进行颜色填充，且颜色的深度可以表现出访问次数的多少。

## 模块接口

### 调用层

+ 提供绘图层函数接口以绑定不同的数据结构对象（如：拓扑图、树、列表等），用于后续的显示（参数：1.对象刷新的数据；2.Trace引用对象）（返回值：对象的名称）。
+ 提供用于解除绘图对象绑定的函数（参数：1.对象名称）。
+ 刷新显示函数负责刷新所有的要显示对象，刷新过程通过对比对象中元素值的变化来自动产生动画效果（参数：1.动画延时）。

### 绘图层

+ 定义不同的可视化对象，通过传递进来的变量值对元素进行排版（参数：1.特定的数据结构；2.Trace引用对象）。
+ 更新对象，实现特定的更新动画，动画可根据整体的延时自动调整（参数：1.特定的数据结构）。

### XML层

+ 为SVG对象添加形状、线条和文字（参数：1.形状及坐标；2.文字内容；3.边框颜色；4.填充颜色）（参数：返回创建元素的id）。
+ 为SVG中特定元素添加动画效果（参数：1.元素id；2.移动起点；3.移动终点；4.透明度变化）。

## 绘制图形

### 拓扑图

+ 使用`Graphviz`三方库对拓扑图进行排版。

+ 由于限制拓扑图中的节点数不超过100个，因此使用最简单的邻接矩阵保存拓扑图，而其它格式的图可以很方便的转换为邻接矩阵。
+ Tracer用来表示拓扑图的节点索引（node_id）。

+ 拓扑图更新动画：
    1. 删节点：上一帧SVG中要删除的节点淡出。
    2. 隐藏边：上一帧SVG中的所有边淡出。
    3. 移动节点：利用贝塞尔曲线轨迹移动所有节点。
    4. 移动边：线性移动所有边。
    5. 显示边：所有未被删除的边淡入。
    4. 添加节点和边：要被添加的节点和边淡入。

### 表格

+ 使用二维的list来保存表格，表格的长度。
+ Tracer用来表示表格行和列的索引，使用自定义对象。
+ 使用不同颜色的tracer来标记表格中被访问过的单元格。
    + Tracer的颜色混合策略（目前采用正片垫底的策略）。参考资料：[rgb颜色混合](https://www.jianshu.com/p/6d9a3f39bb53)

### 向量

+ 使用一维的list来保存数组，向量长度不超过100。
+ Tracer用来表示向量下标索引，为自定义对象。
+ 向量支持的操作：
    + 访问和修改向量中的元素：
        + 将访问和修改过的单元格标记对应Tracer的颜色。
    + 向向量中添加元素：
        + 使用insert(tracer, val)接口进行添加元素，将其添加到tracer所在位置前。
        + 添加时自动记录操作，然后在刷新时自动生成动画。
    + 删除向量中的元素：
        + 使用pop(tracer)删除tracer位置所在的元素。
        + 被删除的元素自动淡出，数组尾部的元素向前移动凑齐数组。
    + 求向量长度__len()\_\_接口重载。
+ 动画刷新时的步骤：
    1. 淡出要删除的元素。
    2. 将剩余元素移动到最终位置。
    3. 淡入要显示的元素。
    4. 执行交换运动。

### 其它

+ 根据元素内填充的颜色自动调整文本颜色，文本颜色只设黑白两种。

+ 在SVG的动画移动中，使用`animateMotion`来控制元素的移动，移动中的坐标是相对于元素自身的坐标系统，而不是绝对坐标系统。

## 参考资料

+ 直接对SVG对象进行操作和更新，需要用到python的xml解析库（参考：[菜鸟教程](https://www.runoob.com/python3/python3-xml-processing.html)、[Python官方文档](https://docs.python.org/3/library/xml.dom.html)）。

+ 使用SVG SMIL强大的效果来产生动画（参考：[学长的博客](https://www.zhangxinxu.com/wordpress/2014/08/so-powerful-SVG-smil-animation/)、[浏览器内核官方文档](https://developer.mozilla.org/zh-CN/docs/Web/SVG/SVG_animation_with_SMIL)、[贝塞尔曲线介绍](https://www.zhangxinxu.com/wordpress/2014/06/deep-understand-SVG-path-bezier-curves-command/)）。

+ 编程接口设计时需要用到Python的弱引用技术，这里使用`WeakKeyDictionary`类(参考：[Python官方](https://docs.python.org/3.1/library/weakref.html)，[简书](https://www.jianshu.com/p/0cecea85ae3b))。

+ Python自定义Class中的运算符重载（参考：[简书](https://www.jianshu.com/p/8a51e384b5f3)）。

+ Graphviz绘图库实现拓扑图绘制（参考：[Python官方接口介绍](https://graphviz.readthedocs.io/en/stable/manual.html)，[Python官方例子](https://graphviz.readthedocs.io/en/stable/examples.html)）
