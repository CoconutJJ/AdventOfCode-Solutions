from typing import List
from sys import argv
import requests
import os


def neighbours(x, y):

    return [
        (x-1, y-1), (x, y - 1), (x + 1, y - 1),
        (x - 1, y), (x, y), (x + 1, y),
        (x - 1, y + 1), (x, y+1), (x+1, y+1)
    ]


def part1(lines: List[str]):

    img_map = lines[0]

    img = dict()

    dimX = len(lines[2])
    dimY = len(lines[2:])

    for y, l in enumerate(lines[2:]):
        x = 0
        for c in l:
            img[(x,y)] = (c == "#")
            x += 1

    def next_step(img: dict, xrange, yrange, zero_val):

        new_img = dict()

        x_lower, x_upper = xrange
        y_lower, y_upper = yrange

        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0

        for x in range(x_lower - 1, x_upper + 2):
            for y in range(y_lower - 1, y_upper + 2):
                bin_str = ""

                for (i, j) in neighbours(x, y):
                    x_min = min(x_min, i)
                    x_max = max(x_max, i)
                    y_min = min(y_min, j)
                    y_max = max(y_max, j)
                    # print(i,j)

                    if (i,j) not in img:
                        bin_str += str(zero_val)
                    elif not img[(i,j)]:
                        bin_str += "0"
                    else:
                        bin_str += "1"

                idx = int(bin_str, 2)

                if img_map[idx] == "#":
                    new_img[(x,y)] = True
                else:
                    new_img[(x,y)] = False

        return new_img, (x_min, x_max), (y_min, y_max)


    finished_img, xrange, yrange = next_step(img, (0, dimX - 1), (0, dimY - 1), 0)
    # finished_img, xrange, yrange = next_step(finished_img, xrange, yrange, 1)

    count = 0
    for (i,j) in finished_img:
        if finished_img[(i,j)]:
            count += 1


    return count


def part2(lines: List[str]):
    img_map = lines[0]

    img = dict()

    dimX = len(lines[2])
    dimY = len(lines[2:])

    for y, l in enumerate(lines[2:]):
        x = 0
        for c in l:
            img[(x,y)] = (c == "#")
            x += 1
    

    def next_step(img: dict, xrange, yrange, zero_val):

        new_img = dict()

        x_lower, x_upper = xrange
        y_lower, y_upper = yrange

        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0

        for x in range(x_lower - 1, x_upper + 2):
            for y in range(y_lower - 1, y_upper + 2):
                bin_str = ""

                for (i, j) in neighbours(x, y):
                    x_min = min(x_min, i)
                    x_max = max(x_max, i)
                    y_min = min(y_min, j)
                    y_max = max(y_max, j)
                    # print(i,j)

                    if (i,j) not in img:
                        bin_str += str(zero_val)
                    elif not img[(i,j)]:
                        bin_str += "0"
                    else:
                        bin_str += "1"

                idx = int(bin_str, 2)

                if img_map[idx] == "#":
                    new_img[(x,y)] = True
                else:
                    new_img[(x,y)] = False

        return new_img, (x_min, x_max), (y_min, y_max)

    
    xrange = (0, dimX - 1)
    yrange = (0, dimY - 1)
    finished_img = img
    z = 0
    for _ in range(50):
        finished_img, xrange, yrange = next_step(finished_img, xrange, yrange, z)
        z = 1 - z

    count = 0
    for (i,j) in finished_img:
        if finished_img[(i,j)]:
            count += 1

    return count

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
