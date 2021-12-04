

def countAdapterArrangements(adapters):

    mem = dict()

    def countAdaptersRec(i, last):
        
        if i == len(adapters) - 1:

            if adapters[i] - 3 <= last:
                return 1
            else:
                return 0

        if (i, last) not in mem:
            
            if adapters[i] - 3 > last:
                mem[(i,last)] = 0
            else:
                mem[(i,last)] = countAdaptersRec(i + 1, adapters[i]) + countAdaptersRec(i+1, last)
        
        return mem[(i,last)]

    return countAdaptersRec(0, 0)


with open("input.txt", "r") as f:

    adapters = []

    for l in f.readlines():
        adapters.append(int(l.strip('\n')))
    
    adapters.sort()

    print(countAdapterArrangements(adapters))

    