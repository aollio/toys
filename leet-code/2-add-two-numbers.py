"""
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8


"""

__author__ = "Aollio Hou"
__email__ = "aollio@outlook.com"



# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        head = ListNode(0)
        curr = head
        carry = 0
        while l1 is not None or l2 is not None or carry != 0:
            l1val = 0 if l1 is None else l1.val
            l2val = 0 if l2 is None else l2.val
            val = l1val + l2val + carry
            carry = val // 10
            val = val % 10
            next = ListNode(val)
            l1 = None if l1 is None else l1.next
            l2 = None if l2 is None else l2.next
            curr.next = next
            curr = next
        return head.next


def print_node(node):
    while node is not None:
        print(node.val, "", end='')
        node = node.next
    print()


if __name__ == '__main__':
    l1 = ListNode(2)
    l1next = ListNode(4)
    l1nextnext = ListNode(3)

    l1.next = l1next
    l1next.next = l1nextnext

    l2 = ListNode(5)
    l2next = ListNode(6)
    l2nextnext = ListNode(4)

    l2.next = l2next
    l2next.next = l2nextnext

    print_node(l1)
    print_node(l2)
    result_node = Solution().addTwoNumbers(l1, l2)
    print_node(result_node)
