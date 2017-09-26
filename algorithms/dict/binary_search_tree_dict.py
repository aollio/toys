#!/usr/bin/env python3


from collections import Iterable

from interface import SortedDictInterface, DictInterface
from dictutil import test_dict

"""
二叉查找树
"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class BinarySearchTreeDict(DictInterface):
    class Node:
        def __init__(self, key=None, value=None, left=None, right=None):
            self.key = key
            self.value = value
            self.left = left
            self.right = right

        def __len__(self):
            length = 1
            if self.left is not None:
                length += len(self.left)
            if self.right is not None:
                length += len(self.right)
            return length

    class ItemIterator:
        def __init__(self, root):
            self.root = root
            self.nodes = []
            self.trans_root_to_nodes(self.root)

        def trans_root_to_nodes(self, root):
            if root is None:
                return
            self.nodes.append(root)
            self.trans_root_to_nodes(root.right)
            self.trans_root_to_nodes(root.left)

        def __iter__(self):
            for node in self.nodes:
                yield node.key, node.value

    def __init__(self, **kwargs):
        self.root = None
        super(BinarySearchTreeDict, self).__init__(**kwargs)

    def __setitem__(self, key, value):
        self.root = self.__setitem_from_root(self.root, key, value)

    def __setitem_from_root(self, root, key, value):
        if root is None:
            return self.Node(key=key, value=value)

        if root.key == key:
            root.value = value
            return root
        elif root.key > key:
            # key belong the left tree of root
            root.left = self.__setitem_from_root(root.left, key, value)
            return root
        elif root.key < key:
            root.right = self.__setitem_from_root(root.right, key, value)
            return root

    def __getitem__(self, key):
        return self.__getitem(self.root, key)

    def __getitem(self, root, key):
        if root is None:
            raise AttributeError
        if root.key == key:
            return root.value
        elif root.key < key:
            return self.__getitem(root.right, key)
        else:
            return self.__getitem(root.left, key)

    def del_min(self):
        self.root = self.__del_min(self.root)

    def __del_min(self, node):
        """删除给定树中最小的节点, 然后返回这棵树"""
        if node.left is None:
            return node.right
        node.left = self.__del_min(node.left)
        return node

    def __delitem__(self, key):
        self.root = self.__delitem(self.root, key)

    def __delitem(self, root, key):
        """删除给定树中给定的键, 然后返回这棵树"""
        # if root is None, means key not exist
        if root is None:
            return None
        # the key is root's right child tree
        if root.key < key:
            root.right = self.__delitem(root.right, key)
            return root
        # the key is root's left child tree
        elif root.key > key:
            root.left = self.__delitem(root.left, key)
            return root
        # find the key
        # root.key == key
        if root.right is None:
            # the key only have left children tree
            return root.left
        elif root.left is None:
            # the key only have right children tree
            return root.right

        # root的左子树最大的叶子节点
        # 先获取右子树最小的节点
        min = self.__min(root.right)
        # 然后删除最小节点
        min.right = self.__del_min(root.right)
        # 链接. 将min 和将要删除的节点 替换
        min.left = root.left
        return min

    def __min(self, root):
        if root is None:
            return None
        if root.left is None:
            return root
        else:
            return self.__min(root.left)

    def __max(self, root):
        if root is None:
            return None
        if root.right is None:
            return root
        else:
            return self.__max(root.right)

    def __len__(self):
        if self.root is None:
            return 0
        return len(self.root)

    def items(self) -> Iterable:
        return self.ItemIterator(self.root)


if __name__ == '__main__':
    test_dict(BinarySearchTreeDict())
