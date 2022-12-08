from typing import List
from sys import argv
import requests
import os

def isBigCave(cave):

    return cave.upper() == cave

def part1(lines: List[str]):

    adj_list = dict()

    for l in lines:
        [s,t] = l.split("-")

        if s not in adj_list:
            adj_list[s] = [t]
        else:
            adj_list[s].append(t)

        if t not in adj_list:
            adj_list[t] = [s]
        else:
            adj_list[t].append(s)

    paths = 0
    def rec(root, visited=set()):
        nonlocal paths
        new_visited = set(visited)
        if root == "end":
            paths += 1
            return
        for cave in adj_list.get(root, []):

            if isBigCave(cave):
                rec(cave, new_visited)
                continue
            
            if cave not in new_visited:
                new_visited.add(cave)
                rec(cave, new_visited)
                new_visited.remove(cave)
        

    rec("start", set(["start"]))


    return paths


def part2(lines: List[str]):
    adj_list = dict()

    for l in lines:
        [s,t] = l.split("-")

        if s not in adj_list:
            adj_list[s] = [t]
        else:
            adj_list[s].append(t)

        if t not in adj_list:
            adj_list[t] = [s]
        else:
            adj_list[t].append(s)

    paths = 0
    def rec(root, visited=set(), smallCave=False):
        nonlocal paths
        
        new_visited = set(visited)
        
        if root == "end":
            paths += 1
            return

        for cave in adj_list.get(root, []):

            if isBigCave(cave):
                rec(cave, new_visited, smallCave)
                continue
            
            if cave not in new_visited:
                new_visited.add(cave)
                rec(cave, new_visited, smallCave)
                new_visited.remove(cave)
            else:
                if not smallCave and cave != "start":
                    rec(cave, new_visited, True)
                
    rec("start", set(["start"]))

    return paths



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
