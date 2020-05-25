#!/usr/bin/env python3

'''
@author:zjluestc@outlook.com
@license:GPLv3
'''

from .visual import Visualizer
from .graph import GraphNode, parseGraph, updateEdgeWeight
from .tree import TreeNode, parseTree
from .link_list import ListNode, parseLinkList

__all__ = [
    'Visualizer',
    'GraphNode', 'parseGraph', 'updateEdgeWeight'
    'TreeNode', 'parseTree',
    'ListNode', 'parseLinkList',
]

__title__ = 'algviz'
__version__ = '1.0.2'
__author__ = 'zjluestc@outlook.com'
__license__ = 'GNU General Public License (GPLv3)'

colors = [
    (255, 193, 37),  # Goldenrod
    (221, 160, 221), # Plum
    (202, 255, 112), # DarkOliveGreen
    (176, 226, 255), # LightSkyBlue
    (245, 222, 179), # Wheat
]