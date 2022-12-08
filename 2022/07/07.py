from typing import List
from sys import argv
import requests
import os


class File:

    def __init__(self, name) -> None:
        self.parent = None
        self.name = name
        self.size = 0
        self.children: list[File] = []


def buildFileTree(lines: list[str]):
    root = File("/")
    root.parent = root
    curr = None
    for l in lines:

        command = l.split(" ")

        match command:
            case ["$", "cd", ".."]:
                curr = curr.parent
            case ["$", "cd", "/"]:
                curr = root
            case ["$", "cd", r]:
                for f in curr.children:
                    if f.name == r:
                        curr = f
            case ["$", "ls"]:
                continue
            case ["dir", d]:
                f = File(d)
                f.parent = curr
                curr.children.append(f)
            case [s, d]:
                if s.isdigit():
                    f = File(d)
                    f.parent = curr
                    f.size = int(s)
                    curr.children.append(f)
                else:
                    raise ValueError("Invalid filename!")

    return root


def printFileTree(root: 'File', tab=0):
    print("\t" * tab, root.name, "dir" if root.size == 0 else "file", )
    for f in root.children:
        printFileTree(f, tab + 1)


def sizeof(dir: 'File'):

    if len(dir.children) == 0:
        return dir.size
    else:
        return sum(map(sizeof, dir.children))


def part1(lines: List[str]):

    root = buildFileTree(lines)

    total = 0

    def getSizeOf(node: 'File'):
        nonlocal total

        if len(node.children) == 0:
            return node.size
        else:
            size = 0

            for f in node.children:
                s = getSizeOf(f)
                size += s

            if size <= 100000:
                total += size

            return size

    getSizeOf(root)

    return total


def part2(lines: List[str]):

    root = buildFileTree(lines)

    TOTAL_DISK_SPACE = 70000000

    USED_SPACE = sizeof(root)

    SPACE_NEEDED = 30000000 - (TOTAL_DISK_SPACE - USED_SPACE)

    def findClosestDir(root: 'File'):

        s = sizeof(root)

        if s < SPACE_NEEDED:
            return (root.name, float('inf'))
        else:

            smallest = (root.name, s)

            for f in root.children:

                if (v := sizeof(f)) > SPACE_NEEDED and f.size == 0:
                    smallest = min(smallest, findClosestDir(f),
                                   key=lambda r: r[1])

            return smallest

    return findClosestDir(root)[1]


# region Fetch Input and Run
YEAR = 2022


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

        inp = input(message)
        inp = inp.strip("\n")

        if inp == "q":
            os._exit(0)

        if inp is None or len(inp) == 0:
            print("invalid input: type q to quit")
            continue

        yield inp


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
