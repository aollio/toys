from sort.util import validate
'''
bobble sort algorithm
'''


def sort(src: list):
    lens = len(src)
    for x in range(lens - 1, -1, -1):
        for y in range(x):
            if src[y] > src[y + 1]:
                src[y], src[y + 1] = src[y + 1], src[y]


# print(list(range(5,-1,-1)))

# a = [9, 3, 21, 34, 12, 2]
# print(sort(a), a)

if __name__ == '__main__':
    validate(sort)
