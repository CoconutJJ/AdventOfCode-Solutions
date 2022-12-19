from aoc import AdventOfCode
from re import compile


def part1(lines: list[str]):

    pattern = compile(
        "Valve (.{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)")

    G = dict()

    nodes = []

    non_zero_flow_rate_nodes = []

    flow_rate = dict()

    distances = dict()

    for l in lines:
        matches = pattern.match(l)

        groups = matches.groups()

        valve = groups[0]
        rate = int(groups[1])
        children = groups[2].split(", ")
        flow_rate[valve] = rate
        nodes.append(valve)

        if rate > 0:
            non_zero_flow_rate_nodes.append(valve)

        for c in children:
            distances[(valve, c)] = 1
            distances[(c, valve)] = 1

    def distance_of(edge: tuple[str, str]):

        if edge in distances:
            return distances[edge]

        return float('inf')

    for k in nodes:
        for x in nodes:
            for y in nodes:

                new_dist = distance_of((x, k)) + distance_of((k, y))

                if distance_of((x, y)) > new_dist:

                    distances[(x, y)] = new_dist

    q = [("AA", 30, set(), 0)]

    max_total = 0

    while len(q) != 0:

        node, time, visited, total = q.pop(0)

        max_total = max(max_total, total)

        for r in non_zero_flow_rate_nodes:

            if r in visited:
                continue

            new_visited = set(visited)

            new_visited.add(r)

            new_time = time - distance_of((node, r)) - 1

            new_total = total + new_time * flow_rate[r]

            if new_time >= 0:
                q.append((r, time - distance_of((node, r)) -
                         1, new_visited, new_total))

    return max_total


def part2(lines: list[str]):

    pattern = compile(
        "Valve (.{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)")

    G = dict()

    nodes = []

    non_zero_flow_rate_nodes = []

    flow_rate = dict()

    distances = dict()

    for l in lines:
        matches = pattern.match(l)

        groups = matches.groups()

        valve = groups[0]
        rate = int(groups[1])
        children = groups[2].split(", ")
        flow_rate[valve] = rate
        nodes.append(valve)

        if rate > 0:
            non_zero_flow_rate_nodes.append(valve)

        for c in children:
            distances[(valve, c)] = 1
            distances[(c, valve)] = 1

    def distance_of(edge: tuple[str, str]):

        if edge in distances:
            return distances[edge]

        return float('inf')

    for k in nodes:
        for x in nodes:
            for y in nodes:

                new_dist = distance_of((x, k)) + distance_of((k, y))

                if distance_of((x, y)) > new_dist:

                    distances[(x, y)] = new_dist

    node_pairs = []

    for r in non_zero_flow_rate_nodes:
        for s in non_zero_flow_rate_nodes:
            if r != s:
                node_pairs.append((r, s))

    q = [("AA", 26, 0)]

    t = [("AA", 26, 0)]

    visited = [set()]

    max_total = 0

    while True:

        if len(q) == 0 and len(t) == 0:
            break

        total = 0

        try:
            n1, t1, total1 = q.pop()
            total += total1
        except:
            n1, t1, total1 = None, None, None

        try:
            n2, t2, total2 = t.pop()
            total += total2
        except:
            n2, t2, total2 = None, None, None

        path = visited.pop()
        max_total = max(max_total, total)

        for r in non_zero_flow_rate_nodes:

            if r in path:
                continue

            new_path = set(path)
            new_path.add(r)

            if n1 is not None:
                new_t1 = t1 - distance_of((n1, r)) - 1

                if new_t1 >= 0:
                    q.append((r, new_t1, total1 + new_t1 * flow_rate[r]))
                    t.append((n2, t2, total2))
                    visited.append(new_path)

            if n2 is not None:
                new_t2 = t2 - distance_of((n2, r)) - 1

                if new_t2 >= 0:
                    q.append((n1, t1, total1))
                    t.append((r, new_t2, total2 + new_t2 * flow_rate[r]))
                    visited.append(set(new_path))

    return max_total


AdventOfCode(part1, part2).exec()
