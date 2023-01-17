from aoc import AdventOfCode


class File:

    def __init__(self, name) -> None:
        self.parent = None
        self.name = name
        self.size = 0
        self.children: list[File] = []


def buildFileTree(lines: list[str]):
    root = File("/")
    root.parent = root
    curr = None
    for l in lines:

        command = l.split(" ")

        match command:
            case ["$", "cd", ".."]:
                curr = curr.parent
            case ["$", "cd", "/"]:
                curr = root
            case ["$", "cd", r]:
                for f in curr.children:
                    if f.name == r:
                        curr = f
            case ["$", "ls"]:
                continue
            case ["dir", d]:
                f = File(d)
                f.parent = curr
                curr.children.append(f)
            case [s, d]:
                if s.isdigit():
                    f = File(d)
                    f.parent = curr
                    f.size = int(s)
                    curr.children.append(f)
                else:
                    raise ValueError("Invalid filename!")

    return root


def printFileTree(root: 'File', tab=0):
    print("\t" * tab, root.name, "dir" if root.size == 0 else "file")
    for f in root.children:
        printFileTree(f, tab + 1)


def sizeof(dir: 'File'):

    if len(dir.children) == 0:
        return dir.size
    else:
        return sum(map(sizeof, dir.children))


def part1(lines: list[str]):

    root = buildFileTree(lines)

    total = 0

    def getSizeOf(node: 'File'):
        nonlocal total

        if len(node.children) == 0:
            return node.size
        else:
            size = 0

            for f in node.children:
                s = getSizeOf(f)
                size += s

            if size <= 100000:
                total += size

            return size

    getSizeOf(root)

    return total


def part2(lines: list[str]):

    root = buildFileTree(lines)

    TOTAL_DISK_SPACE = 70000000

    USED_SPACE = sizeof(root)

    SPACE_NEEDED = 30000000 - (TOTAL_DISK_SPACE - USED_SPACE)

    def findClosestDir(root: 'File'):

        s = sizeof(root)

        if s < SPACE_NEEDED:
            return (root.name, float('inf'))
        else:

            smallest = (root.name, s)

            for f in root.children:

                if (v := sizeof(f)) > SPACE_NEEDED and f.size == 0:
                    smallest = min(smallest, findClosestDir(f),
                                   key=lambda r: r[1])

            return smallest

    return findClosestDir(root)[1]


AdventOfCode(part1, part2).exec()
