from sort.util import validate


def sort(src: list):
    lens = len(src)
    h = 1
    while h < lens // 3:
        h = h * 3 + 1

    while h >= 1:
        for x in range(h, lens):
            for y in range(x, lens):
                while (y - h) >= 0 and src[y - h] > src[y]:
                    src[y - h], src[y] = src[y], src[y - h]
        h = h // 3


if __name__ == '__main__':
    validate(sort)
