

def calculateFloor(ins):

    floor = 0
    i = 0
    for c in ins:

        if c == '(':
            floor += 1
        elif c == ')':
            floor -= 1

        i += 1

        if floor < 0:
            return i

    return None


print(calculateFloor(input()))
