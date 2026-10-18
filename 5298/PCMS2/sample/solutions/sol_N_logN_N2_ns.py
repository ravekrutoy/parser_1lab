import sys


def make_request(i, j):
    if i == j:
        return 1
    print('?', i, j)
    sys.stdout.flush()
    return int(input())


MAXN = 50 * 1000
classes = [0] * (MAXN + 1)


def find_unique(l, r):
    seen = [False] * (n + 1)
    result = 0
    for i in range(l, r + 1):
        if not seen[classes[i]]:
            result += 1
            seen[classes[i]] = True
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
    for i in range(2, n + 1):
        same_index = find_same_class(i)
        num_classes = num_classes + (same_index == 0)
        classes[i] = classes[same_index] if same_index > 0 else num_classes
        
    print("Ready!")
    print(num_classes)
    for i in range(1, n + 1):        
        print(classes[i], end=('\n' if i == n else ' '))
    sys.stdout.flush()


n = int(input())
find_equivalence_classes(n)
