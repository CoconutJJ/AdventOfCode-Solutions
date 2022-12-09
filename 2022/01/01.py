from aoc import AdventOfCode


def part1(lines: list[str]):
    print(lines)
    globalMax = 0

    curr = 0

    for l in lines:

        if len(l) == 0:
            globalMax = max(globalMax, curr)
            curr = 0
        else:
            curr += int(l)

    globalMax = max(globalMax, curr)

    return globalMax


def part2(lines: list[str]):

    topThree = []

    total = 0
    for l in lines:

        if len(l) == 0:
            topThree.append(total)
            total = 0
            if len(topThree) > 3:
                topThree.sort(reverse=True)
                topThree = topThree[:-1]
        else:
            total += int(l)

    topThree.append(total)

    if len(topThree) > 3:
        topThree.sort(reverse=True)
        topThree = topThree[:-1]

    return sum(topThree)


AdventOfCode(part1, part2).exec()
