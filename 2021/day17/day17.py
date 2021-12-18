from typing import List
from sys import argv
import requests
import os


def velocity_next(x,y):

    if x < 0:
        x = x + 1
    elif x > 0:
        x = x - 1

    y = y - 1

    return (x,y)

def within_area(x_range, y_range, coord):

    x1, x2 = x_range
    y1, y2 = y_range

    x,y = coord

    return (min(x1,x2) <= x <= max(x1,x2)) and (min(y1,y2) <= y <= max(y1,y2))


def velocities(maxX, maxY):

    for x in range(-maxX, maxX + 1):
        for y in range(-maxY, maxY + 1):
            yield (x,y)

def run_sim(velocity, x_range, y_range):

    pos = (0,0)
    dx, dy = velocity

    x1, x2 = x_range

    y1, y2 = y_range

    maxY = float('-inf')
    
    px, py = pos

    while True:

        maxY = max(py, maxY)

        px,py = px + dx, py + dy
        
        if within_area(x_range, y_range, (px, py)):
            return True, maxY

        # if dx < 0 and px < min(x1, x2):
        #     return False, maxY

        # if dx > 0 and px > max(x1,x2):
        #     return False, maxY

        if dx == 0 and py < min(y1,y2):
            return False, maxY
        
        dx,dy = velocity_next(dx,dy)

        



def part1():


    x_lower = 79
    x_upper = 137

    y_lower = -176
    y_upper = -117

    maxY = float('-inf')
    for vx,vy in velocities(max(abs(x_lower), abs(x_upper)), max(abs(y_lower), abs(y_upper))):
        success, y = run_sim((vx,vy), (x_lower, x_upper), (y_lower, y_upper))
        if success:
            maxY = max(maxY, y)

    return maxY




# def part2(lines: List[str]):
#     x_lower = 79
#     x_upper = 137

#     y_lower = -176
#     y_upper = -117

#     maxY = float('-inf')

#     successes = 0

#     for vx,vy in velocities(max(abs(x_lower), abs(x_upper)), max(abs(y_lower), abs(y_upper))):
#         success, y = run_sim((vx,vy), (x_lower, x_upper), (y_lower, y_upper))
#         if success:
#             successes += 1

#     return successes


# # region Fetch Input and Run
# YEAR = 2021

# def sessionKey():
#     """
#         Move up the dir. tree until we see a file named SESSION. Then read
#         the session key.
#     """
#     cwd = os.getcwd()
#     curr = cwd
#     while not os.path.exists("SESSION"):
#         os.chdir(curr := os.path.join(curr, ".."))
#         if curr == "/":
#             print("Could not find SESSION file!")
#             exit(1)
    
#     key = open("SESSION", "r")
#     os.chdir(cwd)
#     return key.read().strip("\n")

# def prompt(message):
#     while True:
#         try:
#             inp = input(message)
#             inp = inp.strip("\n")
            
#             if inp == "q":
#                 os._exit(0)

#             if inp is None or len(inp) == 0:
#                 print("invalid input: type q to quit")
#                 continue
#             yield inp
#         except GeneratorExit:
#             return
#         except:
#             print("invalid input: type q to quit")


# def fetchPuzzleInput():
#     """

#     """
#     print("Fetching puzzle input...")

#     if os.path.isfile("input.txt"):
#         print("Using cached input...")
#         fp = open("input.txt", "r")
#         lines = fp.readlines()
#         lines = [r.strip("\n") for r in lines]
#         return lines

#     s = requests.Session()

#     s.cookies.set("session", sessionKey(), domain=".adventofcode.com")

#     filename, _ = argv[0].split(".")

#     dayNo = None

#     if filename.startswith("day"):
#         try:
#             dayNo = int(filename[3:])
#         except:
#             dayNo = None

#     if dayNo is None:
#         for dayNo in prompt("Error parsing day number. Please enter the day number: "):
#             try:
#                 dayNo = int(dayNo)                
#             except:
#                 print("Invalid Day Number")
#                 continue
            
#             break

#     URL = "https://adventofcode.com/%d/day/%d/input" % (YEAR, dayNo)

#     # pretend to be linux firefox...
#     body = s.get(URL, headers={
#         "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0"
#     })

#     fp = open("input.txt", "w")
#     fp.write(body.content.decode("utf-8"))
#     fp.close()

#     lines = body.content.decode("utf-8").splitlines()
#     lines = [r.strip("\n") for r in lines]

#     return lines


if __name__ == "__main__":
    print(part1())
    # if len(argv) < 2:
    #     lines = fetchPuzzleInput()
    # else:
    #     fp = open(argv[1], "r")
    #     lines = fp.readlines()
    #     lines = [r.strip("\n") for r in lines]

    # for part in prompt("Which part to run ? [1 (default)/2]: "):

    #     part = part.strip("\n")

    #     if len(part) == 0:
    #         print(part1(lines))
    #         break

    #     try:
    #         part = int(part)
    #     except:
    #         print("Invalid part number")
    #         continue

    #     if part == 1:
    #         print(part1(lines))
    #     elif part == 2:
    #         print(part2(lines))
    #     else:
    #         print("Invalid part number")
    #         continue

    #     break
# endregion
