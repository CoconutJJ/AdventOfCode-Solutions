from typing import List
from sys import argv
import requests
import os
from itertools import permutations
DIE = 1
nRolls = 0
def rollDie():
    global DIE
    global nRolls
    v = DIE
    DIE = (DIE + 1) % 101
    nRolls += 1
    if DIE == 0:
        DIE = 1

    return v


def roll():

    return rollDie() + rollDie() + rollDie()


def part1(lines: List[str]):

    p1 = lines[0].split(":")[1]
    p2 = lines[1].split(":")[1]
    p1 = int(p1)
    p2 = int(p2)

    positions =[p1 - 1, p2 - 1]
    scores = [0,0]
    turn = 0
    while True:
        positions[turn] = (positions[turn] + roll()) % 10
        scores[turn] += positions[turn] + 1
        print(scores)

        if scores[turn] >= 1000:
            print (nRolls)
            return scores[1-turn] * (nRolls)
        
        turn = 1- turn



def part2(lines: List[str]):
    p1 = lines[0].split(":")[1]
    p2 = lines[1].split(":")[1]
    p1 = int(p1)
    p2 = int(p2)
    print(p1, p2)
    mem = dict()

    def rec(p1, p1Score, p2, p2Score, turn):
        if p1Score >= 21:
            return (1, 0)
        elif p2Score >= 21:
            return (0, 1)

        if (p1, p1Score, p2, p2Score, turn) not in mem:

            if turn == 0:

                u,v = 0, 0
                for rolls in set(permutations([1,1,1,2,2,2,3,3,3], 3)):

                    new_p1_pos = (p1 + sum(rolls)) % 10
                    new_p1_score = p1Score + new_p1_pos + 1

                    s,t = rec(new_p1_pos, new_p1_score, p2, p2Score, 1)
                    
                    u = u + s
                    v = v + t
                mem[(p1, p1Score, p2, p2Score, turn)] = (u,v)
            else:
                u,v = 0, 0
                for rolls in set(permutations([1,1,1,2,2,2,3,3,3], 3)):

                    new_p2_pos = (p2 + sum(rolls)) % 10
                    new_p2_score = p2Score + new_p2_pos + 1

                    s,t = rec(p1, p1Score, new_p2_pos, new_p2_score, 0)
                    
                    u = u + s
                    v = v + t

                mem[(p1, p1Score, p2, p2Score, turn)] = (u,v)
        
        return mem[(p1, p1Score, p2, p2Score, turn)]

    return rec(p1 - 1, 0, p2 - 1, 0, 0)



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
