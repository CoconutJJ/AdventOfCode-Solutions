use std::cmp::max;
use std::collections::{HashSet, VecDeque};
use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

fn main() {
    let file = File::open(Path::new(
        env::args().collect::<Vec<String>>().get(1).unwrap(),
    ))
    .unwrap();

    let reader = BufReader::new(file);

    let mut area: i32 = 0;

    let mut cubes: HashSet<(i32, i32, i32)> = HashSet::new();

    let mut max_x = 0;
    let mut max_y = 0;
    let mut max_z = 0;

    for line in reader.lines() {
        let line = line.unwrap();

        let values: Vec<i32> = line.split(",").map(|r| r.parse::<i32>().unwrap()).collect();

        area += 6;

        max_x = max(max_x, values[0]);
        max_y = max(max_y, values[1]);
        max_z = max(max_z, values[2]);

        let neigbours = vec![
            (values[0] + 1, values[1], values[2]),
            (values[0] - 1, values[1], values[2]),
            (values[0], values[1] + 1, values[2]),
            (values[0], values[1] - 1, values[2]),
            (values[0], values[1], values[2] + 1),
            (values[0], values[1], values[2] - 1),
        ];

        for v in neigbours {
            if cubes.contains(&v) {
                area -= 2
            }
        }

        cubes.insert((values[0], values[1], values[2]));
    }
    println!("Total Area: {}", area);

    let mut visited: HashSet<(i32, i32, i32)> = HashSet::new();

    let mut q: VecDeque<(i32, i32, i32)> = VecDeque::new();

    q.push_back((max_x + 1, max_y + 1, max_z + 1));
    visited.insert((max_x + 1, max_y + 1, max_z + 1));

    let mut area: i32 = 0;

    while q.len() != 0 {
        let (x, y, z) = q.pop_front().unwrap();
        println!("{} {} {}", x, y, z);
        let neigbours = vec![
            (x + 1, y, z),
            (x - 1, y, z),
            (x, y + 1, z),
            (x, y - 1, z),
            (x, y, z + 1),
            (x, y, z - 1),
        ];

        for (i, j, k) in neigbours {
            if visited.contains(&(i, j, k)) {
                continue;
            }

            if cubes.contains(&(i, j, k)) {
                area += 1;
            } else if -1 <= i
                && i <= max_x + 1
                && -1 <= j
                && j <= max_y + 1
                && -1 <= z
                && z <= max_z + 1
            {
                q.push_back((i, j, k));
                visited.insert((i, j, k));
            }
        }
    }

    println!("Exterior Area: {}", area);
}
