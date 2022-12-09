
with open("input.txt", "r") as f:

    lines = f.readlines()

    numbers = []

    for l in lines:

        l = int(l.strip("\n"))

        numbers.append(l)

    numset = set()

    for i in range(len(numbers) - 1):
        for j in range(i + 1, len(numbers)):

            if 2020 - numbers[i] - numbers[j] in numset:
                print(numbers[i] * numbers[j] *
                      (2020 - numbers[i] - numbers[j]))

            numset.add(numbers[i])
            numset.add(numbers[j])
