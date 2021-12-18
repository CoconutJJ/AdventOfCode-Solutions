from typing import List
from sys import argv
import requests
import os
import math

hasUpdate = False

class Node:

    def __init__(self, value, left, right) -> None:
        self.parent = None
        self.left = left
        self.right = right
        self.value = value

def createBT(p):

    if type(p) == int:
        return Node(p, None, None)

    l = p[0]
    r = p[1]

    lnode = createBT(l)
    rnode = createBT(r)
    parent = Node(None, lnode, rnode)
    lnode.parent = parent
    rnode.parent = parent

    return parent

def addPair(l: Node, r: Node):
    node = Node(None, l, r)
    l.parent = node
    r.parent = node
    return node

def addLeftSibling(target: Node, value: int):
    orig = target
    while (target.left is None or target.left is orig):
        orig = target
        target = target.parent

        if target is None:
            return

    target = target.left

    while target.right is not None:
        target = target.right

    target.value += value

def addRightSibling(target: Node, value: int):
    orig = target

    while (target.right is None or target.right is orig):
        orig = target
        target = target.parent

        if target is None:
            return

    target = target.right

    while target.left is not None:
        target = target.left

    target.value += value

# no splits before explode
def reduceExplode(root: Node, depth=0):
    global hasUpdate

    if root is None:
        return root

    if hasUpdate:
        return root

    if depth == 4 and root.value is None:

        l = root.left
        r = root.right

        if l.value is not None and r.value is not None:
            addLeftSibling(l, l.value)
            addRightSibling(r, r.value)
            hasUpdate = True
            return Node(0, None, None)

    l = reduceExplode(root.left, depth + 1)
    r = reduceExplode(root.right, depth + 1)
    if l is not None:
        l.parent = root

    if r is not None:
        r.parent = root

    root.left = l
    root.right = r

    return root


def reduceSplit(root: Node, depth=0):

    global hasUpdate

    if root is None:
        return root

    if hasUpdate:
        return root

    if root.value is not None:

        if root.value >= 10:

            lval = math.floor(root.value/2)
            rval = math.ceil(root.value/2)

            lnode = Node(lval, None, None)
            rnode = Node(rval, None, None)

            parent = Node(None, lnode, rnode)

            lnode.parent = parent
            rnode.parent = parent

            hasUpdate = True

            return parent

    l = reduceSplit(root.left, depth + 1)
    r = reduceSplit(root.right, depth + 1)
    if l is not None:
        l.parent = root

    if r is not None:
        r.parent = root

    root.left = l
    root.right = r
    return root


def createPairList(root: Node):
    if root.value is None:
        return [createPairList(root.left), createPairList(root.right)]
    else:
        return root.value


def magnitude(pairs):

    if type(pairs) == int:
        return pairs

    return 3 * magnitude(pairs[0]) + 2 * magnitude(pairs[1])


def part1(lines: List[str]):
    global hasUpdate
    curr = None
    for l in lines:
        pairs = eval(l)

        if curr is None:
            curr = createBT(pairs)
            continue

        bt = createBT(pairs)

        curr = addPair(curr, bt)

        while True:

            curr = reduceExplode(curr)

            if hasUpdate:
                hasUpdate = False
                continue

            curr = reduceSplit(curr)

            if hasUpdate:
                hasUpdate = False
                continue

            break

    print(magnitude(createPairList(curr)))

    return curr


def part2(lines: List[str]):
    global hasUpdate
    maxMagnitude = float("-inf")
    for s in lines:
        for t in lines:
            p1, p2 = eval(s), eval(t)

            curr = addPair(createBT(p1), createBT(p2))

            while True:

                curr = reduceExplode(curr)

                if hasUpdate:
                    hasUpdate = False
                    continue

                curr = reduceSplit(curr)

                if hasUpdate:
                    hasUpdate = False
                    continue

                break

            maxMagnitude = max(maxMagnitude, magnitude(createPairList(curr)))

    return maxMagnitude


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
