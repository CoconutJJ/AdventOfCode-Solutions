from aoc import AdventOfCode


class CRT:

    def __init__(self, instructions: list[tuple[str, int]]) -> None:
        self.X = 1
        self.instructions = instructions
        self.cycle = 0
        self.ip = 0
        self.screen = [["." for _ in range(40)] for _ in range(6)]
        self.pixel = 0

    def draw_pixel(self):

        x = self.pixel % 40
        y = self.pixel // 40

        if self.X - 1 <= x <= self.X + 1:
            self.screen[y][x] = '#'

        self.pixel = (self.pixel + 1) % (40 * 6)

    def exec(self):

        while self.ip < len(self.instructions):
            self.cycle += 1
            match self.instructions[self.ip]:
                case ("addx", d):
                    yield (self.cycle, self.X)
                    self.draw_pixel()
                    self.cycle += 1
                    yield (self.cycle, self.X)
                    self.draw_pixel()
                    self.X += d
                case ("noop", _):
                    yield (self.cycle, self.X)
                    self.draw_pixel()
                    

            self.ip += 1

        return True


def part1(lines: list[str]):

    ins = []

    for l in lines:

        if l == "noop":
            ins.append(("noop", 0))
        else:
            i, v = l.split(" ")

            ins.append((i, int(v)))

    crt = CRT(ins)
    total = 0
    for cycle, X in crt.exec():
        # print(cycle, X)
        # print(cycle)
        match cycle:
            case 20:
                # print(cycle, X)
                total += cycle * X
            case 60:
                # print(cycle, X)
                total += cycle * X
            case 100:
                # print(cycle, X)
                total += cycle * X
            case 140:
                # print(cycle, X)
                total += cycle * X
            case 180:
                # print(cycle, X)
                total += cycle * X
            case 220:
                # print(cycle, X)
                total += cycle * X

    return total


def part2(lines: list[str]):

    ins = []

    for l in lines:

        if l == "noop":
            ins.append(("noop", 0))
        else:
            i, v = l.split(" ")

            ins.append((i, int(v)))

    crt = CRT(ins)
    total = 0
    for cycle, X in crt.exec():
        continue

    screen = "\n".join(["".join(l) for l in crt.screen])

    return screen


AdventOfCode(part1, part2).exec()
