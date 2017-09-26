from sort.util import validate


def sort(src: list):
    lens = len(src)
    for x in range(1, lens):
        y = x
        while y >= 1 and src[y] < src[y - 1]:
            src[y], src[y - 1] = src[y - 1], src[y]
            y -= 1


if __name__ == '__main__':
    validate(sort)
