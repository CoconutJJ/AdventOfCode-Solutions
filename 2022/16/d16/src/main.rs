use regex::Regex;
use std::cmp::max;
use std::collections::{HashMap, HashSet, VecDeque};
use std::env;
use std::fs::File;
use std::i32;
use std::io::{BufRead, BufReader};
use std::path::Path;
use std::process;

fn bfs(
    distances: &HashMap<(String, String), i32>,
    flow_rate: &HashMap<String, i32>,
    non_zero_nodes: &Vec<String>,
) -> i32 {
    let mut q: VecDeque<(String, i32, HashSet<String>, i32)> = VecDeque::new();

    q.push_back((String::from("AA"), 30, HashSet::new(), 0));

    let mut max_total: i32 = 0;

    while q.len() != 0 {
        let (node, time, visited, total) = q.pop_front().unwrap();

        max_total = max(max_total, total);

        for r in non_zero_nodes {
            if visited.contains(r) {
                continue;
            }

            let mut new_visited = visited.clone();

            new_visited.insert(r.to_owned());

            let dist = *distances
                .get(&(node.to_owned(), r.to_owned()))
                .unwrap_or(&i32::MIN);

            if dist == i32::MIN {
                continue;
            }

            let new_time = time - dist - 1;

            if new_time < 0 {
                continue;
            }

            let new_total = total + new_time * flow_rate.get(r).unwrap();

            q.push_back((r.to_owned(), new_time, new_visited, new_total))
        }
    }

    return max_total;
}

fn floyd_warshall(distances: &mut HashMap<(String, String), i32>, nodes: &Vec<String>) {
    // run floyd-warshall on the graph
    for k in 0..nodes.len() {
        for x in 0..nodes.len() {
            for y in 0..nodes.len() {
                let curr_distance = *distances
                    .get(&(nodes[x].to_owned(), nodes[y].to_owned()))
                    .unwrap_or(&-1);

                let x_to_k = *distances
                    .get(&(nodes[x].to_owned(), nodes[k].to_owned()))
                    .unwrap_or(&-1);

                let k_to_y = *distances
                    .get(&(nodes[k].to_owned(), nodes[y].to_owned()))
                    .unwrap_or(&-1);

                if x_to_k == -1 || k_to_y == -1 {
                    continue;
                }

                if curr_distance == -1 || curr_distance > x_to_k + k_to_y {
                    distances.insert((nodes[x].to_owned(), nodes[y].to_owned()), x_to_k + k_to_y);
                }
            }
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        println!("Expected filename argument.");
        process::exit(0x0);
    }

    let path = Path::new(args.get(1).unwrap());

    let file = File::open(path).expect("Could not open file");

    let reader = BufReader::new(file);

    let re = Regex::new("Valve (.{2}) has flow rate=(\\d+); tunnels? leads? to valves? (.+)")
        .expect("Unable to compile regex");

    let mut graph: HashMap<String, Vec<String>> = HashMap::new();

    let mut flow_rate: HashMap<String, i32> = HashMap::new();

    let mut nodes: Vec<String> = Vec::new();

    let mut non_zero_flow_rate_nodes: Vec<String> = Vec::new();

    let mut distances: HashMap<(String, String), i32> = HashMap::new();

    for line in reader.lines() {
        let line = line.expect("Could not read line");

        let groups = re.captures(&line).expect("Could not capture groups");

        let node = groups
            .get(1)
            .expect("Could not get match")
            .as_str()
            .to_owned();

        let rate: i32 = groups
            .get(2)
            .expect("No flow rate value")
            .as_str()
            .parse()
            .expect("Flow rate not recognized as u32");

        let children: Vec<String> = groups
            .get(3)
            .expect("No children")
            .as_str()
            .split(", ")
            .map(String::from)
            .collect();

        for i in 0..children.len() {
            distances.insert((node.to_owned(), children[i].to_owned()), 1);
        }

        nodes.push(node.to_owned());
        graph.insert(node.to_owned(), children);
        flow_rate.insert(node.to_owned(), rate);

        if rate > 0 {
            non_zero_flow_rate_nodes.push(node);
        }
    }

    floyd_warshall(&mut distances, &nodes);

    let total = bfs(&distances, &flow_rate, &non_zero_flow_rate_nodes);

    println!("total: {}", total);
}
