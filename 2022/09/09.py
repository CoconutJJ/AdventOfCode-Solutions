from aoc import AdventOfCode


class Rope:

    def __init__(self, N: int) -> None:
        self.knots = [(0, 0) for _ in range(N)]
        self.old = (0, 0)
        self.tail_positions = set()

    def up(self):
        hx, hy = self.knots[0]

        hy += 1
        self.old = (hx, hy - 1)
        self.knots[0] = (hx, hy)
        self.update()

    def down(self):
        hx, hy = self.knots[0]

        hy -= 1
        self.old = (hx, hy + 1)
        self.knots[0] = (hx, hy)
        self.update()

    def left(self):
        hx, hy = self.knots[0]

        hx -= 1
        self.old = (hx + 1, hy)
        self.knots[0] = (hx, hy)
        self.update()

    def right(self):
        hx, hy = self.knots[0]

        hx += 1
        self.old = (hx - 1, hy)
        self.knots[0] = (hx, hy)
        self.update()

    def update(self):
        new_rope = [tuple(self.knots[0])]
        curr = tuple(self.knots[0])

        for tail in self.knots[1:]:

            if not self.is_adjacent(curr, tail):
                dx, dy = self.compute_tail_move(curr, tail)
                tx, ty = tail
                new_rope.append((tx + dx, ty + dy))
                self.old = tail
            else:
                new_rope.append(tail)

            curr = new_rope[-1]

        self.knots = new_rope
        self.tail_positions.add(self.knots[-1])

    def _sign(self, x: int):

        if x < 0:
            return -1
        elif x == 0:
            return 0
        else:
            return 1

    def compute_tail_move(self, head: tuple[int, int], tail: tuple[int, int]):
        hx, hy = head
        tx, ty = tail

        dx = hx - tx
        dy = hy - ty

        return (self._sign(dx), self._sign(dy))

    def is_adjacent(self, head: tuple[int, int], tail: tuple[int, int]):
        hx, hy = head
        tx, ty = tail

        dx = abs(hx - tx)
        dy = abs(hy - ty)

        if dx > 1:
            return False

        if dy > 1:
            return False

        return True


def simulate_rope(movements: list[str], length: int):
    r = Rope(length)

    for l in movements:
        match l.split(" "):
            case ["R", d]:
                d = int(d)

                while d > 0:
                    r.right()
                    d -= 1

            case ["L", d]:
                d = int(d)

                while d > 0:
                    r.left()
                    d -= 1

            case ["U", d]:
                d = int(d)

                while d > 0:
                    r.up()
                    d -= 1

            case ["D", d]:
                d = int(d)

                while d > 0:
                    r.down()
                    d -= 1

    return len(r.tail_positions)


def part1(lines: list[str]):
    return simulate_rope(lines, 2)


def part2(lines: list[str]):
    return simulate_rope(lines, 10)


AdventOfCode(part1, part2, day=9).exec()
