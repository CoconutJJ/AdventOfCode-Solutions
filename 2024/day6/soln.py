import sys


def rotate(v: tuple[int, int]):

    a, b = v

    return (-b, a)


def distinct_positions(start_pos, height: int, width: int, barriers: set):

    def in_grid(pos: tuple[int, int]):

        x, y = pos

        return 0 <= x < width and 0 <= y < height

    unique_positions = set()

    direction = (0, -1)
    while in_grid(start_pos):
        unique_positions.add(start_pos)

        x, y = start_pos
        dx, dy = direction
        new_pos = (x + dx, y + dy)

        if new_pos in barriers:
            direction = rotate(direction)
        else:
            start_pos = new_pos

    return len(unique_positions)


def distinct_loop_barriers(start_pos, height: int, width: int, barriers: set):

    def in_grid(pos: tuple[int, int]):

        x, y = pos

        return 0 <= x < width and 0 <= y < height

    def in_loop(barrier: tuple[int, int]):

        unique_positions = dict()

        direction = (0, -1)
        curr_pos = start_pos
        while in_grid(curr_pos):

            if curr_pos in unique_positions and unique_positions[curr_pos] == direction:
                return True

            x, y = curr_pos
            dx, dy = direction
            new_pos = (x + dx, y + dy)

            if new_pos in barriers or new_pos == barrier:
                direction = rotate(direction)
            else:
                unique_positions[curr_pos] = direction
                curr_pos = new_pos
        return False

    total = 0

    for x in range(0, width):
        for y in range(0, height):

            if (x, y) in barriers:
                continue

            if (x, y) == start_pos:
                continue

            if in_loop((x, y)):
                total += 1

    return total


if __name__ == "__main__":

    with open(sys.argv[1], "r") as f:

        barriers = set()
        start_pos = (-1, -1)

        lines = f.readlines()

        for y, l in enumerate(lines):

            for x, c in enumerate(l):

                if c == "#":
                    barriers.add((x, y))
                elif c == "^":
                    start_pos = (x, y)
                else:
                    continue

        height = len(lines)
        width = len(lines[0])

        print(distinct_loop_barriers(start_pos, height, width, barriers))
