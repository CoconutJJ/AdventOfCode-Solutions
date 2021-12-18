with open('input.txt', 'r') as file:
    lines = [i for i in file.read().splitlines()]

Olines = lines
CO2lines = lines



for i in range(0, 12):
    bits = {0: 0, 1: 0}

    for num in lines:
        
        c = int(num[i])
        bits[c] += 1

    O = '1' if bits[0] < bits[1] else '0'
    CO2 = '0' if bits[0] <= bits[1] else '1'

    if len(Olines) > 1:
        new_lines = []
        for line in Olines:
            if line[i] == O:
                new_lines.append(line)
        Olines = new_lines

    if len(CO2lines) > 1:
        new_lines = []
        
        for line in CO2lines:
            if line[i] == CO2:
                new_lines.append(line)
        
        CO2lines = new_lines

print (Olines, CO2lines)
ans = int(Olines[0], 2) * int(CO2lines[0], 2)

print(ans)