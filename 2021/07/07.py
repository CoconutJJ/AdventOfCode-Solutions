from typing import List
from sys import argv
import math
import statistics


def part1(lines: List[str]):

    positions = lines[0].split(",")
    positions = list(map(int, positions))
    positions.sort()

    best_position = statistics.median(positions)

    def fuel_use(positions, pos):

        fuel = 0

        for p in positions:
            fuel += abs(p - pos)

        return fuel

    return fuel_use(positions, best_position)


def part2(lines: List[str]):
    positions = lines[0].split(",")
    positions = list(map(int, positions))
    positions.sort()

    def fuel_use(positions, pos):
        fuel = 0
        for p in positions:
            fuel += abs(p - pos) * (abs(p - pos) + 1)/2

        return fuel

    min_fuel = float('inf')

    for y in range(max(positions) + 1):

        min_fuel = min(min_fuel, fuel_use(positions, y))

    return min_fuel


if __name__ == "__main__":

    fp = open(argv[1], "r")
    lines = fp.readlines()
    lines = [r.strip("\n") for r in lines]

    print(part1(lines))
    print(part2(lines))
