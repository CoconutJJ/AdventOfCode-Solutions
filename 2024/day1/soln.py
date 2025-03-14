

def soln(L1: list[int], L2: list[int]):

    L1, L2 = sorted(L1), sorted(L2)

    dist = 0
    
    for a,b in zip(L1, L2):
        dist += abs(a - b)
    
    return dist


def soln2(L1: list[int], L2: list[int]):

    freq = dict()

    for c in L2:

        if c not in freq:
            freq[c] = 1
        else:
            freq[c] += 1

    sim = 0
    for c in L1:
        
        sim += c * freq.get(c, 0)

    return sim

    
    


if __name__ == "__main__":


    with open("input.txt", "r") as f:

        L1 = []
        L2 = []
        
        for line in f.readlines():

            tokens = line.split(" ")

            a, b = tokens[0], tokens[-1]
            
            L1.append(int(a))
            L2.append(int(b))

        print(soln(list(L1), list(L2)))    
        print(soln2(L1, L2))

                
    
    

