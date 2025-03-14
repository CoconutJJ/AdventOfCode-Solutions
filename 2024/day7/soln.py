import sys


def is_possible(total, terms):

    def rec(t, L):

        if len(L) == 0:
            return t == total
        
        s1 = t * L[0]
        s2 = t + L[0]
        possible = False

        if s1 <= total:
            possible = possible or rec(s1, L[1:])

        if s2 <= total:
            possible = possible or rec(s2, L[1:])

        return possible
            

    return rec(terms[0], terms[1:])
        
def is_possible_with_concat(total, terms):

    def concat(x: int, y: int) -> int:
        
        return int(str(x) + str(y))

    def rec(t, L):
        
        if len(L) == 0:
            return t == total
        
        s1 = t * L[0]
        s2 = t + L[0]
        s3 = concat(t, L[0])
        possible = False

        if s1 <= total:
            possible = possible or rec(s1, L[1:])

        if s2 <= total:
            possible = possible or rec(s2, L[1:])

        if s3 <= total:
            possible = possible or rec(s3, L[1:])
        
        return possible
    
    return rec(terms[0], terms[1:])

if __name__ == "__main__":


    with open(sys.argv[1], "r") as f:

        test_value_sum = 0
        for l in f.readlines():

            test_value, terms = l.split(":")
            test_value = int(test_value)
            terms = list(map(int, terms.strip().split(" ")))
            
            
            if is_possible_with_concat(test_value, terms):
                test_value_sum += test_value

            
        print(test_value_sum)
                
                        
        
    
