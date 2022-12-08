from typing import List
from sys import argv
import requests
import os
from random import randint

def inputGenerator():
    for _ in range(100):
        row = [str(randint(0, 9)) for _ in range(100)]
        print("".join(row))

def part1(lines: List[str]):

    grid = []

    for l in lines:
        grid.append(list(map(int, [c for c in l])))

    def inGrid(i, j):

        return (0 <= i < len(grid)) and (0 <= j < len(grid[i]))

    def neighbours(i, j):

        n = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]

        for x, y in n:
            if inGrid(x, y):
                yield (x, y)

    lowPointsRiskSum = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            isLower = True
            for x, y in neighbours(i, j):
                if grid[i][j] >= grid[x][y]:
                    isLower = False
                    break

            if isLower:
                lowPointsRiskSum += grid[i][j] + 1
    return lowPointsRiskSum


def part2(lines: List[str]):
    grid = []
    for l in lines:
        grid.append(list(map(int, [c for c in l])))

    def inGrid(i, j):
        return (0 <= i < len(grid)) and (0 <= j < len(grid[i]))

    def neighbours(i, j):

        n = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]

        for x, y in n:
            if inGrid(x, y):
                yield (x, y)

    def bfs(i, j):

        q = [(i, j)]    
        visited = set()
        visited.add((i,j))
        size = 1
        while len(q) != 0:

            x, y = q.pop(0)

            for s, t in neighbours(x, y):

                if (grid[x][y] < grid[s][t]) and ((s, t) not in visited) and (grid[s][t] != 9):
                    q.append((s, t))
                    visited.add((s,t))
                    size += 1
        
        return size

    top3 = []

    for i in range(len(grid)):
        for j in range(len(grid[i])):

            isLowPoint = True
            for x,y in neighbours(i,j):
                if grid[i][j] >= grid[x][y]:
                    isLowPoint = False

            if not isLowPoint:
                continue

            if grid[i][j] != 9:
                top3.append(bfs(i,j))
            
    top3.sort(reverse=True)

    return top3

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
            while (dayNo := input(
                    "Error parsing day number. Please enter the day number: ")):
                try:
                    dayNo = int(dayNo)
                    break
                except:
                    print("Invalid Day Number")
                    continue

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

    while (part := input("Which part to run ? [1 (default)/2]: ")):

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
