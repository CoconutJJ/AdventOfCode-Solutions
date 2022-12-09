from typing import List
from sys import argv


def part1(lines: List[str]):

    fish = list(map(int, lines[0].split(",")))

    for i in range(80):
        curr = []
        print(i)
        for f in fish:

            if f - 1 < 0:
                curr.append(6)
                curr.append(8)
            else:
                curr.append(f - 1)

        fish = curr

    print("Total fish after 80 days: %d" % len(fish))


def part2(lines: List[str], days: int):

    fish = list(map(int, lines[0].split(",")))

    fishLifeCount = dict()

    for f in fish:

        fishLifeCount[f] = fishLifeCount.get(f, 0) + 1

    for i in range(days):
        newFishCount = dict()
        for f in range(0, 8 + 1):

            if f == 0:
                newFishCount[f] = 0
                newFishCount[6] = newFishCount.get(
                    6, 0) + fishLifeCount.get(f, 0)
                newFishCount[8] = newFishCount.get(
                    8, 0) + fishLifeCount.get(f, 0)
            else:
                newFishCount[f -
                             1] = newFishCount.get(f-1, 0) + fishLifeCount.get(f, 0)

        fishLifeCount = newFishCount

    totalFish = 0

    for i in range(0, 8 + 1):
        totalFish += newFishCount.get(i, 0)

    return totalFish


def fishCount(life, days):

    mem = dict()
    hitCount = 0

    def T(L, D):
        nonlocal hitCount
        if (L, D) not in mem:
            if D == 0:
                mem[(L, D)] = 1
            elif L == 0:
                mem[(L, D)] = T(8, D - 1) + T(6, D - 1)
            else:
                mem[(L, D)] = T(L - min(L, D), D - min(L, D))
        else:
            hitCount += 1

        return mem[(L, D)]

    t = T(life, days)

    return t


def fishCountIter(life, days):

    F = dict()

    for l in range(0, 8 + 1):
        F[(l, 0)] = 1

    for d in range(1, days + 1):
        F[(0, d)] = F[(8, d - 1)] + F[(6, d - 1)]

    for l in range(1, 8 + 1):
        for d in range(1, days + 1):
            F[(l, d)] = F[(l - min(l, d), d - min(l, d))]

    return F[(life, days)]


if __name__ == "__main__":

    fp = open(argv[1], "r")
    lines = fp.readlines()
    lines = [r.strip("\n") for r in lines]

    print(fishCount(8, 0), fishCount(6, 0))
