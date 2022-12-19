use std::cmp;
use std::env;
use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

fn main() {
    let args: Vec<String> = env::args().collect();

    let file = File::open(Path::new(&args[1])).expect("Could not open file");

    let reader = BufReader::new(file);

    let mut max = 0u32;
    let mut curr_total = 0u32;

    for line in reader.lines() {
        let line = line.unwrap();
        let n = line.chars().count();

        if n <= 1 {
            max = cmp::max(max, curr_total);
            curr_total = 0;
            continue;
        }

        match line.trim().parse::<u32>() {
            Ok(v) => curr_total += v,
            Err(e) => panic!("{}", e),
        }
    }
    max = cmp::max(max, curr_total);

    println!("{}", max);
}
