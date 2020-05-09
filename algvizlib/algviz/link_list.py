#!/usr/bin/env python3

'''
前向链表节点定义。
'''
class ForwardListNode():
    def __init__(self, val):
        self.val = val
        self.next = None

    def _neighbors_(self):
        return (self.next)
        
'''
前向链表跟踪器定义。
'''
class ForwardListTrace():
    pass

'''
双向链表节点定义。
'''
class DoublyListNode():
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None
        
    def _neighbors_(self):
        return (self.prev, self.next)

'''
双向链表跟踪器定义。
'''
class DoublyListTrace():
    pass
