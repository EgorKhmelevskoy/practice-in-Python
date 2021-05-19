sudoky = open('sudoky', encoding='utf8').readlines()
sudoky = list(map(lambda x: list(map(lambda y: int(y), x.strip().replace('', ' ')[1:-1].split())), sudoky))
print(sudoky)
def sudoky_search (sudoky):
    boxes = []
    var = (0, 3, 6)
    i = 0
    k = 0
    n = 3
    while len(boxes) != 9:
        box = []
        N = var[i]
        while len(box) != 9:
            box.extend(sudoky[N][k:n])
            N += 1
        boxes.append(box)
        k += 3
        n += 3
        if len(boxes) % 3 == 0:
            k = 0
            n = 3
            i += 1
    opt = set(tuple(range(1, 10)))
    res = list(map(lambda x: x[:], sudoky))
    while any(list(map(lambda x: 0 in x, res))):
        k = 0
        for i in range(len(sudoky)):
            opt = set(tuple(range(1, 10)))
            if i == 3:
                k = 3
            elif i == 6:
                k = 6
            row = set(res[i])
            if 0 in row:
                row.remove(0)
            for j in range(len(sudoky[i])):
                if res[i][j] == 0:
                    opt = opt - row
                    for r in res:
                        if r[j] in opt:
                            opt.remove(r[j])
                    if j < 3:
                        p = 0
                        opt = opt - set(boxes[k])
                    elif j < 6:
                        p = 1
                        k += p
                        opt = opt - set(boxes[k])
                    else:
                        p = 2
                        k += p
                        opt = opt - set(boxes[k])
                    if len(opt) == 1:
                        res[i][j] = list(opt)[0]
                        n = i % 3 * 3 + j % 3
                        boxes[k][n] = list(opt)[0]
                        row.add(list(opt)[0])
                    elif len(opt) == 2 and n == 'Recursion':
                        res1 = list(map(lambda x: x[:], res))
                        res[i][j] = list(opt)[0]
                        res1[i][j] = list(opt)[1]
                        if type(sudoky_search(res)) == list:
                            return sudoky_search(res)
                        else:
                            return sudoky_search(res1)
                    elif len(opt) == 0:
                        return False
                    k -= p
                    opt = set(tuple(range(1, 10)))
        cur_n = sum(list(map(lambda x: len(list(filter(lambda y: y == 0, x))), sudoky)))
        if cur_n == n:
            n = "Recursion"
        else:
            n = cur_n
    return res
print(sudoky_search(sudoky))











