from typing import List
from sys import argv


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


if __name__ == "__main__":

    fp = open(argv[1], "r")
    lines = fp.readlines()
    lines = [r.strip("\n") for r in lines]

    # print(part1(lines))
    print(part2(lines))
