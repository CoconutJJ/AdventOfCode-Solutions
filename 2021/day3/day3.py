
import sys


def getBitCount(nums):
    bitCount = dict()
    for r in nums:
        for i, c in enumerate(r):

            bitCount[i] = bitCount.get(i, 0) + (1 if int(c) == 1 else -1)

    return bitCount


def filterOxygenFrequency(nums, bitPos):

    oxygen = []
    bitCount = getBitCount(nums)

    for r in nums:

        if bitCount[bitPos] == 0 and r[bitPos] == '1':
            oxygen.append(r)
            continue

        if (bitCount[bitPos] < 0 and r[bitPos] == '0') or (bitCount[bitPos] > 0 and r[bitPos] == '1'):
            oxygen.append(r)
            continue

    return oxygen


def filterC02Frequency(nums, bitPos):
    c02 = []
    bitCount = getBitCount(nums)

    for r in nums:
        if bitCount[bitPos] == 0 and r[bitPos] == '0':
            c02.append(r)
            continue
        if (bitCount[bitPos] < 0 and r[bitPos] == '1') or (bitCount[bitPos] > 0 and r[bitPos] == '0'):
            c02.append(r)
            continue

    return c02


fp = open(sys.argv[1], "r")

nums = fp.readlines()
nums = [r.strip("\n") for r in nums]


oxygen = nums
i = 0
while len(oxygen) != 1:
    print(len(oxygen))
    oxygen = filterOxygenFrequency(oxygen, i)
    i += 1

print("Oxygen: %d" % int(oxygen[0], base=2))

C02 = nums
i = 0
while len(C02) != 1:
    C02 = filterC02Frequency(C02, i)
    i += 1

print("C02: %d" % int(C02[0], base=2))


print("Lifesupport Rating: %d" %
      (int(oxygen[0], base=2) * int(C02[0], base=2)))
