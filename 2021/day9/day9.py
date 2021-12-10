from typing import List
from sys import argv
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


if __name__ == "__main__":

    fp = open(argv[1], "r")
    lines = fp.readlines()
    lines = [r.strip("\n") for r in lines]
    # print(inputGenerator())
    # part1(lines)
    print(part2(lines))
