#!/usr/bin/env python3

"""
Merge two sorted linked lists and return it as a new list.
The new list should be made by splicing together the nodes of the first two lists.
"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x, next=None):
        self.val = x
        self.next = next

    def __str__(self):
        node = self
        list = []
        while node is not None:
            list.append(node.val)
            node = node.next
        return ' '.join(map(lambda x: str(x), list))

    __repr__ = __str__


class Solution(object):
    def mergeTwoLists(self, l1: ListNode, l2: ListNode):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        l1por = l1
        l2por = l2
        root = ListNode(None)
        node = root

        while l1por is not None and l2por is not None:
            if l2por.val > l1por.val:
                node.next = l1por
                l1por = l1por.next
            else:
                node.next = l2por
                l2por = l2por.next
            node = node.next
        if l1por is None:
            node.next = l2por

        if l2por is None:
            node.next = l1por
        return root.next


def parse(nums: list):
    root = ListNode(None)
    node = root
    for num in nums:
        node.next = ListNode(num)
        node = node.next
    return root.next


def assert_eq(node: ListNode, nums: list):
    nums = list(nums)
    while node is not None:
        assert node.val == nums[0]
        nums.pop(0)
        node = node.next
    assert len(nums) == 0


def test_merge(list1: list, list2: list):
    l1 = parse(list1)
    l2 = parse(list2)

    res = Solution().mergeTwoLists(l1, l2)
    list1.extend(list2)
    assert_eq(res, sorted(list1))


if __name__ == '__main__':
    test_merge([1, 3, 5], [2, 4, 6, 8])
    test_merge([2], [1])
