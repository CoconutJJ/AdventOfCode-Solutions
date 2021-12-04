import re
import sys

fp = open(sys.argv[1], 'r')

moves = fp.readlines()

fwd = re.compile("forward ([0-9]+)")
down = re.compile("down ([0-9]+)")
up = re.compile("up ([0-9]+)")

horizontal = 0
aim = 0
depth = 0

for move in moves:

    if c := fwd.match(move):
        horizontal += int(c.group(1))
        depth += aim * int(c.group(1))
    elif c := down.match(move):
        aim += int(c.group(1))
    elif c := up.match(move):
        aim -= int(c.group(1))

print("Horizontal\t %d" % horizontal)
print("Depth\t\t %d" % depth)
print("Product\t\t %d" % (horizontal * depth))
