from aoc import AdventOfCode


def is_visible(grid, coord: tuple[int, int]):
    x, y = coord

    if y == 0 or y == len(grid) - 1:
        return True

    if x == 0 or x == len(grid) - 1:
        return True

    left_visible = True

    for i in range(x):
        if grid[y][i] >= grid[y][x]:
            left_visible = False
            break

    if left_visible:
        return True

    top_visible = True

    for i in range(y):

        if grid[i][x] >= grid[y][x]:
            top_visible = False
            break

    if top_visible:
        return True

    right_visible = True

    for i in range(len(grid[0]) - 1, x, -1):
        if grid[y][i] >= grid[y][x]:
            right_visible = False
            break

    if right_visible:
        return True

    bottom_visible = True

    for i in range(len(grid) - 1, y, -1):
        if grid[i][x] >= grid[y][x]:
            bottom_visible = False
            break

    return bottom_visible


def part1(lines: list[str]):

    grid: list[list[int]] = [[int(c) for c in l] for l in lines]

    count = 0

    for y in range(len(grid)):
        for x in range(len(grid[0])):

            if is_visible(grid, (x, y)):
                count += 1

    return count


def scenic_score(grid: list[list[int]], coord: tuple[int, int]):
    up = down = left = right = 0
    x, y = coord
    for i in range(x + 1, len(grid[0])):
        right += 1
        if grid[y][x] <= grid[y][i]:
            break
    for i in range(x - 1, -1, -1):
        left += 1
        if grid[y][x] <= grid[y][i]:
            break
    for i in range(y + 1, len(grid)):
        down += 1
        if grid[y][x] <= grid[i][x]:
            break
    for i in range(y - 1, -1, -1):
        up += 1
        if grid[y][x] <= grid[i][x]:
            break

    return up * down * left * right


def part2(lines: List[str]):
    grid: list[list[int]] = [[int(c) for c in l] for l in lines]

    max_scenic_score = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):

            max_scenic_score = max(
                max_scenic_score, scenic_score(grid, (x, y)))

    return max_scenic_score


AdventOfCode(part1, part2).exec()
