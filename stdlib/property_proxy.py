class A:

    def __init__(self):
        self._a = None
        self._b = 10

    @property
    def a(self):
        print('get_a')
        return self._a

    @a.setter
    def a(self, value):
        print('set_a')
        self._a = value

    def __getattr__(self, item):
        print('getattr', item)
        return self.__dict__[item]


class B:
    def __init__(self, tar):
        self.a = tar

    @property
    def __getattr__(self, item):
        return self.a.__dict__


from lazy_object_proxy import Proxy
b = B(A())
b.a
print(b._b)
print(b.c)
