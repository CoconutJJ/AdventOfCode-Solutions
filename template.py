from typing import List
from sys import argv


def part1(lines: List[str]):
    pass

def part2(lines: List[str]):
    pass

if __name__ == "__main__":

    fp = open(argv[1], "r")
    lines = fp.readlines()
    lines = [r.strip("\n") for r in lines]

    part1(lines)
    part2(lines)



