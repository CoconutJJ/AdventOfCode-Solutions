from typing import List, Tuple
def inGrid(arrangement, x, y):
    return (0 <= y < len(arrangement)) and (0 <= x < len(arrangement[0]))

def countSeats(arrangement: List[List[str]], xy: Tuple[int, int]):
    x, y = xy

    neighbours = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1, -1), (-1, 1), (-1,-1)]
    
    occupied = 0

    for dx,dy in neighbours:
        i, j = x,y
        while True:

            i, j = i + dx, j + dy
            
            if not inGrid(arrangement, i,j):
                break
            
            if arrangement[j][i] == ".":
                continue

            if arrangement[j][i] == "#":
                occupied += 1
            
            break



    return occupied

def mkCopy(arrangement):

    return [["." for c in l] for l in arrangement]


with open("input.txt", "r") as f:
    
    arrangement = []

    for l in f.readlines():
        l = l.strip('\n')
        if len(l) == 0:
            continue

        arrangement.append([c for c in l])
    
    changed = True
    new_arrangement = mkCopy(arrangement)
    while (changed):
        changed = False    
        for y in range(len(arrangement)):
            for x in range(len(arrangement[0])):
                
                if arrangement[y][x] == ".":
                    continue

                occ = countSeats(arrangement, (x,y))
                
                new_arrangement[y][x] = arrangement[y][x]
                
                if arrangement[y][x] == "L" and occ == 0:
                    new_arrangement[y][x] = "#"
                    changed = True

                if arrangement[y][x] == "#" and occ >= 5:
                    new_arrangement[y][x] = "L"
                    changed = True
        
        arrangement = new_arrangement
        new_arrangement = mkCopy(arrangement)
    
    occupied = 0
    for y in range(len(arrangement)):
        for x in range(len(arrangement[0])):
            if arrangement[y][x] == "#":
                occupied += 1

    print(occupied)
