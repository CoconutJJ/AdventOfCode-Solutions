import re

with open("input.txt", "r") as f:

    lines = f.readlines()

    n = 0

    for l in lines:

        l = l.strip('\n')
        match = re.search("([0-9]*)-([0-9]*) (.): (.*)", l)
        lb = int(match.group(1))
        up = int(match.group(2))

        ch = match.group(3)

        password = match.group(4)

        if password[lb - 1] == ch and password[up - 1] == ch:
            continue

        if password[lb - 1] == ch or password[up - 1] == ch:
            n += 1

    print(n)
