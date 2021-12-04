with open("input.txt", "r") as f:

    x = y = 0
    trees = 0
    lines = f.readlines()

    while y < len(lines):

        l = lines[y].strip('\n')

        if l[x] == "#":
            trees += 1
        
        x = (x + 1) % len(l)
        y = y + 2

    print(trees)
    
# 82, 242, 71, 67, 24