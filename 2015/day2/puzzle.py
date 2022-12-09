

from typing import List
import sys


def totalArea(dims: List[int]):

    dimensions = list(map(int, dims.split("x")))
    dimensions.sort()
    a, b, c = dimensions

    return 2 * a + 2 * b + a*b*c


def totalWrappingPaperArea(inp: str):

    boxes = inp.splitlines()

    SA = 0

    for b in boxes:

        SA += totalArea(b)

    return SA


fp = open(sys.argv[1], "r")

print(totalWrappingPaperArea(fp.read()))
