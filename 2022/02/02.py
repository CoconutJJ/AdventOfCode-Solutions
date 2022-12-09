from aoc import AdventOfCode
mapping = {
    "A": "X",
    "B": "Y",
    "C": "Z"
}

scores = {
    "X": 1,
    "Y": 2,
    "Z": 3
}


def getScore(opponent, you):
    order = ["X", "Z", "Y"]

    opponent = mapping[opponent]

    if you == opponent:
        return 3 + scores[you]

    losingChoice = order[(order.index(opponent) + 1) % 3]

    if you == losingChoice:
        return scores[you]

    return 6 + scores[you]


def getScorePartTwo(opponent, strategy):
    order = ["A", "C", "B"]
    choice = None
    match strategy:
        case "X":
            choice = order[(order.index(opponent) + 1) % 3]
        case "Y":
            choice = order[order.index(opponent)]
        case "Z":
            choice = order[(order.index(opponent) - 1) % 3]

    return getScore(opponent, mapping[choice])


def part1(lines: list[str]):
    total = 0
    for round in lines:

        (p1, p2) = round.split(" ")
        total += getScore(p1, p2)

    return total


def part2(lines: list[str]):
    total = 0
    for round in lines:

        (p1, p2) = round.split(" ")
        total += getScorePartTwo(p1, p2)

    return total


AdventOfCode(part1, part2).exec()
