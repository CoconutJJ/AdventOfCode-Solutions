import random

charset = dict()

def unfoldX(coord, X):

    x, y = coord

    if x > X:
        return (x, y)

    x = -(x - X) + X

    return (x, y)


def unfoldY(coord, Y):

    x, y = coord

    if y > Y:
        return (x, y)

    y = -(y - Y) + Y

    return (x, y)

def write(s):

    grid = [[], [], [], [], [], [], [], [], []]

    for c in s:

        if c == " ":
            for i in range(len(grid)):
                grid[i].append("   ")

            continue


        for i, line in enumerate(charset[c]):
            grid[i].extend(line)
    
    return grid


def scramble(grid):

    rounds = 15

    points = set()

    folds = []

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "#":
                points.add((x,y))

    xMax = len(grid[0])
    yMax = len(grid)
    
    for _ in range(rounds):

        foldF = None
        v = None
        if random.randint(0,1) == 1:
            foldF = unfoldX
            xMax = xMax * 2
            v = xMax - 1
            folds.append(("x", xMax - 1))
        else:
            foldF = unfoldY
            yMax = yMax * 2
            v = yMax - 1
            folds.append(("y", yMax - 1))


        new_points = set()
        for x,y in points:

            if random.randint(0,1) == 0:
                new_points.add(foldF((x,y), v))
            else:
                new_points.add((x,y))
        points = new_points
    
    for x,y in points:
        print("%d,%d" % (x,y))
    
    print("\n\n")

    for ax, v in reversed(folds):
        print("fold along %s=%d" % (ax, v))

if __name__ == "__main__":

    font = open("asciichars.txt", "r")
    lines = font.readlines()

    i = 0


    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

        while "#" not in lines[i]: 
            i += 1
        
        charset[c] = []

        while "#" in lines[i]:
            
            charset[c].append([r for r in lines[i].strip("\n")])
            i += 1
    
    scramble(write("AOC TWENTY TWENTY ONE"))

    # print("\n".join(["".join(g) for g in write("DAVID IS COOL")]))
    
    
        