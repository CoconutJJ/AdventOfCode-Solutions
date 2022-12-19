from aoc import AdventOfCode


def compare(left: list | int, right: list | int):

    if type(left) == list and type(right) == list:

        for i in range(min(len(left), len(right))):

            if (v := compare(left[i], right[i])) == 0:
                continue

            return v

        if len(left) < len(right):
            return 1
        elif len(left) > len(right):
            return -1
        else:
            return 0

    if type(left) == int and type(right) == int:

        if left < right:
            return 1
        if left > right:
            return -1

        return 0

    if type(left) == int:
        left = [left]

    elif type(right) == int:
        right = [right]

    return compare(left, right)


def part1(lines: list[str]):

    packets = []
    total = 0
    idx = 1
    for l in lines:

        if len(l) == 0:
            assert len(packets) == 2

            if compare(packets[0], packets[1]) == 1:
                total += idx

            idx += 1
            packets = []
        else:
            packets.append(eval(l))

    return total


def qsort(items: list):

    if len(items) == 0:
        return []

    pivot = len(items)//2

    left = []

    right = []

    for i, item in enumerate(items):

        if i == pivot:
            continue

        if compare(item, items[pivot]) >= 1:
            left.append(item)
        else:
            right.append(item)

    return qsort(left) + [items[pivot]] + qsort(right)


def part2(lines: list[str]):

    packets = []

    for l in lines:
        if len(l) == 0:
            continue
        packets.append(eval(l))

    packets.append([[2]])
    packets.append([[6]])

    packets = qsort(packets)

    return "\n".join(str(r) for r in packets)


AdventOfCode(part1, part2).exec()
