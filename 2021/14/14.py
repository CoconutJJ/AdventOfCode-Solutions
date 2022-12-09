from typing import List
from sys import argv
import requests
import os


def memoSoln(lines: List[str]):
    rules = dict()

    for l in lines[2:]:

        s, t = l.split(" -> ")

        rules[s] = t

    template = lines[0]

    mem = dict()

    def rec(pattern, step):

        if step == 0:
            return dict()

        if (pattern, step) not in mem:
            c = rules[pattern]

            p1 = pattern[0] + c
            p2 = c + pattern[1]

            freq1 = rec(p1, step - 1)
            freq2 = rec(p2, step - 1)

            freq = dict()

            for k in freq1:
                freq[k] = freq1[k]

            for k in freq2:
                freq[k] = freq.get(k, 0) + freq2[k]

            freq[c] = freq.get(c, 0) + 1

            mem[(pattern, step)] = freq

        return mem[(pattern, step)]

    total = dict()

    for c in template:
        total[c] = total.get(c, 0) + 1

    for i in range(len(template) - 1):

        freq = rec(template[i:i+2], 40)

        for k in freq:
            total[k] = total.get(k, 0) + freq[k]

    return total


def part1(lines: List[str]):

    rules = dict()

    for l in lines[2:]:

        s, t = l.split(" -> ")

        rules[s] = t

    def step(s):
        res = ""
        for i in range(len(s) - 1):
            r = s[i: i + 2]

            if len(res) == 0:
                res += r[0] + rules[r] + r[1]
            else:
                res += rules[r] + r[1]

        return res

    template = lines[0]

    for i in range(10):
        template = step(template)

    freq = dict()
    maxFreq = 0
    minFreq = float('inf')
    for c in template:
        freq[c] = freq.get(c, 0) + 1

    for c in freq:
        maxFreq = max(maxFreq, freq[c])
        minFreq = min(minFreq, freq[c])

    return maxFreq - minFreq


def part2(lines: List[str]):

    rules = dict()

    for l in lines[2:]:

        s, t = l.split(" -> ")

        rules[s] = t

    pairs = dict()
    freq = dict()
    template = lines[0]

    for c in template:
        freq[c] = freq.get(c, 0) + 1

    for i in range(len(template) - 1):
        r = template[i: i + 2]
        pairs[r] = pairs.get(r, 0) + 1

    def step(pairs):
        new_pairs = dict()
        for key in pairs:

            r = rules[key]
            p1, p2 = key[0] + r, r + key[1]

            freq[r] = freq.get(r, 0) + pairs[key]
            new_pairs[p1] = new_pairs.get(p1, 0) + pairs[key]
            new_pairs[p2] = new_pairs.get(p2, 0) + pairs[key]

        return new_pairs

    for _ in range(40):
        pairs = step(pairs)

    maxFreq = 0
    minFreq = float('inf')

    for c in freq:
        maxFreq = max(maxFreq, freq[c])
        minFreq = min(minFreq, freq[c])

    return maxFreq - minFreq


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
