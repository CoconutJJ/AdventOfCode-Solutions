use std::env::args;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

fn parse_input() -> Vec<i64> {
    let argv: Vec<String> = args().collect();

    let f = File::open(Path::new(&argv[1])).unwrap();

    let reader = BufReader::new(f);

    let data: Vec<i64> = reader
        .lines()
        .map(|l| l.unwrap().parse::<i64>().unwrap())
        .collect();

    return data;
}

fn shuffle_list(original_nums: &Vec<i64>, current_positions: &mut Vec<usize>) {
    for (i, &v) in original_nums.iter().enumerate() {
        let pos = current_positions.iter().position(|&r| r == i).unwrap() as i64;

        current_positions.remove(pos as usize);

        let new_pos = (pos + v).rem_euclid(current_positions.len() as i64);

        current_positions.insert(new_pos as usize, i);
    }
}

fn find_zero_index(nums: &Vec<i64>) -> i64 {
    return nums.iter().position(|&r| r == 0).unwrap() as i64;
}

fn part_1() -> i64 {
    let nums = parse_input();

    let mut positions: Vec<_> = (0..nums.len()).collect();

    shuffle_list(&nums, &mut positions);

    let zero_idx = find_zero_index(&positions.iter().map(|&r| nums[r]).collect::<Vec<i64>>());

    let message: Vec<i64> = positions.iter().map(|&r| nums[r]).collect();

    return [1000, 2000, 3000]
        .map(|r| message[(r + zero_idx).rem_euclid(message.len() as i64) as usize])
        .iter()
        .sum();
}

fn part_2() -> i64 {
    let decryption_key = 811_589_153i64;

    let nums: Vec<i64> = parse_input().iter().map(|&r| r * decryption_key).collect();

    let mut positions: Vec<_> = (0..nums.len()).collect();

    for _ in 0..10 {
        shuffle_list(&nums, &mut positions);
    }

    let zero_idx = find_zero_index(&positions.iter().map(|&r| nums[r]).collect::<Vec<i64>>());

    let message: Vec<i64> = positions.iter().map(|&r| nums[r]).collect();

    return [1000, 2000, 3000]
        .map(|r| message[(r + zero_idx).rem_euclid(message.len() as i64) as usize])
        .iter()
        .sum();
}

fn main() {
    println!("Part 1: {}", part_1());
    println!("Part 2: {}", part_2());
}
