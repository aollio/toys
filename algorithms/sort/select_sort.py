from sort.util import validate

"""
select sort
"""


def sort(src: list):
    lens = len(src)
    for x in range(lens):
        mini = x
        for y in range(x, lens):
            if src[y] < src[mini]:
                mini = y
        src[x], src[mini] = src[mini], src[x]


if __name__ == '__main__':
    validate(sort)
