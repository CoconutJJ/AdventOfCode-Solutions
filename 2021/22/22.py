from typing import List
from sys import argv
import requests
import os
from itertools import count, product


def turn_on(on_cubes: set[tuple[int, int, int]], x_range, y_range, z_range):

    x1, x2 = x_range
    y1, y2 = y_range
    z1, z2 = z_range

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                on_cubes.add((x, y, z))
    return on_cubes


def turn_off(on_cubes: set[tuple[int, int, int]], x_range, y_range, z_range):

    x1, x2 = x_range
    y1, y2 = y_range
    z1, z2 = z_range

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                if (x, y, z) in on_cubes:
                    on_cubes.remove((x, y, z))
    return on_cubes


def within_range(s, t):

    return not (s >= 50 or t <= -50)


def part1(lines: List[str]):
    on_cubes = set()
    for l in lines:

        state, ranges = l.split(" ")
        axis_ranges = ranges.split(",")
        x_range = axis_ranges[0].split("=")[1].split("..")
        y_range = axis_ranges[1].split("=")[1].split("..")
        z_range = axis_ranges[2].split("=")[1].split("..")

        x1, x2 = int(x_range[0]), int(x_range[1])
        y1, y2 = int(y_range[0]), int(y_range[1])
        z1, z2 = int(z_range[0]), int(z_range[1])

        if within_range(x1, x2) and within_range(y1, y2) and within_range(z1, z2):

            if state == "on":

                on_cubes = turn_on(on_cubes,
                                   (max(-50, x1), min(50, x2)),
                                   (max(-50, y1), min(50, y2)),
                                   (max(-50, z1), min(50, z2))
                                   )
            else:
                on_cubes = turn_off(on_cubes,
                                    (max(-50, x1), min(50, x2)),
                                    (max(-50, y1), min(50, y2)),
                                    (max(-50, z1), min(50, z2))
                                    )

    return len(on_cubes)


def volume(cube):

    vol = 1

    for (s, t) in cube:

        vol *= (t - s + 1)

    return vol


def intersect(i1, i2):
    x, y = i1
    s, t = i2

    if not (s >= y or t <= x):
        return (max(x, s), min(y, t))
    else:
        return None


def overlap(cube1, cube2):

    x, y, z = cube1
    u, v, w = cube2

    bounds = []

    for r, t in ((x, u), (y, v), (z, w)):
        if intersect(r, t) is None:
            return None
        else:
            bounds.append(intersect(r, t))

    return tuple(bounds)


def part2(lines: List[str]):

    all_ranges = []

    for l in lines:

        state, ranges = l.split(" ")
        axis_ranges = ranges.split(",")
        x_range = axis_ranges[0].split("=")[1].split("..")
        y_range = axis_ranges[1].split("=")[1].split("..")
        z_range = axis_ranges[2].split("=")[1].split("..")

        x1, x2 = int(x_range[0]), int(x_range[1])
        y1, y2 = int(y_range[0]), int(y_range[1])
        z1, z2 = int(z_range[0]), int(z_range[1])

        all_ranges.append((state, ((x1, x2), (y1, y2), (z1, z2))))

    counts = dict()

    for [state, q] in all_ranges:
        overlaps = []
        for c in counts:

            o = overlap(q, c)

            if o is None:
                continue
            overlaps.append(o)

        for v in overlaps:
            counts[v] = -1

        counts[q] = 1

    total_vol = 0
    for cube in counts:
        print(volume(cube))
        total_vol += volume(cube) * counts[cube]

    return total_vol


# region Fetch Input and Run
YEAR = 2021


def sessionKey():
    """
        Move up the dir. tree until we see a file named SESSION. Then read
        the session key.
    """
    cwd = os.getcwd()
    curr = cwd
    while not os.path.exists("SESSION"):
        os.chdir(curr := os.path.join(curr, ".."))
        if curr == "/":
            print("Could not find SESSION file!")
            exit(1)

    key = open("SESSION", "r")
    os.chdir(cwd)
    return key.read().strip("\n")


def prompt(message):
    while True:

        inp = input(message)
        inp = inp.strip("\n")

        if inp == "q":
            os._exit(0)

        if inp is None or len(inp) == 0:
            print("invalid input: type q to quit")
            continue

        yield inp


def fetchPuzzleInput():
    """

    """
    print("Fetching puzzle input...")

    if os.path.isfile("input.txt"):
        print("Using cached input...")
        fp = open("input.txt", "r")
        lines = fp.readlines()
        lines = [r.strip("\n") for r in lines]
        return lines

    s = requests.Session()

    s.cookies.set("session", sessionKey(), domain=".adventofcode.com")

    filename, _ = argv[0].split(".")

    dayNo = None

    if filename.startswith("day"):
        try:
            dayNo = int(filename[3:])
        except:
            dayNo = None

    if dayNo is None:
        for dayNo in prompt("Error parsing day number. Please enter the day number: "):
            try:
                dayNo = int(dayNo)
            except:
                print("Invalid Day Number")
                continue

            break

    URL = "https://adventofcode.com/%d/day/%d/input" % (YEAR, dayNo)

    # pretend to be linux firefox...
    body = s.get(URL, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0"
    })

    fp = open("input.txt", "w")
    fp.write(body.content.decode("utf-8"))
    fp.close()

    lines = body.content.decode("utf-8").splitlines()
    lines = [r.strip("\n") for r in lines]

    return lines


if __name__ == "__main__":

    if len(argv) < 2:
        lines = fetchPuzzleInput()
    else:
        fp = open(argv[1], "r")
        lines = fp.readlines()
        lines = [r.strip("\n") for r in lines]

    for part in prompt("Which part to run ? [1 (default)/2]: "):

        part = part.strip("\n")

        if len(part) == 0:
            print(part1(lines))
            break

        try:
            part = int(part)
        except:
            print("Invalid part number")
            continue

        if part == 1:
            print(part1(lines))
        elif part == 2:
            print(part2(lines))
        else:
            print("Invalid part number")
            continue

        break
# endregion
