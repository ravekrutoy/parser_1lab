import sys


def make_request(i, j):
    if i == j:
        return 1
    print('?', i, j)
    sys.stdout.flush()
    return int(input())


MAXN = 50 * 1000
classes = [0] * (MAXN + 1)

SQRTN = int(MAXN ** 0.5) + 1
sqrts = [0] * SQRTN
rightmost_position = [0] * (MAXN + 1)


def add(index, value):
    rightmost_position[index] += value
    sqrt_idx = index // SQRTN
    sqrts[sqrt_idx] += value


def find_unique(l, r):
    a = l // SQRTN
    b = r // SQRTN
    result = 0
    for i in range(a + 1, b):
        result += sqrts[i]

    for i in range(l, min((a + 1) * SQRTN, r + 1)):
        result += rightmost_position[i]

    if a != b:
        for i in range(max(l, b * SQRTN), r + 1):
            result += rightmost_position[i]    
    return result


def find_same_class(i):
    l, r = 0, i
    while (r - l > 1):
        m = (l + r) // 2
        if (make_request(m, i) == find_unique(m, i - 1) + 1):
            r = m
        else:
            l = m
    return l


def find_equivalence_classes(n):
    classes[1], num_classes = 1, 1
    add(1, 1)
    for i in range(2, n + 1):        
        same_index = find_same_class(i)
        num_classes = num_classes + (same_index == 0)
        classes[i] = classes[same_index] if same_index > 0 else num_classes
        if same_index > 0:
            add(same_index, -1)        
        add(i, 1)
        
    print("Ready!")
    print(num_classes)
    for i in range(1, n + 1):        
        print(classes[i], end=('\n' if i == n else ' '))
    sys.stdout.flush()


n = int(input())
find_equivalence_classes(n)
