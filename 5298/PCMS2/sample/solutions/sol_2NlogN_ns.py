import sys

def make_request(i, j):
    if i == j:
        return 1
    print('?', i, j)
    sys.stdout.flush()
    return int(input())

def find_same_class_binsearch(i):
    l, r = 0, i
    while (r - l > 1):
        m = (l + r) // 2                
        if (make_request(m, i - 1) != make_request(m, i)):
            r = m
        else:
            l = m
    return l

def find_equivalence_classes(n):
    classes = [0] * (n + 1)
    classes[1], num_classes = 1, 1
    for i in range(2, n + 1):
        same_index = find_same_class_binsearch(i)
        #print(same_index)
        num_classes = num_classes + (same_index == 0)
        classes[i] = classes[same_index] if same_index > 0 else num_classes
        
    print("Ready!")
    print(num_classes)
    for i in range(1, n + 1):        
        print(classes[i], end=('\n' if i == n else ' '))
    sys.stdout.flush()

find_equivalence_classes(int(input()))
