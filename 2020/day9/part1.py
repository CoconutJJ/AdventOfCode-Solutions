with open("input.txt") as f:

    numbers = []

    for l in f.readlines():
        numbers.append(int(l.strip("\n")))

    prefixSum = dict()
    prefixSum[-1] = 0
    sumIndex = dict()
    currNumbers = set()
    for i in range(len(numbers)):

        prefixSum[i] = prefixSum[i-1] + numbers[i]
        sumIndex[prefixSum[i]] = i

        if (k := prefixSum[i] - 32321523) in currNumbers:
            l = numbers[sumIndex[k] + 1: i+1]

            print(numbers[sumIndex[k] + 1: i+1])
            break

        currNumbers.add(prefixSum[i])
