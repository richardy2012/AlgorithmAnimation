#!/usr/bin/env python3

import graphviz
import xml.dom.minidom as xmldom
import utility as util

class SvgGraph(): 
    '''
    root:... 拓扑图的根节点，用于初始化拓扑图（可以是图/树/链表的节点）。
    directed:bool 表示拓扑图是否为有向图。
    delay:float 动画延时时长。
    horizontal:bool 是否对拓扑图进行横向排版（用于链表类型的图的显示）。
    '''
    def __init__(self, root, directed, delay, horizontal=False):
        self._directed = directed       # 拓扑图是否为有向图。
        self._delay = delay             # 每帧动画的延时时长。
        self._horizontal = horizontal   # 拓扑图是否横向排版。
        self._node_label = dict()       # 拓扑图每个节点上要显示的标签信息。
        self._edge_label = dict()       # 拓扑图每条边上要显示的标签信息。
        self._node_tcs = dict()         # 记录所有节点中的轨迹访问信息（节点索引：ColorStack）。
        self._edge_tcs = dict()         # 记录当前拓扑图中所有边的轨迹访问信息（（起点索引，终点索引）：ColorStack）。
        self._node_appear = set()       # 记录下一帧动画中消失的节点索引集合。
        self._node_disappear = set()    # 记录下一帧动画中消失的节点索引集合。
        self._node_move = set()         # 记录在动画效果中移动的节点索引集合。
        self._frame_trace_old = list()  # 缓存上一帧需要清除的节点/边相关信息（节点索引，轨迹颜色值）。
        self._frame_trace = list()      # 记录下一帧待刷新的节点/边相关信息(节点索引，轨迹颜色值，是否持久化)。
        self._trace_color = set()       # 记录现存的所有跟踪器的颜色（方便为下一个跟踪器分配颜色）。
        self._svg = None                # 将要显示的拓扑图的svg对象。
        self._node_idmap = None         # 实际节点id值和graphviz中对应节点的id值。
        self._edge_idmap = None         # 实际节点对的id值和graphviz中对应边的id值。
        self._trace_last_visit = dict() # 记录拓扑中所有跟踪器上一次访问的节点id值（(R,G,B):id）。
        (self._svg, self._node_idmap, self._edge_idmap) = self._create_svg_()
        if root is not None:
            self.add_node(root, None, True)

    '''
    node:... 要添加的节点对象，可以是拓扑图/树/链表节点。
    parent:... node的父节点对象，需要与node的类型一致。
    recursive:bool 是否递归的添加和node相关联的节点。
    '''
    def add_node(self, node, parent, recursive):
        visited = {id(parent)}
        node_stack = [node]
        temp_edge_label = list()
        if parent is not None and node is not None:
            for neigh in parent._neighbors_():
                if id(neigh[0]) == id(node):
                    temp_edge_label.append((id(parent), id(node), neigh[1]))
        while len(node_stack) > 0:
            cur_node = node_stack.pop()
            if cur_node is None or id(cur_node) in visited:
                continue
            visited.add(id(cur_node))
            self._node_label[id(cur_node)] = cur_node.val
            self._node_tcs[id(cur_node)] = util.TraceColorStack()
            self._node_appear.add(id(cur_node))
            if recursive:
                for neigh in cur_node._neighbors_()[::-1]:
                    if neigh[0] is None:
                        continue
                    temp_edge_label.append((id(cur_node), id(neigh[0]), neigh[1]))
                    node_stack.append(neigh[0])
        # 为所有新增边添加标签和轨迹颜色记录。
        for (n1id, n2id, label) in temp_edge_label:
            self._edge_label[(n1id, n2id)] = label
            self._edge_tcs[(n1id, n2id)] = util.TraceColorStack(bgcolor=(0, 0, 0))
    
    '''
    node:... 要删除的节点对象，可以是拓扑图/树/链表节点。
    recursive:bool 是否递归的删除和node相关联的节点。
    '''
    def delete_node(self, node, recursive):
        visited = set()
        node_stack = [node]
        while len(node_stack) > 0:
            cur_node = node_stack.pop()
            if cur_node is None or id(cur_node) in visited:
                continue
            visited.add(id(cur_node))
            self._node_label.pop(id(cur_node))
            self._node_tcs.pop(id(cur_node))
            self._node_disappear.add(id(cur_node))
            if recursive:
                for neigh in cur_node._neighbors_():
                    node_stack.append(neigh[0])
        # 删除所有消失边的标签和轨迹颜色记录。
        temp_remove_edges = list()
        for (n1id, n2id) in self._edge_label.keys():
            if n1id in self._node_disappear or n2id in self._node_disappear:
                temp_remove_edges.append((n1id, n2id))
        for k in temp_remove_edges:
            self._edge_label.pop(k)
            self._edge_tcs.pop(k)
        
    '''
    node:... 跟踪器访问的节点，可以是拓扑图/树/链表节点。
    color:(R,G,B) 跟踪器的颜色。
    hold:bool 是否保留轨迹颜色。
    '''
    def trace_visit(self, node, color, hold):
        if node is not None and self._node_label[id(node)] != node.val:
            self._node_label[id(node)] = node.val
            node_id = 'node{}'.format(self._node_idmap.toConsecutiveId(id(node)))
            svg_node = util.find_tag_by_id(self._svg, 'g', node_id)
            self._update_node_label_(svg_node, node.val)
        if color in self._trace_last_visit.keys() and self._trace_last_visit[color] == id(node):
            return
        self._node_tcs[id(node)].add(color)
        self._frame_trace.append((id(node), color, hold))
        if color in self._trace_last_visit.keys():
            edge_key = (self._trace_last_visit[color], id(node))
            if edge_key in self._edge_tcs.keys():
                self._edge_tcs[edge_key].add(color)
                self._frame_trace.append((edge_key, color, hold))
        self._trace_last_visit[color] = id(node)
    
    '''
    color:(R,G,B) 将要被删除的跟踪器颜色。
    hold:bool 是否保留轨迹颜色。
    '''
    def delete_trace(self, color, hold):
        if hold == True:
            for k in self._node_label.keys():
                if self._node_tcs[k].remove(color):
                    node_id = 'node{}'.format(self._node_idmap.toConsecutiveId(k))
                    node = util.find_tag_by_id(self._svg, 'g', node_id)
                    self._update_node_color_(node, self._node_tcs[k].color())
            for k in self._edge_label.keys():
                if self._edge_tcs[k].remove(color):
                    edge_id = 'edge{}'.format(self._edge_idmap.toConsecutiveId(k))
                    edge = util.find_tag_by_id(self._svg, 'g', edge_id)
                    self._update_edge_color_(edge, self._edge_tcs[k].color())
        self._trace_color.remove(color)
        self._trace_last_visit.pop(color)
    
    '''
    返回:str 拓扑图SVG显示字符串。
    '''
    def _repr_svg_(self):
        # 更新节点跟踪器的颜色。
        self._update_trace_color_()
        if len(self._node_appear)==0 and len(self._node_disappear)==0:
            return self._svg.toxml()
        # 对拓扑图进行重新排版并添加动画效果。
        (new_svg, node_idmap, edge_idmap) = self._create_svg_()
        self._update_svg_size_(new_svg)
        self._update_svg_nodes_(new_svg, node_idmap)
        self._update_svg_edges_(new_svg, edge_idmap)
        self._node_appear.clear()
        self._node_disappear.clear()
        self._node_move.clear()
        res = self._svg.toxml()
        # 更新SVG内容，为下一帧做准备。
        self._svg, self._node_idmap, self._edge_idmap = new_svg, node_idmap, edge_idmap
        new_nodes = self._get_node_pos_(self._svg)
        for node_id in new_nodes.keys():
            nid = self._node_idmap.toAttributeId(node_id)
            self._update_node_color_(new_nodes[node_id][0], self._node_tcs[nid].color())
        new_edges = self._get_svg_edges_(self._svg)
        for edge_id in new_edges.keys():
            eid = self._edge_idmap.toAttributeId(edge_id)
            self._update_edge_color_(new_edges[edge_id], self._edge_tcs[eid].color())
        return res
    
    '''
    node:xmldom.Node 要更新的拓扑图节点的SVG对象。
    color:(R,G,B) 新的颜色值。
    '''
    def _update_node_color_(self, node, color):
        if node is not None:
            ellipse = node.getElementsByTagName('ellipse')[0]
            ellipse.setAttribute('fill', util.rgbcolor2str(color))
            text = node.getElementsByTagName('text')[0]
            if text is not None:
                text.setAttribute('fill', util.auto_text_color(color))
    '''
    edge:xmldom.Node 要更新的拓扑图边的SVG对象。
    color:(R,G,B) 新的颜色值。
    '''
    def _update_edge_color_(self, edge, color):
        if edge is not None:
            polygon = edge.getElementsByTagName('polygon')[0]
            polygon.setAttribute('fill', util.rgbcolor2str(color))
    
    '''
    功能：更新拓扑图中节点的标签值。
    node:xmldom.Node 要更新的节点对象。
    text:... 新的标签内容。
    '''
    def _update_node_label_(self, node, text):
        if node is None or text is None:
            return
        ellipse = node.getElementsByTagName('ellipse')[0]
        cx = float(ellipse.getAttribute('cx'))
        cy = float(ellipse.getAttribute('cy'))
        rx = float(ellipse.getAttribute('rx'))
        fc = util.str2rgbcolor(ellipse.getAttribute('fill'))
        text_svg = node.getElementsByTagName('text')
        if text_svg is not None:
            node.removeChild(text_svg[0])
        t = self._svg.createElement('text')
        t.setAttribute('alignment-baseline', 'middle')
        t.setAttribute('text-anchor', 'middle')
        t.setAttribute('x', '{:.2f}'.format(cx))
        t.setAttribute('y', '{:.2f}'.format(cy))
        font_size = min(12, util.text_font_size(2*rx, '{}'.format(text)))
        t.setAttribute('font-size', '{:.2f}'.format(font_size))
        t.setAttribute('fill', util.auto_text_color(fc))
        tt = self._svg.createTextNode('{}'.format(text))
        t.appendChild(tt)
        node.appendChild(t)
    
    '''
    功能：更新该帧中SVG的轨迹颜色变化。
    '''
    def _update_trace_color_(self):
        for k, color in self._frame_trace_old:
            if type(k) == int:
                self._node_tcs[k].remove(color)
                node_id = 'node{}'.format(self._node_idmap.toConsecutiveId(k))
                node = util.find_tag_by_id(self._svg, 'g', node_id)
                self._update_node_color_(node, self._node_tcs[k].color())
            else:
                self._edge_tcs[k].remove(color)
                edge_id = 'edge{}'.format(self._edge_idmap.toConsecutiveId(k))
                edge = util.find_tag_by_id(self._svg, 'g', edge_id)
                self._update_edge_color_(edge, self._edge_tcs[k].color())
        self._frame_trace_old.clear()
        for k, color, hold in self._frame_trace:
            if type(k) == int:
                node_id = 'node{}'.format(self._node_idmap.toConsecutiveId(k))
                node = util.find_tag_by_id(self._svg, 'g', node_id)
                self._update_node_color_(node, self._node_tcs[k].color())
            else:
                edge_id = 'edge{}'.format(self._edge_idmap.toConsecutiveId(k))
                edge = util.find_tag_by_id(self._svg, 'g', edge_id)
                self._update_edge_color_(edge, self._edge_tcs[k].color())
            if not hold:
                self._frame_trace_old.append((nid, color))
        self._frame_trace.clear()
    
    '''
    功能：调整self._svg的视图尺寸，以保证所有元素都能被观察到。
    new_svg:xmldom.Document 最新的SVG对象。
    '''
    def _update_svg_size_(self, new_svg):
        old_svg_node = self._svg.getElementsByTagName('svg')[0]
        new_svg_node = new_svg.getElementsByTagName('svg')[0]
        old_svg_width = int(old_svg_node.getAttribute('width')[0:-2])
        old_svg_height = int(old_svg_node.getAttribute('height')[0:-2])
        new_svg_width = int(new_svg_node.getAttribute('width')[0:-2])
        new_svg_height = int(new_svg_node.getAttribute('height')[0:-2])
        width = max(old_svg_width, new_svg_width)
        height = max(old_svg_height, new_svg_height)
        old_svg_node.setAttribute('width', '{}pt'.format(width))
        old_svg_node.setAttribute('height', '{}pt'.format(height))
        old_svg_node.setAttribute('viewBox', '0.00 0.00 {:.2f} {:.2f}'.format(width, height))
        graph = util.find_tag_by_id(new_svg, 'g', 'graph0')
        clone_graph = graph.cloneNode(deep=False)
        clone_graph.setAttribute('id', 'graph1')
        old_svg_node.appendChild(clone_graph)
    
    '''
    功能：向SVG中添加所有与节点有关的动画。
    edge_idmap:ConsecutiveIdMap 边在内存中的ID和在SVG中的ID的双向映射关系。
    new_svg:xmldom.Document 最新的SVG对象。
    '''
    def _update_svg_edges_(self, new_svg, edge_idmap):
        old_edges = self._get_svg_edges_(self._svg)
        new_edges = self._get_svg_edges_(new_svg)
        for old_edge_id in old_edges.keys():
            (n1id, n2id) = self._edge_idmap.toAttributeId(old_edge_id)  # 边的（起点，终点）在内存中的ID值。
            # 添加边的消失动画效果。
            if n1id in self._node_disappear or n2id in self._node_disappear or n1id in self._node_move or n2id in self._node_move:
                g = old_edges[old_edge_id]
                animate = self._svg.createElement('animate')
                util.add_animate_appear_into_node(g, animate, (0, self._delay), False)
        graph = util.find_tag_by_id(self._svg, 'g', 'graph1')
        for new_edge_id in new_edges.keys():
            (n1id, n2id) = edge_idmap.toAttributeId(new_edge_id)
            if n1id in self._node_appear or n2id in self._node_appear or n1id in self._node_move or n2id in self._node_move:
                old_edge_id = self._edge_idmap.toConsecutiveId((n1id, n2id))
                clone_edge = new_edges[new_edge_id].cloneNode(deep=True)
                clone_edge.setAttribute('id', 'edge{}'.format(old_edge_id))
                graph.appendChild(clone_edge)
                animate = self._svg.createElement('animate')
                util.add_animate_appear_into_node(clone_edge, animate, (0, self._delay), True)
    
    '''
    功能：向SVG中添加所有与边有关的动画。
    node_idmap:ConsecutiveIdMap 节点在内存中的ID和在SVG中的ID的双向映射关系。
    new_svg:xmldom.Document 最新的SVG对象。
    '''
    def _update_svg_nodes_(self, new_svg, node_idmap):
        old_pos = self._get_node_pos_(self._svg)
        new_pos = self._get_node_pos_(new_svg)
        for old_node_id in old_pos.keys():
            old_nid = self._node_idmap.toAttributeId(old_node_id)    # 在内存中的ID值。
            if old_nid in node_idmap._attr2id.keys():
                import pdb;pdb.set_trace()
                # TODO 调试移动位置出错的bug。
                # 添加图节点的移动动画效果。
                new_node_id = node_idmap.toConsecutiveId(old_nid)
                delt_x = new_pos[new_node_id][1] - old_pos[old_node_id][1]
                delt_y = new_pos[new_node_id][2] - old_pos[old_node_id][2]
                if abs(delt_x) > 0.001 or abs(delt_y) > 0.001:
                    g = old_pos[old_node_id][0]
                    animate = self._svg.createElement('animateMotion')
                    move = (delt_x, delt_y)
                    time = (0, self._delay)
                    util.add_animate_move_into_node(g, animate, move, time, False)
                    self._node_move.add(old_nid)
            elif old_nid in self._node_disappear:
                # 添加图节点的消失动画效果。
                g = old_pos[old_node_id][0]
                animate = self._svg.createElement('animate')
                util.add_animate_appear_into_node(g, animate, (0, self._delay), False)
        graph = util.find_tag_by_id(self._svg, 'g', 'graph1')
        for old_nid in self._node_appear:
            # 添加图节点的出现动画效果。
            new_node_id = node_idmap.toConsecutiveId(old_nid)
            clone_node = new_pos[new_node_id][0].cloneNode(deep=True)
            graph.appendChild(clone_node)
            animate = self._svg.createElement('animate')
            util.add_animate_appear_into_node(clone_node, animate, (0, self._delay), True)
    
    '''
    功能：获取svg中拓扑图节点的位置坐标（绝对坐标）。
    svg:xmldom.Document 显示的SVG对象。
    '''
    def _get_node_pos_(self, svg):
        graph = util.find_tag_by_id(svg, 'g', 'graph0')
        transform = graph.getAttribute('transform')
        translate_index = transform.find('translate')
        delt_x, delt_y = 0, 0
        if translate_index != -1:
            st = transform.find('(', translate_index)+1
            ed = transform.find(')', translate_index)
            translate = transform[st:ed].split(' ')
            delt_x, delt_y = float(translate[0]), float(translate[1])
        positions = dict()
        nodes = svg.getElementsByTagName('g')
        for node in nodes:
            if node.getAttribute('class') == 'node':
                node_id = int(node.getAttribute('id')[4:])
                ellipse = node.getElementsByTagName('ellipse')[0]
                cx = float(ellipse.getAttribute('cx')) - delt_x
                cy = float(ellipse.getAttribute('cy')) - delt_y
                positions[node_id] = (node, cx, cy)
        return positions
    
    '''
    功能：获取svg中拓扑图的所有边。
    svg:xmldom.Document 显示的SVG对象。
    '''
    def _get_svg_edges_(self, svg):
        edges = dict()
        nodes = svg.getElementsByTagName('g')
        for node in nodes:
            if node.getAttribute('class') == 'edge':
                edge_id = int(node.getAttribute('id')[4:])
                edges[edge_id] = node
        return edges
    
    '''
    功能：更新拓扑图中各个节点的位置。
    返回:xmldom.Document 经过graphviz排版后拓扑图。
    '''
    def _create_svg_(self):
        dot = None
        node_idmap = util.ConsecutiveIdMap(1)
        edge_idmap = util.ConsecutiveIdMap(1)
        if self._directed:
            dot = graphviz.Digraph(format='svg')
        else:
            dot = graphviz.Graph(format='svg')
        if self._horizontal:
            dot.graph_attr['rankdir'] = 'LR'
        dot.node_attr.update(shape='circle', fixedsize='true')
        dot.edge_attr.update(arrowhead='vee')
        for nid, label in self._node_label.items():
            if label is None:
                dot.node(name='{}'.format(nid), shape='circle')
            else:
                dot.node(name='{}'.format(nid), label='{}'.format(label))
            node_idmap.toConsecutiveId(nid)
        for (n1id, n2id) in self._edge_label.keys():
            label = self._edge_label[(n1id, n2id)]
            if label is None:
                dot.edge('{}'.format(n1id), '{}'.format(n2id))
            else:
                dot.edge('{}'.format(n1id), '{}'.format(n2id), label='{}'.format(label))
            edge_idmap.toConsecutiveId((n1id, n2id))
        return (xmldom.parseString(dot._repr_svg_()), node_idmap, edge_idmap)
