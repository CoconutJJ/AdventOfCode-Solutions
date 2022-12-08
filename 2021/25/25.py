import os
from sys import argv
from typing import List

import requests


def part1(lines: List[str]):
    grid = []

    for r in lines:
        grid.append([c for c in r])

    width = len(grid[0])
    height = len(grid)

    def rightStep(x, y):

        return (x + 1) % width, y

    def printGrid(g):
        print("\n".join(["".join(r) for r in g]))

    def downStep(x, y):
        return x, (y + 1) % height

    def computeMove(init):

        hasMoved = False
        eastMovedState = [["." for x in range(width)] for y in range(height)]
        for y in range(height):
            for x in range(width):

                if init[y][x] == ">":
                    r, t = rightStep(x, y)

                    if init[t][r] == ".":
                        eastMovedState[t][r] = ">"
                        hasMoved = True
                        continue
                        
                if eastMovedState[y][x] == ".":
                    eastMovedState[y][x] = init[y][x]
        


        finalState = [["." for x in range(width)] for y in range(height)]

        for y in range(height):
            for x in range(width):

                if eastMovedState[y][x] == "v":
                    r, t = downStep(x, y)

                    if eastMovedState[t][r] == ".":
                        finalState[t][r] = "v"
                        hasMoved = True
                        continue
                
                if finalState[y][x] == ".":
                    finalState[y][x] = eastMovedState[y][x]

        return finalState, hasMoved

    step = 0

    moved = True

    while moved:
        grid, moved = computeMove(grid)
        step += 1

    return step


def part2(lines: List[str]):
    pass


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
