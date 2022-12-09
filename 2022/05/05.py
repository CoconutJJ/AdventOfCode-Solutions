from aoc import AdventOfCode
import re


def part1(lines: list[str]):

    regex = re.compile("move (\d+) from (\d+) to (\d+)")

    stacks = {
        1: ["L", "N", "W", "T", "D"],
        2: ["C", "P", "H"],
        3: ["W", "P", "H", "N", "D", "G", "M", "J"],
        4: ["C", "W", "S", "N", "T", "Q", "L"],
        5: ["P", "H", "C", "N"],
        6: ["T", "H", "N", "D", "M", "W", "Q", "B"],
        7: ["M", "B", "R", "J", "G", "S", "L"],
        8: ["Z", "N", "W", "G", "V", "B", "R", "T"],
        9: ["W", "G", "D", "N", "P", "L"]
    }

    for l in lines:

        if "move" not in l:
            continue

        amount, fr, dest = regex.match(l).groups()
        amount, fr, dest = int(amount), int(fr), int(dest)

        end_index = len(stacks[fr]) - amount
        removed = reversed(stacks[fr][end_index:])

        stacks[fr] = stacks[fr][:end_index]
        stacks[dest].extend(removed)

    word = ""

    for i in range(1, 10):

        word += stacks[i][-1]

    return word


def part2(lines: list[str]):
    regex = re.compile("move (\d+) from (\d+) to (\d+)")

    stacks = {
        1: ["L", "N", "W", "T", "D"],
        2: ["C", "P", "H"],
        3: ["W", "P", "H", "N", "D", "G", "M", "J"],
        4: ["C", "W", "S", "N", "T", "Q", "L"],
        5: ["P", "H", "C", "N"],
        6: ["T", "H", "N", "D", "M", "W", "Q", "B"],
        7: ["M", "B", "R", "J", "G", "S", "L"],
        8: ["Z", "N", "W", "G", "V", "B", "R", "T"],
        9: ["W", "G", "D", "N", "P", "L"]
    }

    for l in lines:

        if "move" not in l:
            continue

        amount, fr, dest = regex.match(l).groups()
        amount, fr, dest = int(amount), int(fr), int(dest)

        end_index = len(stacks[fr]) - amount
        removed = stacks[fr][end_index:]

        stacks[fr] = stacks[fr][:end_index]
        stacks[dest].extend(removed)

    word = ""

    for i in range(1, 10):

        word += stacks[i][-1]

    return word


AdventOfCode(part1, part2).exec()
