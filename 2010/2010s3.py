f = open("s3.8.in", "r")
f.readline()

CIRCUMFERENCE = 1000000


class Group:
    def __init__(self, lengths, left, right):
        self.left = left
        self.right = right
        self.lengths = lengths
        self.len = sum(lengths)

    def combine(self, other):
        return Group(self.lengths + [self.right] + other.lengths, self.left, other.right)

    def combined_lengths(self, other):
        return self.lengths + [self.right] + other.lengths

    def sum_lengths(self, other):
        return self.len + other.len + self.right

    def give(self, other):
        return (Group(self.lengths[:-1], self.left, self.lengths[-1]),
                Group([self.right] + other.lengths, self.lengths[-1], other.right))

    def take(self, other):
        return (Group(self.lengths + [self.right], self.left, other.lengths[0]),
                Group(other.lengths[1:], other.lengths[0], other.right))

    def __str__(self):
        return str(self.left) + ", " + str(self.len) + ", " + str(self.right)


class House:
    def __init__(self, left, right, pos):
        self.left = left
        self.right = right
        self.pos = pos

    def __str__(self):
        return str(self.left) + ", " + str(self.right) + ", " + str(self.pos)


def reduce_groups(groups):
    global hcounter
    if hcounter != hds:
        nlist = []
        for i in range(len(groups[:-1])):
            nlist.append(groups[i].sum_lengths(groups[i+1]))
        m = min(nlist)
        ind = nlist.index(m)
        hcounter -= 1
        groups = reduce_groups(groups[:ind] + [groups[ind].combine(groups[ind+1])] + groups[ind+2:])
    return groups


def optimize(groups):
    save_reduced = groups.copy()
    reduced = groups.copy()
    while True:
        len_groups = [i.len for i in reduced]
        m = max(len_groups)
        ind = len_groups.index(m)
        reduced = attempt_reduce(reduced, ind, m)
        if reduced == -1:
            return save_reduced
        else:
            save_reduced = reduced.copy()


def attempt_reduce(groups, ind, length):
    ind_copy = ind
    groups_copy = groups.copy()
    while ind_copy != 0:
        newg1, newg2 = groups_copy[ind_copy-1].take(groups_copy[ind_copy])

        while newg2.len > length:
            newg1, newg2 = newg1.take(newg2)

        groups_copy = groups_copy[:ind_copy-1] + [newg1, newg2] + groups_copy[ind_copy+1:]

        if newg1.len < length:
            return groups_copy
        ind_copy -= 1

    ind_copy = ind
    groups_copy = groups.copy()
    maximum = len(groups) - 2
    while ind_copy != maximum:
        newg1, newg2 = groups_copy[ind_copy].give(groups_copy[ind_copy + 1])

        while newg1.len > length:
            newg1, newg2 = newg1.give(newg2)

        groups_copy = groups_copy[:ind_copy] + [newg1, newg2] + groups_copy[ind_copy + 2:]
        if newg2.len < length:
            return groups_copy
        ind_copy += 1
    return -1


def is_adjacent(i1, i2, lst):
    return i1 == i2 - 1 or (i1 == 1 and i2 == len(lst)-1)


def get_range(i1, i2, lst):
    if i1 > i2:
        return lst[i1:] + lst[:i2]
    return lst[i1:i2]


def get_next(lst, i, incr):
    return lst[(i+incr) % len(lst)]


lengths = []

adds = []

for l in f:
    adds.append(int(l.strip()))

hds = adds[-1]

adds = adds[:-1]

adds.sort()

lh = None

for h in adds:
    if lh is not None:
        lengths.append(h - lh)

    lh = h

lengths.append(CIRCUMFERENCE + adds[0] - adds[-1])

ind = lengths.index(max(lengths))
lengthsCopy = lengths[ind+1:] + lengths[:ind]
addsCopy = adds[ind+1:] + adds[:ind+1]

house_list = [House(lengthsCopy[i], lengthsCopy[i+1], addsCopy[i+1]) for i in range(len(addsCopy[1:-1]))]
house_list.insert(0, House(0, lengthsCopy[0], addsCopy[0]))
house_list.append(House(lengthsCopy[-1], 0, addsCopy[-1]))

group_list = [Group([], h.left, h.right) for h in house_list]

hcounter = len(group_list)

ans = reduce_groups(group_list)
ans = optimize(ans)

finalans = max([i.len for i in ans])/2
if finalans == int(finalans):
    print(int(finalans))
else:
    print(int(finalans+1))
