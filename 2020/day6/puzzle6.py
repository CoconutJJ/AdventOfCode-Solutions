
def part1():

    with open("input.txt", 'r') as f:

        questions = set()
        count = 0
        for l in f.readlines():

            l = l.strip()

            if len(l) == 0:
                count += len(questions)
                questions = set()
            else:

                for r in l:
                    questions.add(r)
        
        count += len(questions)

        print(count)

def part2():

    with open('input.txt', 'r') as f:
        
        questions = set([chr(z) for z in range(ord('a'), ord('z') + 1)])

        count = 0

        for l in f.readlines() + ['']:
            l = l.strip()

            if len(l) == 0:

                count += len(questions)
                questions = set([chr(z) for z in range(ord('a'), ord('z') + 1)])
            else:

                curr = set()

                [curr.add(r) for r in l]

                questions = questions.intersection(curr)
        
        print(count)
