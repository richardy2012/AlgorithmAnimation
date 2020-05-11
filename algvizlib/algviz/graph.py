#!/usr/bin/env python3

'''
图节点定义。
'''
class GraphNode():
    def __init__(self, val, neighbors=list()):
        self.val = val
        self.neighbors = neighbors
        
    def _neighbor_(self):
        res = list()
        for child in self.children:
            res.append((child, None))
        return res

'''
图节点跟踪器定义。
'''
class GraphTrace():
    pass
