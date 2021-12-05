from typing import List
import sys

class Board:

    def __init__(self, boardRows: List[List[int]]) -> None:
        self.rows = boardRows
        self.marked = dict()

    def idx(self, i, j):
        return self.rows[i][j]

    def isWinningMark(self, i, j):

        row = True
        col = True

        for k in range(len(self.rows[i])):
            row = row and self.marked.get((i, k), False)

        for k in range(len(self.rows)):
            col = col and self.marked.get((k, j), False)

        return row or col

    def calculateScore(self, lastNum):

        total = 0

        for i in range(len(self.rows)):
            for j in range(len(self.rows[i])):

                if not self.marked.get((i,j), False):
                    total += self.idx(i,j)

        return total * lastNum

    def mark(self, n) -> bool:

        win = False

        for i in range(len(self.rows)):
            for j in range(len(self.rows[i])):

                if self.idx(i, j) == n:

                    self.marked[(i, j)] = True

                    win = win or self.isWinningMark(i, j)

        return win


fp = open(sys.argv[1], "r")

lines = fp.readlines()
lines = [l.strip("\n") for l in lines]

numbers: List[int] = map(int, lines[0].split(","))
boards: List[Board] = []

rows = []

for l in lines[1:]:

    if len(l) == 0:
        continue
    
    l = l.split(" ")
    l = [int(j) for j in l if len(j) > 0]


    rows.append(l)

    if len(rows) == 5:
        boards.append(Board(rows))
        rows = []


lastWinScore = None

for n in numbers:
    survivingBoards = []

    for b in boards:
        if b.mark(n):
            lastWinScore = b.calculateScore(n)
        else:
            survivingBoards.append(b)

    boards = survivingBoards

print("Last Board Win Score %d" % lastWinScore)

# Part 1
# for n in numbers:
#     for b in boards:
#         if b.mark(n):
#             total = 0
#             for i in range(len(b.rows)):
#                 for j in range(len(b.rows[i])):
#                     if not b.marked.get((i,j), False):
#                         total += b.idx(i,j)

#             print("Final Score %d" % (total * n))
#             exit(0)