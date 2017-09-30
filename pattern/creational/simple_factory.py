#!/usr/bin/env python3

"""
Simple Factory Pattern.
The Factory Method pattern can be create a interface for a method, leave the implementation to the class
that gets instantiated.
"""

__author__ = 'Aollio Hou'
__email__ = 'aollio@outlook.com'


class Student:
    def show(self):
        print('Student')


class Teacher:
    def show(self):
        print('Teacher')


class SimpleFactory:
    @staticmethod
    def create(desc):
        if desc == 'teacher':
            return Teacher()
        elif desc == 'student':
            return Student()
        else:
            raise NotImplementedError()


def usage():
    a, b = SimpleFactory.create(desc='student'), SimpleFactory.create(desc='teacher')
    for x in a, b:
        x.show()


if __name__ == '__main__':
    usage()
