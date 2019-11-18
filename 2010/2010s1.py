f = open("s1.7.in", "r")
f.readline()
scores = [0, 0]
names = {0: []}
l = None
for l in f:
    name, R, S, D = l.strip().split()
    R = int(R)
    S = int(S)
    D = int(D)
    score = 2 * R + 3 * S + D
    if score > scores[0]:
        if score != scores[1]:
            names[score] = [name]
        else:
            names[score].append(name)
        scores[0] = score
    elif score == scores[0]:
        names[score].append(name)
    scores.sort()

if l is not None:
    if len(names[scores[1]]) > 1:
        n = names[scores[1]]
        n.sort()
        print(n[0])
        print(n[1])
    else:
        print(names[scores[1]][0])
        if len(names[scores[0]]) > 1:
            n = names[scores[0]]
            n.sort()
            n = n[0]
            print(n)
        elif len(names[scores[0]]) == 1:
            n = names[scores[0]][0]
            print(n)
