from aoc import AdventOfCode
from typing import Callable


class Monkey:

    def __init__(self, items: list[int], op: Callable[[int], int], div: int) -> None:

        self.items = items
        self.op = op
        self.div = div
        self.true_monkey: Monkey = None
        self.false_monkey: Monkey = None
        self.inspections = 0

    def add_item(self, v):
        self.items.append(v)

    def process(self):

        for v in self.items:
            self.inspections += 1

            worry = self.op(v) // 3

            if worry % self.div == 0:
                self.true_monkey.add_item(worry % 9699690)
            else:
                self.false_monkey.add_item(worry % 9699690)

        self.items = []

    def process_no_worry(self):
        for v in self.items:
            self.inspections += 1
            worry = self.op(v)

            if worry % self.div == 0:
                self.true_monkey.add_item(worry % 9699690)
            else:
                self.false_monkey.add_item(worry % 9699690)

        self.items = []


def part1(lines: list[str]):

    monkeys = [Monkey([57], lambda r: r * 13, 11),
               Monkey([58, 93, 88, 81, 72, 73, 65], lambda r: r + 2, 7),
               Monkey([65, 95], lambda r: r + 6, 13),
               Monkey([58, 80, 81, 83], lambda r: r * r, 5),
               Monkey([58, 89, 90, 96, 55], lambda r: r + 3, 3),
               Monkey([66, 73, 87, 58, 62, 67], lambda r: r * 7, 17),
               Monkey([85, 55, 89], lambda r: r + 4, 2),
               Monkey([73, 80, 54, 94, 90, 52, 69, 58], lambda r: r + 7, 19)
               ]

    monkeys[0].true_monkey = monkeys[3]
    monkeys[0].false_monkey = monkeys[2]
    monkeys[1].true_monkey = monkeys[6]
    monkeys[1].false_monkey = monkeys[7]
    monkeys[2].true_monkey = monkeys[3]
    monkeys[2].false_monkey = monkeys[5]
    monkeys[3].true_monkey = monkeys[4]
    monkeys[3].false_monkey = monkeys[5]
    monkeys[4].true_monkey = monkeys[1]
    monkeys[4].false_monkey = monkeys[7]
    monkeys[5].true_monkey = monkeys[4]
    monkeys[5].false_monkey = monkeys[1]
    monkeys[6].true_monkey = monkeys[2]
    monkeys[6].false_monkey = monkeys[0]
    monkeys[7].true_monkey = monkeys[6]
    monkeys[7].false_monkey = monkeys[0]

    for r in range(20):

        for i in range(8):
            monkeys[i].process()

    inspections = []

    for i in range(8):
        inspections.append(monkeys[i].inspections)

    inspections.sort(reverse=True)

    return inspections[0] * inspections[1]


def part2(lines: list[str]):
    monkeys = [Monkey([57], lambda r: r * 13, 11),
               Monkey([58, 93, 88, 81, 72, 73, 65], lambda r: r + 2, 7),
               Monkey([65, 95], lambda r: r + 6, 13),
               Monkey([58, 80, 81, 83], lambda r: r*r, 5),
               Monkey([58, 89, 90, 96, 55], lambda r: r + 3, 3),
               Monkey([66, 73, 87, 58, 62, 67], lambda r: r * 7, 17),
               Monkey([85, 55, 89], lambda r: r + 4, 2),
               Monkey([73, 80, 54, 94, 90, 52, 69, 58], lambda r: r + 7, 19)
               ]

    monkeys[0].true_monkey = monkeys[3]
    monkeys[0].false_monkey = monkeys[2]
    monkeys[1].true_monkey = monkeys[6]
    monkeys[1].false_monkey = monkeys[7]
    monkeys[2].true_monkey = monkeys[3]
    monkeys[2].false_monkey = monkeys[5]
    monkeys[3].true_monkey = monkeys[4]
    monkeys[3].false_monkey = monkeys[5]
    monkeys[4].true_monkey = monkeys[1]
    monkeys[4].false_monkey = monkeys[7]
    monkeys[5].true_monkey = monkeys[4]
    monkeys[5].false_monkey = monkeys[1]
    monkeys[6].true_monkey = monkeys[2]
    monkeys[6].false_monkey = monkeys[0]
    monkeys[7].true_monkey = monkeys[6]
    monkeys[7].false_monkey = monkeys[0]

    for r in range(10000):
        for i in range(8):
            monkeys[i].process_no_worry()

    inspections = []

    for i in range(8):
        inspections.append(monkeys[i].inspections)

    print(inspections)

    inspections.sort(reverse=True)

    return inspections[0] * inspections[1]


AdventOfCode(part1, part2).exec()
