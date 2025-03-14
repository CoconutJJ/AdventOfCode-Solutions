import sys

def file_check_sum(disk_map: str):

    if len(disk_map) % 2 != 0:
        disk_map += "0"

    new_map = []    
    
    for id, (used, free) in enumerate(zip(disk_map[::2], disk_map[1::2])):

        new_map.extend([id] * int(used) + [-1] * int(free))
        

    i = 0
    j = len(new_map) - 1

    while i < j:

        if new_map[i] != -1:
            i += 1
            continue


        if new_map[j] == -1:

            j -= 1
            continue


        new_map[i] = new_map[j]
        new_map[j] = -1

    
        
    check_sum = 0
    for i, c in enumerate(new_map):

        if c == -1:
            break
        
        check_sum += i * c

    return check_sum

def map_repr(new_map):

    map = ""
    for id, size in new_map:

        if id == -1:

            map += "." *size

        else:

            map += str(id) * size

    return map


def entire_file_checksum(disk_map: str):

    if len(disk_map) % 2 != 0:
        disk_map += "0"

    new_map = []    
    
    for id, (used, free) in enumerate(zip(disk_map[::2], disk_map[1::2])):

        new_map.append((id, int(used)))
        new_map.append((-1, int(free)))

    
    j = len(new_map) - 1


    def find_next_section(dmap, moved_ids: set) -> int:

        for j in range(len(dmap) - 1, -1, -1):

            id, size = dmap[j]

            if id != -1 and id not in moved_ids:

                return j

        return -1

    def find_empty_slot(dmap,max_j, size) -> int:


        for i in range(max_j):
                
            id, n = dmap[i]

            if id != -1:
                continue
            
            if n >= size:
                return i


        return -1


    visited = set()
    
    while True:
        j = find_next_section(new_map, visited)

        if j == -1:
            break
        
        id, size = new_map[j]

        visited.add(id)
        
        i = find_empty_slot(new_map, j, size)

        
        if i == -1:
            continue

        _, dest_size = new_map[i]

        new_map[i] = new_map[j]

        new_map[j] = (-1, size)

        if dest_size - size > 0:
        
            new_map = new_map[:i + 1] + [(-1, dest_size - size)] + new_map[i+1:]

    check_sum = 0

    for i, c in enumerate(map_repr(new_map)):

        if c == '.':
            continue
        
        check_sum += i * int(c)
                
                
    return check_sum         

    
        
    
    
            
with open(sys.argv[1], "r") as f:

    
    print(entire_file_checksum(f.read().strip()))
