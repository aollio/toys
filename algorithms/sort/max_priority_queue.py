import sort.util as util

"""
优先队列
"""


class MaxPriorityQueue(object):
    """
    优先队列
    插入时维持次序
    """

    def __init__(self):
        self.__items = [0]

    def insert(self, item):
        """
        插入一个对象，插入时需要维持次序，使用上浮来维持
        :param item: 
        :return: 
        """
        self.__items.append(item)
        self.come_up()

    def come_up(self):
        items = self.__items
        if self.is_empty():
            return
        last = len(items) - 1
        parent = last // 2
        while parent != 0 and items[last] > items[parent]:
            util.swap(items, parent, last)
            last = parent
            parent = last // 2

    def max(self):
        return self.__items[1]

    def del_max(self):
        val = self.__items.pop(1)
        new = self.__items.pop(-1)
        self.__items.insert(1, new)
        self.sink()
        return val

    def sink(self):
        items = self.__items
        new = 1

        while new <= self.size() // 2:
            j = 2 * new
            if j < self.size() and items[j] < items[j + 1]:
                j += 1

            if not items[new] < items[j]:
                break

            util.swap(items, new, j)
            new = j

    def is_empty(self):
        if len(self.__items) == 1:
            return True
        else:
            return False

    def size(self):
        return len(self.__items) - 1

    def __len__(self):
        return len(self.__items) - 1

    def print(self):
        print(self.__items)


if __name__ == '__main__':
    queue = MaxPriorityQueue()

    init = [10, 5, 9, 2, 3, 5, 6, 1, 1, 1, 2, 4, 3, 1, 2]
    for x in init:
        queue.insert(x)
    queue.print()
    queue.del_max()
    queue.print()
    queue.del_max()
    queue.print()
    # queue.insert(8)
    queue.del_max()
    queue.print()
