
from os import EX_USAGE
from typing import Callable, Tuple


class Navigator:

    def __init__(self) -> None:
        super().__init__()
        self.ship_pos = 0, 0
        self.waypoint_pos = 1, 10

    def rotateCounterClockwise(self, x, y):

        return -y, x

    def rotateClockWise(self, x, y):

        return self.compose(
            self.rotateCounterClockwise,
            self.compose(self.rotateCounterClockwise,
                         self.rotateCounterClockwise)
        )(x, y)

    def compose(self, f, g):

        return lambda *args: f(*g(*args))

    def north(self, v):
        i, j = self.waypoint_pos

        self.waypoint_pos = i + v, j

    def south(self, v):
        self.north(-v)

    def east(self, v):
        i, j = self.waypoint_pos

        self.waypoint_pos = i, j + v

    def west(self, v):
        self.east(-v)

    def forward(self, v):
        si, sj = self.ship_pos

        wi, wj = self.waypoint_pos

        dx, dy = wi - si, wj - sj

        self.ship_pos = (si + v*dx, sj + v*dy)

        si, sj = self.ship_pos

        self.waypoint_pos = si + dx, sj + dy

    def R(self, v):

        wi, wj = self.waypoint_pos

        si, sj = self.ship_pos

        tx, ty = wi - si, wj - sj

        for r in range(v//90):

            tx, ty = self.rotateClockWise(tx, ty)

        self.waypoint_pos = tx + si, ty + sj

    def L(self, v):
        wi, wj = self.waypoint_pos

        si, sj = self.ship_pos

        tx, ty = wi - si, wj - sj

        for r in range(v//90):

            tx, ty = self.rotateCounterClockwise(tx, ty)

        self.waypoint_pos = tx + si, ty + sj


def mandist(L):

    nav = Navigator()
    for s, v in L:

        if s == "F":
            nav.forward(v)
        elif s == "L":
            nav.L(v)
        elif s == "R":
            nav.R(v)
        elif s == "N":
            nav.north(v)
        elif s == "E":
            nav.east(v)
        elif s == "S":
            nav.south(v)
        elif s == "W":
            nav.west(v)

    x, y = nav.ship_pos

    print(abs(x) + abs(y))


with open("input.txt", "r") as f:
    instructions = []
    for l in f.readlines():
        l = l.strip('\n')
        instructions.append((l[0], int(l[1:])))

    mandist(instructions)
