#!/usr/bin/env python3

# 图节点定义。
class GraphNode():
    def __init__(self, val, neighbors=list(), weights=None):
        self.val = val
        self.neighbors = neighbors
        self.weights = weights
    
    '''
    返回：所有邻居节点和邻居边的权重值。
    '''
    def _neighbors_(self):
        res = list()
        for i in range(len(self.neighbors)):
            if weights is None:
                res.append((self.neighbors[i], None))
            else:
                res.append((self.neighbors[i], self.weights[i]))
        return res

    '''
    返回：图节点中邻居的数量。
    '''
    def __len__(self):
        return len(self.neighbors)
    
# 图节点跟踪器定义。
class GraphTrace():
    '''
    node:GraphNode 初始化跟踪拓扑图的节点。
    graph:SvgGraph 绑定要显示的图对象。
    color:(R,G,B) 跟踪器所在节点的RGB背景颜色。
    hold:bool 是否一直保留轨迹。
    '''
    def __init__(self, node, graph, color, hold):
        self._graph = graph
        self._node = node
        self._color = color
        self._hold = hold
    
    '''
    node:GraphNode 为跟踪器绑定新的拓扑图节点。
    '''
    def __call__(self, node):
        super().__setattr__('_node', node)
        self._graph.add_node(node, None, False)
        return self._node

    def __eq__(self, other):
        return super().__getattribute__('_node') == other
    
    def __ne__(self, other):
        return super().__getattribute__('_node') != other 
    
    def __getattribute__(self, name):
        if name == 'val':
            self._graph.trace_visit(super().__getattribute__('_node'), super().__getattribute__('_color'), super().__getattribute__('_hold'))
            return super().__getattribute__('_node').val
        else:
            return super().__getattribute__(name)
    
    def __setattr__(self, name, value):
        if name == 'val':
            setattr(self._node, 'val', value)
            self._graph.trace_visit(super().__getattribute__('_node'), super().__getattribute__('_color'), super().__getattribute__('_hold'))
        else:
            super().__setattr__(name, value)
