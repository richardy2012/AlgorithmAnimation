# 笔记本目录

## 经典算法

+ [排序算法](经典算法/排序算法.ipynb) （插入排序、冒泡排序、快排、快速排序、归并排序、堆排序、桶排序）
+ [字符串匹配算法](经典算法/字符串匹配算法.ipynb) （朴素字符串匹配、KMP算法）
+ [二分查找算法](经典算法/二分查找算法.ipynb) （折半查找）
+ [二分图匹配算法](经典算法/二分图匹配算法.ipynb) （匈牙利算法、KM算法）TODO
+ [拓扑排序算法](经典算法/拓扑排序算法.ipynb) （Kahn's 算法、深度优先搜索、DFS）
+ [求拓扑图的最短路径算法] TODO
+ [极大极小值算法] TODO

## 数据结构

+ [并查集介绍](数据结构/并查集.ipynb) （Uion Find）

## 经典编程题

+ [lc200.岛屿数量](经典编程题/lc200.岛屿数量.ipynb) （并查集）
+ [lc11.盛最多水的容器](经典编程题/lc11.盛最多水的容器.ipynb) （滑动窗口、双指针）
+ [lc300.最长上升子序列](经典编程题/lc300.最长上升子序列.ipynb) （动态规划、数组）
+ [lc1143.最长公共子序列](经典编程题/lc1143.最长公共子序列.ipynb) （动态规划、字符串）
+ [lc105.从前序与中序遍历序列构造二叉树](经典编程题/lc105.从前序与中序遍历序列构造二叉树.ipynb) （二叉树、前序遍历、中序遍历、递归）
+ [递归算法-N皇后](经典编程题/递归算法-N皇后.ipynb) （递归，8皇后）
+ [最大流问题](经典编程题/最大流问题.ipynb) TODO
+ [最小生成树问题] TODO
+ [动态规划-钢条切割] TODO
+ [动态规划-矩阵乘法] TODO

## 游戏相关

+ [二维网格寻路算法](游戏相关/二维网格寻路算法.ipynb) （广度优先搜索、BFS、A\*算法、最短路径）
+ [汉诺塔游戏](游戏相关/汉诺塔.ipynb) （递归、套娃）
+ [2048游戏](游戏相关/2048.ipynb) （数字游戏、休闲）

----------

# 环境搭建

## 安装 jupyter notebook

[jupyter notebook](https://jupyter.org) 是一款写代码或文档的神器，推荐使用 Anaconda 的方式进行安装更加方便，下面是网上的一些安装教程，可以参考一下：

+ Windows 版本安装教程：https://zhuanlan.zhihu.com/p/32320214
+ Mac 版本安装教程：https://zhuanlan.zhihu.com/p/33105153
+ Linux 版本安装教程：https://blog.csdn.net/jenyzhang/article/details/73275232
+ 搭建云服务器（体验最好）：https://zhuanlan.zhihu.com/p/44405596

## 安装 graphviz

[graphviz](https://graphviz.gitlab.io) 是一款强大的开源拓扑图布局库，本仓库中代码的运行需要依赖该库，可以参考以下教程进行安装：

+ Windows 版本安装教程：https://zhuanlan.zhihu.com/p/69185415
+ Mac 版本安装教程：https://blog.csdn.net/skyztttt/article/details/71601365
+ Linux 版本安装教程：https://blog.csdn.net/caiandyong/article/details/44408831

## 关于 algvizlib

`algvizlib` 是由本人独立开发的的数据结构可视化 **python** 库，基于 **jupyter notebook** 和 **graphviz 拓扑图可视化库**。它提供一组接口用于操作一维向量(vector)、二维表格(table)、链表(link_list)、二叉树(tree)、拓扑图(graph)等数据结构，并**根据数据内容的变化生成直观的动画效果，可以在常用的浏览器中渲染显示**。

*本笔记中的许多算法代码都使用了 `algvizlib` 来进行可视化，用于加深对算法的理解。* 

使用该库，你可以方便的展示自己的[排序算法](经典算法/排序算法.ipynb)的运行过程，下图是冒泡排序的动画效果：

<img src = 'https://ftp.bmp.ovh/imgs/2020/10/c0585e4414aa2c77.gif' algin=center width="358" height="270"/>

也可以直观的观察自己在解决编程题时所写出来的奇怪逻辑（[leetcode.105题.从前序与中序遍历序列构造二叉树](经典编程题/lc105.从前序与中序遍历序列构造二叉树.ipynb)）

<img src = 'https://pic.downk.cc/item/5f953e8f1cd1bbb86b909348.gif' algin=center width="409" height="568"/>

甚至可以写一些简单的游戏来玩[2048游戏](游戏相关/2048.ipynb)😄。

<img src = 'https://ftp.bmp.ovh/imgs/2020/10/1e83cb4fddbbe93c.gif' algin=center width="291" height="311"/>

*另外，由于开发时间仓促，代码中可能存在一些 bug，希望能够帮忙指出，一些额外的功能也欢迎提出建议*。

## 安装 algvizlib

`algvizlib` 库位于代码仓库的 `algvizlib/` 文件夹下面，具体的接口使用可参考 [algvizlib接口使用说明](algvizlib/接口使用说明.ipynb)。 `algvizlib` 需要在 **Python3** 的环境下运行，且需要 `graphviz` 动态链接库的支持。该库的安装方法比较简单，在各系统的命令行工具中执行以下命令即可：

1. `cd 仓库目录/AlgorithmAnimation/algvizlib/release/dev`
2. `python3 setup.py install`
