def get_pos(a, b, t):
    n = len(a)
    pos = [0] * n
    last = n
    for i in range(n - 1, -1, -1):
        pos[i] = last - 1
        if i > 0 and a[i] + t > b[i - 1]:
            last = i
    return pos


def get_ans(a, t, pos):
    n = len(a)
    bad = [False] * n
    for i in range(0, n):
        if pos[i] != n - 1:
            bad[pos[i] + 1] = True
    b = [a[-1] + t + n] * n
    for i in range(n - 2, -1, -1):
        b[i] = b[i + 1] - 1
        if bad[i + 1]:
            b[i] = min(b[i], a[i + 1] + t - 1)
    return b


def main():
    n, t = map(int, input().split())
    a = list(map(int, input().split()))
    pos = list(map(lambda x: int(x) - 1, input().split()))
    b = get_ans(a, t, pos)
    if get_pos(a, b, t) != pos:
        print('No')
    else:
        print('Yes')
        print(' '.join(map(str, b)))


if __name__ == '__main__':
    main()
