
def getSeatID(code):

    rows = list(range(128))
    cols = list(range(8))
    for c in code:

        if c == "F":
            rows = rows[:len(rows)//2]
        elif c == "B":
            rows = rows[len(rows)//2:]
        elif c == "L":
            cols = cols[:len(cols)//2]
        elif c == "R":
            cols = cols[len(cols)//2:]

    return 8*rows[0] + cols[0]


with open("input.txt", "r") as f:

    lines = f.readlines()

    seats = []

    for l in lines:
        l = l.strip('\n')
        ids = getSeatID(l)
        seats.append(ids)

    seats.sort()

    for s, k in zip(seats, seats[1::1]):

        if k - s > 1:
            print(s + 1)
            break