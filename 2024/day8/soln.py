import sys
from math import gcd


def distsqr(x, y):

    t1, t2 = x
    s1, s2 = y

    return (t1 - s1) ** 2 + (t2 - s2) ** 2


def smallest_integer_vector(x):

    u, v = x

    if u == 0:
        return (0, 1)
    elif v == 0:
        return (1, 0)

    return (u // gcd(u, v), v // gcd(u, v))


def antinode_points_twice_distance(width, height, antennas):

    antinodes = set()
    for x in range(width):
        for y in range(height):
            for antenna in antennas:
                for p in antennas[antenna]:

                    if p == (x, y):
                        continue

                    u, v = p

                    du, dv = u - x, v - y

                    if (u + du, v + dv) in antennas[antenna]:
                        antinodes.add((x, y))

                    if (x - 2 * du, y - 2 * dv) in antennas[antenna]:
                        antinodes.add((x, y))

    return len(antinodes)


def antinode_points_any_distance(width, height, antennas):

    def in_grid(x):

        a, b = x

        return 0 <= a < width and 0 <= b < height

    antinode_points = set()
    for antenna in antennas:

        for p1 in antennas[antenna]:

            for p2 in antennas[antenna]:

                if p1 == p2:
                    continue

                s1, s2 = p1
                t1, t2 = p2

                du, dv = s1 - t1, s2 - t2

                du, dv = smallest_integer_vector((du, dv))

                x, y = s1, s2
                while in_grid((x, y)):
                    antinode_points.add((x, y))
                    x += du
                    y += dv

                x, y = s1, s2

                while in_grid((x, y)):
                    antinode_points.add((x, y))
                    x -= du
                    y -= dv

    return len(antinode_points)


if __name__ == "__main__":

    with open(sys.argv[1], "r") as f:

        antennas = dict()

        lines = f.readlines()

        for y, l in enumerate(lines):

            for x, c in enumerate(l.strip()):

                if c == ".":
                    continue

                if c not in antennas:
                    antennas[c] = set()

                antennas[c].add((x, y))

        width = len(lines[0].strip())
        height = len(lines)

        print(antinode_points_any_distance(width, height, antennas))
