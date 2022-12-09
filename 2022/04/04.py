from aoc import AdventOfCode


def contains(a: tuple[int, int], b: tuple[int, int]):
    s, t = a
    x, y = b
    return x <= s <= t <= y


def containsUnordered(a: tuple[int, int], b: tuple[int, int]):

    return contains(a, b) or contains(b, a)


def overlap(a: tuple[int, int], b: tuple[int, int]):
    s, t = a
    x, y = b

    return not (t < x or y < s)


def part1(lines: list[str]):

    total = 0
    for l in lines:

        a, b = l.split(",")

        s, t = a.split("-")

        x, y = b.split("-")

        if containsUnordered((int(s), int(t)), (int(x), int(y))):
            total += 1

    return total


def part2(lines: list[str]):

    total = 0
    for l in lines:

        a, b = l.split(",")

        s, t = a.split("-")

        x, y = b.split("-")

        if overlap((int(s), int(t)), (int(x), int(y))):
            total += 1

    return total


AdventOfCode(part1, part2).exec()
