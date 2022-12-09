import re


def processRule(line: str):

    bagContents = re.findall("([0-9]*)\s([a-z]*\s[a-z]*)\sbag[s,.]*", line)

    bagType = re.findall("([a-z]*\s[a-z]*) bags contain", line)

    if len(bagContents) == 1 and bagContents[0][0] == "":
        bagContents = []

    bagContents = list(map(lambda r: (int(r[0]), r[1]), bagContents))

    return bagType[0], bagContents


with open("input.txt", "r") as f:

    graph = dict()

    for l in f.readlines():

        l = l.strip("\n")

        bag, contents = processRule(l)

        for (n, b) in contents:
            if b not in graph:
                graph[b] = set([bag])
            else:
                graph[b].add(bag)

    bags = set()

    q = ["shiny gold"]

    while len(q) != 0:

        bag = q.pop()

        if bag not in graph:
            continue

        for b in graph[bag]:
            if b not in bags:
                bags.add(b)
                q.append(b)

    print(len(bags))
