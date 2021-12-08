from typing import List
from sys import argv

mapping = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9
}

def part1(lines: List[str]):

    count = 0
    for l in lines:

        signal_patterns, output = l.split(" | ")

        for out in output.split(" "):
            if len(out) in (2, 4, 3, 7):
                count += 1

    return count



def findMatching(perm: List[str], signals):

    if len(perm) == 7:
        for sig in signals:
            new_map = ""
            for c in sig:
                new_map += "abcdefg"[perm.index(c)]

            new_map = "".join(sorted([c for c in new_map]))

            if new_map not in mapping:
                return []
        
        return perm
    else:
        for c in "abcdefg":
            if c not in perm:
                perm.append(c)
                soln = findMatching(perm[:], signals)

                if len(soln) > 0:
                    return soln
                
                perm = perm[:-1]

        return []

def part2(lines: List[str]):

    total = 0
    for l in lines:

        signal_patterns, output = l.split(" | ")

        perm = findMatching([], signal_patterns.split(" "))

        num = ""

        for out in output.split(" "):
            new_map = ""
            for c in out:
                new_map += "abcdefg"[perm.index(c)]

            num += str(mapping["".join(sorted(new_map))])
            
        total += int(num)

    return total
            




if __name__ == "__main__":

    fp = open(argv[1], "r")
    lines = fp.readlines()
    lines = [r.strip("\n") for r in lines]

    print(part1(lines))
    print(part2(lines))
