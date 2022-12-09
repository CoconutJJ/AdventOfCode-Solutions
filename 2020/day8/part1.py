
def runProgram(instructions, ip=0):
    acc = 0
    ip = 0
    while ip < len(instructions):

        ins, n = instructions[ip]

        yield (ip, acc)

        if ins == "jmp":
            ip += n
            continue

        if ins == "acc":
            acc += n
            ip += 1
            continue

        if ins == "nop":
            ip += 1
            continue

    return


def runProgramEnd(instructions, ip):

    ipset = set()
    for (ip, acc) in runProgram(instructions, ip):
        if ip in ipset:
            return False
        ipset.add(ip)

    return True


with open("input.txt", "r") as f:

    instructions = []

    for l in f.readlines():

        l = l.strip("\n")

        if len(l) == 0:
            continue

        ins, n = l.split(" ")

        instructions.append((ins, int(n)))

    instructions[277] = ("nop", 0)

    for (ip, acc) in runProgram(instructions):
        print(ip, acc)
