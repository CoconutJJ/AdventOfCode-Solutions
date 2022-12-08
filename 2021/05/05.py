
from typing import Dict, List, Tuple
import sys

def countOverlappingPoints(vecs: List[Tuple[Tuple[int,int], Tuple[int, int]]]):

        points = dict()

        for ((x1,y1), (x2,y2)) in vecs:

            if x1 != x2 and y1 != y2:
                continue
            
            if x1 == x2:

                for y in range(min(y1,y2), max(y1,y2) + 1):

                    points[(x1, y)] = points.get((x1, y), 0) + 1
            elif y1 == y2:

                for x in range(min(x1,x2), max(x1,x2) + 1):
                    points[(x, y1)] = points.get((x, y1), 0) + 1
        
        overlappingCount = 0
        for p in points:

            if points[p] > 1:
                overlappingCount += 1

        return overlappingCount


def countOverlappingPointsWithDiagonal(vecs: List[Tuple[Tuple[int,int], Tuple[int, int]]]):

    points = dict()

    for ((x1,y1), (x2,y2)) in vecs:

        v = [0,0]

        if x1 < x2:
            v[0] = 1
        elif x1 > x2:
            v[0] = -1

        if y1 < y2:
            v[1] = 1
        elif y1 > y2:
            v[1] = -1


        while (x1, y1) != (x2, y2):

            points[(x1,y1)] = points.get((x1,y1), 0) + 1

            x1 += v[0]
            y1 += v[1]

        points[(x2, y2)] = points.get((x2,y2), 0) + 1
        
    overlappingCount = 0
    for p in points:

        if points[p] > 1:
            overlappingCount += 1

    printGrid(points)

    return overlappingCount

def printGrid(points: Dict[Tuple[int,int], int]):
    
    for x in range(1000):
        for y in range(1000):

            c = points.get((x,y), 0)

            if c == 0:
                print("", end="")
            else:
                print(c, end="")
        
        print("\n", end="")


def parseInput(filename):

    fp = open(filename, "r")

    vecs = fp.readlines()

    parsedVecs = []

    for v in vecs:

        start,end = v.split(" -> ")

        x1,y1 = list(map(int, start.split(",")))
        x2,y2 = list(map(int, end.split(",")))

        parsedVecs.append(((x1,y1), (x2,y2)))
    
    return parsedVecs

if __name__ == "__main__":

    vecs = parseInput(sys.argv[1])

    print(countOverlappingPointsWithDiagonal(vecs))


            
            
