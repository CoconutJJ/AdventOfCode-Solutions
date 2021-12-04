
import sys


inp = open(sys.argv[1], "r")

depths = list(map(int, inp.read().splitlines()))

increased = 0

prev = float('inf')

for u, v, w in zip(depths[:-1], depths[1:], depths[2:]):

    if u + v + w > prev:
        increased += 1

    prev = u + v + w

print(increased)
