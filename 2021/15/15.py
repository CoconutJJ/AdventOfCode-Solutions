from typing import List
from sys import argv
import requests
import os
import heapq


def djikstra(N, M, cost):

    def neighbours(x, y):
        return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    def inGrid(x, y):
        return (0 <= x < N) and (0 <= y < M)

    pq = []
    dist = dict()

    for i in range(M):
        for j in range(N):
            heapq.heappush(pq, (float('inf'), (j, i)))
            dist[(j, i)] = float('inf')

    heapq.heappush(pq, (0, (0, 0)))

    dist[(0, 0)] = 0

    removed = set()

    while len(removed) != N * M:

        p, (x, y) = heapq.heappop(pq)
        removed.add((x, y))
        for i, j in neighbours(x, y):

            if (i, j) not in removed and inGrid(i, j):

                alt = p + cost(i, j)

                if dist[(i, j)] > alt:

                    dist[(i, j)] = alt

                    heapq.heappush(pq, (alt, (i, j)))

    return dist[(N - 1, M - 1)]


def part1(lines: List[str]):

    grid = []

    for l in lines:
        grid.append([int(c) for c in l])

    def cost(i,j):
        return grid[j][i]

    return djikstra(len(grid[0]), len(grid), cost)

def part2(lines: List[str]):
    grid = []

    for l in lines:
        grid.append([int(c) for c in l])


    def calcRiskLevel(i, j):

        x = i//(len(grid[0]))
        y = j//(len(grid))

        i = i % len(grid[0])
        j = j % len(grid)

        cost = (grid[j][i] + x + y - 1) % 9 + 1

        return cost

    return djikstra(len(grid[0]) * 5, len(grid) * 5, calcRiskLevel)


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
