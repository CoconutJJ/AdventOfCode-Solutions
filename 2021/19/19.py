from sys import argv
import requests
import os


class Map:

    def __init__(self) -> None:
        self.beacons = set()
        self.scanners = []

    def add_beacon(self, coord):
        self.beacons.add(coord)

    def all_possible_orientations(self, off):

        x, y, z = off

        rotations = [(x, y, z), (x, z, y), (y, x, z),
                     (y, z, x), (z, y, x), (z, x, y)]

        signs = [(-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1),
                 (1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1)]

        orientations = []
        for (x, y, z) in rotations:
            for (i, j, k) in signs:
                orientations.append((x * i, y * j, z * k))

        return orientations

    def generate_orientations(self, coords: list[tuple[int, int, int]]):

        orientations = []

        for c in coords:

            ors = self.all_possible_orientations(c)

            for i in range(len(ors)):

                if i == len(orientations):
                    orientations.append([ors[i]])
                else:
                    orientations[i].append(ors[i])
        return orientations

    def add_vec(self, v1, v2):

        v1x, v1y, v1z = v1
        v2x, v2y, v2z = v2

        return (v1x + v2x, v1y + v2y, v1z + v2z)

    def sub_vec(self, v1, v2):

        v1x, v1y, v1z = v1
        v2x, v2y, v2z = v2

        return (v1x - v2x, v1y - v2y, v1z - v2z)

    def match_beacons(self, coords):
        for u in self.beacons:
            for orientation in self.generate_orientations(coords):
                for v in orientation:
                    k = self.sub_vec(u, v)

                    non_beacons = set()
                    overlaps = 0
                    matched_beacons = set()
                    for beacon in orientation:
                        pos = self.add_vec(k, beacon)

                        if pos in self.beacons:
                            overlaps += 1
                            matched_beacons.add(pos)
                        else:
                            non_beacons.add(pos)

                    if overlaps >= 12:
                        self.beacons = self.beacons.union(non_beacons)
                        self.scanners.append(k)
                        return True

        return False

    def intialize_beacons(self, coords: list[tuple[int, int, int]]):
        self.scanners.append((0, 0, 0))
        for c in coords:
            self.beacons.add(c)

    def stitch_map(self, scanner_coords: list[list[tuple[int, int, int]]]):
        self.intialize_beacons(scanner_coords[0])
        coords_left = scanner_coords[1:]
        while len(coords_left) > 0:

            c = coords_left.pop(0)

            if self.match_beacons(c):
                continue

            coords_left.append(c)

    def greatest_manhattan_distance(self, scanner_coords: list[list[tuple[int, int, int]]]):
        self.stitch_map(scanner_coords)

        max_manhattan_dist = 0
        for u in self.scanners:
            for v in self.scanners:
                i, j, k = self.sub_vec(u, v)
                max_manhattan_dist = max(
                    max_manhattan_dist, abs(i) + abs(j) + abs(k))

        return max_manhattan_dist


def part1(lines: list[str]):
    scanner_coords = []
    coords = None
    for l in lines:

        if "---" in l:
            if coords is not None:
                scanner_coords.append(coords)

            coords = []
            continue

        if "," in l:

            entries = l.split(",")
            c = tuple(map(int, entries))
            coords.append(c)
            continue

    if coords is not None:
        scanner_coords.append(coords)

    m = Map()

    m.stitch_map(scanner_coords)

    return len(m.beacons)


def part2(lines: list[str]):
    scanner_coords = []
    coords = None
    for l in lines:

        if "---" in l:
            if coords is not None:
                scanner_coords.append(coords)

            coords = []
            continue

        if "," in l:

            entries = l.split(",")
            c = tuple(map(int, entries))
            coords.append(c)
            continue

    if coords is not None:
        scanner_coords.append(coords)

    m = Map()

    return m.greatest_manhattan_distance(scanner_coords)


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
