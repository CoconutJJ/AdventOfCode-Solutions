from aoc import AdventOfCode


def part1(lines: list[str]):
    l = lines[0]

    for i in range(4, len(l)):
        if len(set([c for c in l[i-4: i]])) == 4:
            return i


def part2(lines: list[str]):
    l = lines[0]

    for i in range(14, len(l)):
        if len(set([c for c in l[i-14: i]])) == 14:
            return i


AdventOfCode(part1, part2).exec()
