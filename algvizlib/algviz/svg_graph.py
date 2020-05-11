#!/usr/bin/env python3

import graphviz
import xml.dom.minidom as xmldom
import utility as util

class SvgGraph(): 
    '''
    root:... 拓扑图的根节点，用于初始化拓扑图（可以是图/树/链表的节点）。
    directed:bool 表示拓扑图是否为有向图。
    delay:float 动画延时时长。
    '''
    def __init__(self, root, directed, delay):
        self._directed = directed       # 拓扑图是否为有向图。
        self._delay = delay             # 每帧动画的延时时长。
        self._node_label = dict()       # 拓扑图每个节点上要显示的标签信息。
        self._edge_label = dict()       # 拓扑图每条边上要显示的标签信息。
        self._node_tcs = dict()         # 记录所有节点中的轨迹访问信息（节点索引：ColorStack）信息。
        self._node_appear = set()       # 记录下一帧动画中消失的节点索引。
        self._node_disappear = set()    # 记录下一帧动画中消失的节点索引。
        self._frame_trace_old = list()  # 缓存上一帧需要清除的节点相关信息（节点索引，轨迹颜色值）。
        self._frame_trace = list()      # 记录下一帧待刷新的节点相关信息(节点索引，轨迹颜色值，是否持久化)。
        self._trace_color = set()       # 记录现存的所有跟踪器的颜色（方便为下一个跟踪器分配颜色）。
        self._svg = None                # 将要显示的拓扑图的svg对象。
        self._node_idmap = None         # 实际节点id值和graphviz中对应节点的id值。
        self._edge_idmap = None         # 实际节点对的id值和graphviz中对应边的id值。
        if root is not None:
            self.add_node(root, None, True)
        (self._svg, self._node_idmap, self._edge_idmap) = self._create_svg_()

    '''
    node:... 要添加的节点对象，可以是拓扑图/树/链表节点。
    parent:... node的父节点对象，需要与node的类型一致。
    recursive:bool 是否递归的添加和node相关联的节点。
    '''
    def add_node(self, node, parent, recursive):
        visited = {id(parent)}
        node_stack = [node]
        temp_edge_label = list()
        if parent is not None:
            for neigh in parent._neighbors_():
                if id(neigh[0]) == id(node):
                    temp_edge_label.append(id(parent), id(node), neigh[1])
        while len(node_stack) > 0:
            cur_node = node_stack.pop()
            if id(cur_node) in visited:
                continue
            visited.add(id(cur_node))
            self._node_label[id(cur_node)] = cur_node.val
            self._node_tcs[id(cur_node)] = util.TraceColorStack()
            self._node_appear.add(id(cur_node))
            if recursive:
                for neigh in cur_node._neighbors_():
                    temp_edge_label.append(id(cur_node), id(neigh[0]), neigh[1])
                    node_stack.append(neigh[0])
        for (n1id, n2id, label) in temp_edge_label:
            self._edge_label[(n1id, n2id)] = label
    
    '''
    node:... 要删除的节点对象，可以是拓扑图/树/链表节点。
    recursive:bool 是否递归的删除和node相关联的节点。
    '''
    def delete_node(self, node, recursive):
        visited = set()
        node_stack = [node]
        while len(node_stack) > 0:
            cur_node = node_stack.pop()
            if id(cur_node) in visited:
                continue
            visited.add(id(cur_node))
            self._node_label.pop(id(cur_node))
            self._node_tcs.pop(id(cur_node))
            self._node_disappear.add(id(cur_node))
            if recursive:
                for neigh in cur_node._neighbors_():
                    node_stack.append(neigh[0])
        temp_remove_edges = list()
        for (n1id, n2id) in self._edge_label.keys():
            if n1id in self._node_disappear or n2id in self._node_disappear:
                temp_remove_edges.append((n1id, n2id))
        for k in temp_remove_edges:
            self._edge_label.pop(k)
        
    '''
    node:... 跟踪器访问的节点，可以是拓扑图/树/链表节点。
    color:(R,G,B) 跟踪器的颜色。
    hold:bool 是否保留轨迹颜色。
    '''
    def visit_node(self, node, color, hold):
        self._node_tcs[id(node)].add(color)
        self._frame_trace.append((id(node), color, hold))
    
    '''
    color:(R,G,B) 将要被删除的跟踪器颜色。
    hold:bool 是否保留轨迹颜色。
    '''
    def delete_trace(self, color, hold):
        if hold:
            for nid in self._node_label.keys():
                if self._node_tcs[nid].remove(color):
                    self._update_svg_color_(nid, self._node_tcs[nid].color())
        self._trace_color.remove(color)
    
    '''
    返回:str 拓扑图SVG显示字符串。
    '''
    def __repr_svg__(self):
        # 更新节点跟踪器的颜色。
        for (nid, color) in self._frame_trace_old:
            self._cell_tcs[nid].remove(color)
            node_id = 'node{}'.format(self._node_idmap.toConsecutiveId(nid))
            self._update_svg_color_(node_id, self._cell_tcs[nid].color())
        self._frame_trace_old.clear()
        for (nid, color, hold) in self._frame_trace:
            node_id = 'node{}'.format(self._node_idmap.toConsecutiveId(nid))
            self._update_svg_color_(node_id, self._cell_tcs[nid].color())
            if not hold:
                self._frame_trace_old.append((rid, color))
        self._frame_trace.clear()
        if len(self._node_appear)==0 and len(self._node_disappear)==0:
            return self._svg.toxml()
        # 对拓扑图进行重新排版并添加动画效果。
        (new_svg, node_idmap, edge_idmap) = self._create_svg_()
        self._update_svg_nodes_(new_svg, node_idmap)
        self._update_svg_edges_(new_svg, edge_idmap)
        self._node_appear.clear()
        self._node_disappear.clear()
        res = self._svg.toxml()
        # 更新SVG内容，为下一帧做准备。
        self._svg, self._node_idmap, self._edge_idmap = new_svg, node_idmap, edge_idmap
        for nid in self._node_tcs.keys():
            node_id = 'node{}'.format(self._node_idmap.toConsecutiveId(nid))
            self._update_svg_color_(node_id, self._node_tcs[nid].color())
        return res
    
    '''
    node_id:str 要更新的拓扑图节点ID值。
    color:(R,G,B) 新的颜色值。
    '''
    def _update_svg_color_(self, node_id, color):
        node = util.find_tag_by_id(self._svg, 'g', node_id)
        if node is not None:
            ellipse = g.getElementsByTagName('ellipse')[0]
            ellipse.setAttribute('fill', util.rgbcolor2str(color))
            text = g.getElementsByTagName('text')[0]
            if text is not None:
                text.setAttribute('fill', util.auto_text_color(color))
    
    '''
    功能：向SVG中添加所有与节点有关的动画。
    edge_idmap:ConsecutiveIdMap 边在内存中的ID和在SVG中的ID的双向映射关系。
    new_svg:xmldom.Document 最新的SVG对象。
    '''
    def _update_svg_edges_(self, new_svg, edge_idmap):
        old_edges = self._get_svg_edges_(self._svg)
        new_edges = self._get_svg_edges_(new_svg)
        pass
    
    '''
    功能：向SVG中添加所有与边有关的动画。
    node_idmap:ConsecutiveIdMap 节点在内存中的ID和在SVG中的ID的双向映射关系。
    new_svg:xmldom.Document 最新的SVG对象。
    '''
    def _update_svg_nodes_(self, new_svg, node_idmap):
        old_pos = self._get_node_pos_(self._svg)
        new_pos = self._get_node_pos_(new_svg)
        for old_node_id in old_pos.keys():
            old_nid = self._node_idmap.toAttributeId(old_node_id)
            if old_nid in self._node_appear:
                new_node_id = 'node{}'.format(node_idmap.toConsecutiveId(old_nid))
                clone_node = new_pos[new_node_id].cloneNode(deep=True)
                graph = util.find_tag_by_id(self._svg, 'g', 'graph0')
                graph.appendChild(clone_node)
                animate = self._svg.createElement('animate')
                util.add_animate_appear_into_node(clone_node, animate, (0, self._delay), True)
            elif old_nid in node_idmap.keys():
                new_node_id = 'node{}'.format(node_idmap.toConsecutiveId(old_nid))
                delt_x = new_pos[new_node_id][1] - old_pos[old_node_id][1]
                delt_y = new_pos[new_node_id][2] - old_pos[old_node_id][2]
                if abs(delt_x) > 0.001 or abs(delt_y) > 0.001:
                    g = old_pos[old_node_id][0]
                    animate = self._svg.createElement('animateMotion')
                    move = (delt_x, delt_y)
                    time = (0, self._delay)
                    util.add_animate_move_into_node(g, animate, move, time)
            elif old_nid in self._node_disappear:
                g = old_pos[old_node_id][0]
                animate = self._svg.createElement('animate')
                util.add_animate_appear_into_node(g, animate, (0, self._delay), False)
    
    '''
    功能：获取svg中拓扑图节点的位置坐标。
    svg:xmldom.Document 显示的SVG对象。
    '''
    def _get_node_pos_(self, svg):
        positions = dict()
        nodes = svg.getElementsByTagName('g')
        for node in nodes:
            if node.getAttribute('class') == 'node':
                node_id = int(node.getAttribute('id')[4:])
                ellipse = g.getElementsByTagName('ellipse')[0]
                cx = float(ellipse.getAttribute('cx'))
                cy = float(ellipse.getAttribute('cy'))
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
        for (nid, label) in self._node_label:
            if label is None:
                dot.node(name='{}'.format(nid), shape='circle')
            else:
                dot.node(name='{}'.format(nid), label=label, shape='circle')
            node_idmap.toConsecutiveId(nid)
        for (n1id, n2id) in self._edge_label.keys():
            label = self._edge_label[(n1id, n2id)]
            if label is None:
                dot.edge('{}'.format(n1id), '{}'.format(n2id))
            else:
                dot.edge('{}'.format(n1id), '{}'.format(n2id), label=label)
            edge_idmap.toConsecutiveId((n1id, n2id))
        return (minidom.parseString(dot._repr_svg()), node_idmap, edge_idmap)
