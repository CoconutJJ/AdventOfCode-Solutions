from typing import List
from sys import argv
import requests
import os


def is_visible(grid, coord: tuple[int, int]):
    x, y = coord

    if y == 0 or y == len(grid) - 1:
        return True

    if x == 0 or x == len(grid) - 1:
        return True

    left_visible = True

    for i in range(x):
        if grid[y][i] >= grid[y][x]:
            left_visible = False
            break

    if left_visible:
        return True

    top_visible = True

    for i in range(y):

        if grid[i][x] >= grid[y][x]:
            top_visible = False
            break

    if top_visible:
        return True

    right_visible = True

    for i in range(len(grid[0]) - 1, x, -1):
        if grid[y][i] >= grid[y][x]:
            right_visible = False
            break

    if right_visible:
        return True

    bottom_visible = True

    for i in range(len(grid) - 1, y, -1):
        if grid[i][x] >= grid[y][x]:
            bottom_visible = False
            break

    return bottom_visible


def part1(lines: List[str]):

    grid: list[list[int]] = [[int(c) for c in l] for l in lines]

    count = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):

            if is_visible(grid, (x, y)):
                count += 1

    return count


def scenic_score(grid: list[list[int]], coord: tuple[int, int]):
    up = down = left = right = 0
    x, y = coord
    for i in range(x + 1, len(grid[0])):
        right += 1
        if grid[y][x] <= grid[y][i]:
            break
    for i in range(x - 1, -1, -1):
        left += 1
        if grid[y][x] <= grid[y][i]:
            break
    for i in range(y + 1, len(grid)):
        down += 1
        if grid[y][x] <= grid[i][x]:
            break
    for i in range(y - 1, -1, -1):
        up += 1
        if grid[y][x] <= grid[i][x]:
            break

    return up * down * left * right


def part2(lines: List[str]):
    grid: list[list[int]] = [[int(c) for c in l] for l in lines]

    max_scenic_score = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):

            max_scenic_score = max(
                max_scenic_score, scenic_score(grid, (x, y)))

    return max_scenic_score


# region Fetch Input and Run
YEAR = 2022


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
