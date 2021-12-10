from typing import List
from sys import argv
import requests
import os

def part1(lines: List[str]):

    points = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137
    }

    totalPoints = 0
    for l in lines:

        st = []

        for c in l:

            if c in ("(", "{", "<", "["):
                st.append(c)
            else:

                if len(st) == 0:
                    totalPoints += points[c]
                    break

                r = st.pop()

                if (r, c) in (("(", ")"), ("{", "}"), ("<", ">"), ("[", "]")):
                    continue

                totalPoints += points[c]
                break

    return totalPoints


def part2(lines: List[str]):

    points = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }

    scores = []
    for l in lines:

        st = []
        valid = True
        totalScore = 0

        for c in l:

            if c in ("(", "{", "<", "["):
                st.append(c)
            else:

                if len(st) == 0:
                    valid = False
                    break

                r = st.pop()

                if (r, c) in (("(", ")"), ("{", "}"), ("<", ">"), ("[", "]")):
                    continue

                valid = False
                break

        if valid and len(st) > 0:
            while len(st) != 0:

                r = st.pop()

                if r == "(":
                    totalScore = totalScore * 5 + points[")"]
                elif r == "{":
                    totalScore = totalScore * 5 + points["}"]
                elif r == "<":
                    totalScore = totalScore * 5 + points[">"]
                elif r == "[":
                    totalScore = totalScore * 5 + points["]"]
            scores.append(totalScore)
        print("%s : Valid: %s, Score: %d" % (l, str(valid), totalScore))


    return sorted(scores)

# region Fetch Input and Run
YEAR = 2021

def sessionKey():
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

def fetchPuzzleInput():
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
            while (dayNo := input(
                    "Error parsing day number. Please enter the day number: ")):
                try:
                    dayNo = int(dayNo)
                    break
                except:
                    print("Invalid Day Number")
                    continue

    URL = "https://adventofcode.com/%d/day/%d/input" % (YEAR, dayNo)
    print("Downloading input for day %d" % dayNo)
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

    while (part := input("Which part to run ? [1 (default)/2]: ")):

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
