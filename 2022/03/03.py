from aoc import AdventOfCode


def priority(c):

    if ord('a') <= ord(c) <= ord('z'):
        return ord(c) - ord('a') + 1
    elif ord('A') <= ord(c) <= ord('Z'):
        return ord(c) - ord('A') + 27
    else:
        raise ValueError("must be a-z or A-Z")


def part1(lines: list[str]):
    total = 0
    for l in lines:

        half = len(l)//2

        left = set([c for c in l[:half]])

        right = set([c for c in l[half:]])

        intersect = left.intersection(right)
        for p in intersect:
            total += priority(p)

    return total


def part2(lines: list[str]):
    group = []

    total = 0

    for l in lines:

        group.append(set([c for c in l]))

        if len(group) == 3:

            intersect = group[0].intersection(group[1]).intersection(group[2])

            for p in intersect:
                total += priority(p)

            group = []

    return total


AdventOfCode(part1, part2).exec()
