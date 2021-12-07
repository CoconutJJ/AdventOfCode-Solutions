

from typing import List
from sys import argv

class VM:

    def __init__(self) -> None:
        self.instructions = []
        self.inputs = []
        self.outputs = []
        self.memory = [0] * 10000
        self.ip = 0
        self.base = 0
        self.next_input = 0

    def resetVM(self):
        self.outputs = []
        self.memory = [0] * 1000
        self.ip = 0
        self.next_input = 0
        self.loadInstructions(self.instructions)

    def loadInstructions(self, ins):
        self.instructions = ins
        for i, op in enumerate(ins):
            self.memory[i] = op

    def loadInput(self, inputs):
        self.inputs = inputs

    def READ_INT(self):
        op = self.memory[self.ip]
        self.ip += 1
        return op

    def READ_INPUT(self):
        v = self.inputs[self.next_input]
        self.next_input += 1
        return v

    def WRITE_OUTPUT(self, out):
        self.outputs.append(out)

    def READ_OP(self):
        return self.parseOp(self.READ_INT())

    def parseOp(self, op):
        opcode = op % 100
        modesblob = op // 100

        modes = [0,0,0]

        modes[0] = modesblob % 10
        modesblob = modesblob // 10
        modes[1] = modesblob % 10
        modesblob = modesblob // 10
        modes[2] = modesblob % 10
        

        return opcode, modes

    def processModes(self, modes, args):
        new_args = []
        for i, arg in enumerate(args):
            if modes[i] == 0:
                new_args.append(self.memory[arg])
            elif modes[i] == 2:
                new_args.append(arg + self.base)
            elif modes[i] == 1:
                new_args.append(arg)
            else:
                print("Invalid mode")
            
        return new_args

    def run(self):

        while True:
            op, modes = self.READ_OP()
            print(op, modes)
            if op == 1:
                arg1 = self.READ_INT()
                arg2 = self.READ_INT()
                arg3 = self.READ_INT()
                args = self.processModes(modes, [arg1,arg2, arg3])
                self.memory[args[2]] = args[0] + args[1]
            
            elif op == 2:
                arg1 = self.READ_INT()
                arg2 = self.READ_INT()
                arg3 = self.READ_INT()
                args = self.processModes(modes, [arg1, arg2, arg3])
                self.memory[args[2]] = args[0] * args[1]

            elif op == 3:
                arg = self.READ_INT()
                args = self.processModes(modes, [arg])
                self.memory[args[0]] = self.READ_INPUT()

            elif op == 4:
                arg = self.READ_INT()
                self.WRITE_OUTPUT(self.processModes(modes, [arg])[0])

            elif op == 5:
                arg1 = self.READ_INT()
                arg2 = self.READ_INT()
                args = self.processModes(modes, [arg1, arg2])
                if args[0] != 0:
                    self.ip = args[1]

            elif op == 6:
                arg1 = self.READ_INT()
                arg2 = self.READ_INT()
                print(arg1, arg2)
                print(self.ip)
                args = self.processModes(modes, [arg1, arg2])
                if args[0] == 0:
                    self.ip = args[1]

            elif op == 7:
                arg1 = self.READ_INT()
                arg2 = self.READ_INT()
                arg3 = self.READ_INT()
                args = self.processModes(modes, [arg1, arg2, arg3])
                if args[0] < args[1]:
                    self.memory[args[2]] = 1
                else:
                    self.memory[args[2]] = 0

            elif op == 8:
                arg1 = self.READ_INT()
                arg2 = self.READ_INT()
                arg3 = self.READ_INT()
                args = self.processModes(modes, [arg1, arg2, arg3])
                
                if args[0] == args[1]:
                    self.memory[args[2]] = 1
                else:
                    self.memory[args[2]] = 0

            elif op == 9:
                arg1 = self.READ_INT()
                self.base += self.processModes(modes, [arg1])[0]

            elif op == 99:
                break
            else:
                print("Invalid instruction %d" % op)
                break


def readInstructionFile(file):
    fp = open(file, "r")

    line = fp.readlines()[0]

    instructions = list(map(int, line.split(",")))
    print(instructions)
    return instructions

if __name__ == "__main__":

    instructions = readInstructionFile(argv[1])

    vm = VM()
    vm.loadInstructions(instructions)
    vm.loadInput([1])
    vm.run()
    print(vm.parseOp(204))
    # print(vm.outputs)
