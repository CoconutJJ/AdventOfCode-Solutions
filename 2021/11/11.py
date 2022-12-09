from typing import List
from sys import argv
import requests
import os


def inGrid(i, j):
    return (0 <= i < 10) and (0 <= j < 10)


def neighbours(i, j):
    children = [(i-1, j), (i + 1, j), (i, j - 1), (i, j + 1),
                (i-1, j-1), (i-1, j+1), (i+1, j+1), (i+1, j - 1)]

    for (x, y) in children:
        if inGrid(x, y):
            yield (x, y)


def nextState(state: List[List[int]]):

    # newState = [[0 for _ in range(len(state[0]))] for __ in range(len(state))]
    hasFlashed = set()
    visited = set()

    def rec(i, j):
        if (i, j) not in visited:
            state[i][j] += 1
            visited.add((i, j))

        if (i, j) not in hasFlashed:

            if state[i][j] > 9:
                hasFlashed.add((i, j))
                state[i][j] = 0

                for (x, y) in neighbours(i, j):
                    if (x, y) not in hasFlashed:
                        state[x][y] += 1
                        if state[x][y] > 9:
                            rec(x, y)

        for (x, y) in neighbours(i, j):
            if (x, y) not in visited:
                rec(x, y)

    rec(0, 0)

    return state, len(hasFlashed)


def part1(lines: List[str]):

    grid = []

    for l in lines:

        grid.append([int(c) for c in l])

    totalFlashes = 0
    for step in range(100):
        grid, flashes = nextState(grid)
        totalFlashes += flashes

    print("\n".join([str(g) for g in grid]))

    return totalFlashes


def part2(lines: List[str]):
    grid = []

    for l in lines:

        grid.append([int(c) for c in l])

    step = 0

    while True:
        step += 1
        grid, flashes = nextState(grid)

        if flashes == 100:
            return step


# region Fetch Input and Run
YEAR = 2021


def sessionKey():

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
        try:
            inp = input(message)
            inp = inp.strip("\n")

            if inp == "q":
                os._exit(0)

            if inp is None or len(inp) == 0:
                print("invalid input: type q to quit")
                continue
            yield inp
        except GeneratorExit:
            return
        except:
            print("invalid input: type q to quit")


def fetchPuzzleInput():
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
