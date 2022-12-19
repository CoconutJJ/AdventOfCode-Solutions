from aoc import AdventOfCode


def parse_input(lines: list[str]):
    points = set()
    abyss_y = 0
    for l in lines:
        tokens = l.split(" -> ")
        for start, end in zip(tokens[:-1], tokens[1:]):

            x, y = start.split(",")
            x, y = int(x), int(y)

            s, t = end.split(",")
            s, t = int(s), int(t)

            abyss_y = max(abyss_y, y, t)

            points = points.union(generate_line_coords((x, y), (s, t)))

    return points, abyss_y


def sign(x: int):

    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1


def generate_line_coords(start: tuple[int, int], end: tuple[int, int]):

    line = set()

    s, t = end
    x, y = start
    line.add(start)
    line.add(end)
    dx, dy = (sign(s - x), sign(t - y))

    while x != s or y != t:

        line.add((x, y))
        x += dx
        y += dy

    return line


def neigbours(curr: tuple[int, int]):

    x, y = curr

    yield (x, y + 1)
    yield (x - 1, y + 1)
    yield (x + 1, y + 1)


def part1(lines: list[str]):

    points, abyss_y = parse_input(lines)
    curr = (500, 0)

    def next_step(curr: tuple[int, int]):

        for s, t in neigbours(curr):

            if (s, t) not in points and t <= abyss_y:
                return (s, t)
            elif t > abyss_y:
                return None

        return curr

    particles = 0

    while True:

        abyss = False
        curr = (500, 0)

        while True:

            step = next_step(curr)

            if step == curr:
                break

            if step is None:
                abyss = True
                break

            curr = step

        if abyss:
            break

        points.add(curr)
        particles += 1

    return particles


def part2(lines: list[str]):
    points, abyss_y = parse_input(lines)

    curr = (500, 0)

    abyss_y += 2

    def next_step(curr: tuple[int, int]):

        for s, t in neigbours(curr):

            if t == abyss_y:
                return curr

            if (s, t) not in points:
                return (s, t)

        return curr

    particles = 0

    while True:
        curr = (500, 0)
        while True:
            step = next_step(curr)

            if step == curr:
                break

            curr = step

        points.add(curr)
        particles += 1

        if curr == (500, 0):
            break

    return particles


AdventOfCode(part1, part2).exec()
