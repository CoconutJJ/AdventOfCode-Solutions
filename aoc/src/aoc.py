from sys import argv
from requests import Session
from datetime import datetime
from typing import Callable
from os.path import basename
import os


class AdventOfCode:

    def __init__(self, part1: Callable[[list[str]], int | str], part2: Callable[[list[str]], int | str], year=None, day=None) -> None:
        self.session_key = self._sessionKey()

        self.year = year
        if self.year is None:
            self.year = self._getYear()

        self.day = day
        if self.day is None:
            self.day = self._getDay()

        self.part1: Callable[[list[str]], int | str] = part1
        self.part2: Callable[[list[str]], int | str] = part2

    def exec(self):
        if len(argv) < 2:
            lines = self._fetchPuzzleInput()
        else:
            fp = open(argv[1], "r")
            lines = fp.readlines()
            lines = [r.strip("\n") for r in lines]

        for part in self._prompt("Which part to run ? [1 (default)/2]: "):

            part = part.strip("\n")

            if len(part) == 0:
                print(self.part1(lines))
                break

            try:
                part = int(part)
            except:
                print("Invalid part number")
                continue

            if part == 1:
                print(self.part1(lines))
            elif part == 2:
                print(self.part2(lines))
            else:
                print("Invalid part number")
                continue

            break

    def _getYear(self):
        return datetime.now().year

    def _getDay(self):

        return int(basename(argv[0]).split(".")[0])

    def _sessionKey(self):
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

    def _prompt(self, message):
        while True:

            inp = input(message)
            inp = inp.strip("\n")

            if inp == "q":
                os._exit(0)

            if inp is None or len(inp) == 0:
                print("invalid input: type q to quit")
                continue

            yield inp

    def _fetchPuzzleInput(self):

        print("Fetching puzzle input...")

        if os.path.isfile("input.txt"):
            print("Using cached input...")
            fp = open("input.txt", "r")
            lines = fp.readlines()
            lines = [r.strip("\n") for r in lines]
            return lines

        s = Session()

        s.cookies.set("session", self.session_key, domain=".adventofcode.com")

        URL = "https://adventofcode.com/%d/day/%d/input" % (
            self.year, self.day)

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
