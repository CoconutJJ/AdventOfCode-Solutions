from aoc import AdventOfCode
from heapq import heappush, heappop


def get_elevation(c: str):

    if c == "S":
        return 0

    if c == "E":
        return ord('z') - ord('a')

    return ord(c) - ord('a')


def cost(a, b):

    a_el = get_elevation(a)
    b_el = get_elevation(b)

    if b_el <= a_el + 1:
        return 1

    return float('inf')


def neigbours(coord: tuple[int, int], y_len, x_len):

    x, y = coord

    vecs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dx, dy in vecs:

        if x + dx < 0:
            continue

        if x + dx >= x_len:
            continue

        if y + dy < 0:
            continue

        if y + dy >= y_len:
            continue

        yield (x + dx, y + dy)

    return


def dijkstra(grid: list[list[str]], start: tuple[int, int]):

    x, y = start

    pq = [(0, start)]

    visited = set()

    grid_size = len(grid) * len(grid[0])

    dist = dict()
    prev = dict()
    # print(grid_size)
    while len(visited) != grid_size:

        _, (x, y) = heappop(pq)
        visited.add((x, y))
        # print (len(visited))
        dist[(x, y)] = 0

        for nx, ny in neigbours((x, y), len(grid), len(grid[0])):

            if (nx, ny) in visited:
                continue

            new_cost = dist[(x, y)] + cost(grid[y][x], grid[ny][nx])

            if (nx, ny) not in dist:
                dist[(nx, ny)] = float('inf')

            if new_cost < dist[(nx, ny)]:

                dist[(nx, ny)] = new_cost

                prev[(nx, ny)] = (x, y)

            heappush(pq, (dist[(nx, ny)], (nx, ny)))

    return prev


def bfs(grid: list[list[str]], start: tuple[int, int]):

    q = [(start, 0)]
    visited = set()
    min_dist = float('inf')
    visited.add(start)
    while len(q) != 0:

        (x, y), steps = q.pop(0)

        if grid[y][x] == "E":
            min_dist = min(min_dist, steps)
            continue

        for nx, ny in neigbours((x, y), len(grid), len(grid[0])):

            if (nx, ny) in visited:
                continue

            if cost(grid[y][x], grid[ny][nx]) == 1:
                visited.add((nx, ny))
                q.append(((nx, ny), steps + 1))

    return min_dist


def part1(lines: list[str]):

    grid = [[c for c in l] for l in lines]

    start = None
    end = None

    for y in range(len(grid)):
        for x in range(len(grid[0])):

            if grid[y][x] == "S":
                start = (x, y)
            elif grid[y][x] == "E":
                end = (x, y)

    return bfs(grid, start)


def part2(lines: list[str]):
    grid = [[c for c in l] for l in lines]

    start = None
    end = None
    min_dist = float('inf')
    for y in range(len(grid)):
        for x in range(len(grid[0])):

            if grid[y][x] == "a":
                min_dist = min(min_dist, bfs(grid, (x, y)))
                print(x, y)

    return min_dist


AdventOfCode(part1, part2).exec()
