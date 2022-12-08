from typing import List
from sys import argv
import requests
import os
import math


class Interpreter:

    def __init__(self, hexCode) -> None:
        self.PACKETS = self.convertToBinaryCode(hexCode)
        self.BITS_READ = 0
        self.tree = ""
        self.tablevel = 0

    def convertToBinaryCode(self, hexcode):

        leadingZeroes = 0

        for c in hexcode:
            if c != "0":
                break
            leadingZeroes += 1

        bincode = bin(int(hexcode, 16))[2:]

        bincode = "0" * 4 * leadingZeroes + bincode

        return self.align4Bits(bincode)

    def align4Bits(self, PACKETS):

        if len(PACKETS) % 4 == 0:
            return PACKETS

        return "0" * (4 - (len(PACKETS) % 4)) + PACKETS

    def readbits(self, n):

        self.BITS_READ += n
        chunk = self.PACKETS[:n]
        self.PACKETS = self.PACKETS[n:]

        return int(chunk, 2)

    def subpackets(self):

        type_id = self.readbits(1)

        match type_id:
            case 1:
                num_packets = self.readbits(11)

                for _ in range(num_packets):
                    yield self.readpacket()
            case 0:
                total_len = self.readbits(15)

                start = self.BITS_READ
                while self.BITS_READ < start + total_len:
                    yield self.readpacket()
        return

    def readpacket(self):

        version = self.readbits(3)
        id = self.readbits(3)

        if id == 4:
            segments = []
            while True:

                c = self.readbits(1)

                segments.append(self.readbits(4))

                if c == 0:
                    break
            total = 0
            for s in segments:
                total = total << 4
                total = total | s

            return total

        packets = []
        for s in self.subpackets():
            packets.append(s)
        match id:
            case 0: return sum(packets)
            case 1: return math.prod(packets)
            case 2: return min(packets)
            case 3: return max(packets)
            case 5: return 1 if packets[0] > packets[1] else 0
            case 6: return 1 if packets[0] < packets[1] else 0
            case 7: return 1 if packets[0] == packets[1] else 0

    def interpret(self):

        return self.readpacket()


def part1(lines: List[str]):
    pass


def part2(lines: List[str]):
    interp = Interpreter(lines[0])

    return interp.interpret()


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
