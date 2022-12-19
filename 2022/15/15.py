from aoc import AdventOfCode
from re import compile, match

ROW_Y = 2000000


def get_interval(scanner: tuple[int, int], beacon: tuple[int, int], row: int):

    sx, sy = scanner
    bx, by = beacon

    M = abs(bx - sx) + abs(by - sy)

    a = abs(row - sy) - M + sx
    b = M - abs(row - sy) + sx

    if a > b:
        return None

    return (a, b)


def merge(s: tuple[int, int], t: tuple[int, int]):

    sx, sy = s
    tx, ty = t

    if not (sy < tx or ty < sx):
        return (min(tx, sx), max(sy, ty))
    else:
        return None


def merge_interval(intervals: list[tuple[int, int]], v: tuple[int, int]):

    new_intervals = []

    curr = v

    for r in intervals:

        if (s := merge(curr, r)) is not None:
            curr = s
        else:
            new_intervals.append(r)

    new_intervals.append(curr)
    new_intervals.sort(key=lambda r: r[0])

    return new_intervals


def part1(lines: list[str]):

    pattern = compile(
        "Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

    intervals = []

    beacons = set()

    for l in lines:

        matches = match(pattern, l)
        groups = matches.groups()

        sx, sy = int(groups[0]), int(groups[1])

        bx, by = int(groups[2]), int(groups[3])

        if by == ROW_Y:
            beacons.add((bx, by))

        v = get_interval((sx, sy), (bx, by), ROW_Y)

        if v is not None:
            intervals = merge_interval(intervals, v)

    total = 0
    for (x, y) in intervals:
        total += y - x + 1

        for bx, by in beacons:
            if x <= bx <= y:

                total -= 1

    return total


def part2(lines: list[str]):
    pattern = compile(
        "Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")

    for y in range(0, 4000000):
        intervals = []

        beacons = set()
        for l in lines:

            matches = match(pattern, l)
            groups = matches.groups()

            sx, sy = int(groups[0]), int(groups[1])

            bx, by = int(groups[2]), int(groups[3])

            if by == y:
                beacons.add((bx, by))

            v = get_interval((sx, sy), (bx, by), y)

            if v is not None:
                intervals = merge_interval(intervals, v)

        print(y, intervals)

    pass


AdventOfCode(part1, part2).exec()
