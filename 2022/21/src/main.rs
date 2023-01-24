use std::env::args;
use std::fs::File;
use std::io::{BufRead, BufReader, Read};
use std::path::Path;

fn parse_input() -> Vec<String> {
    let argv: Vec<String> = args().collect();
    let f = File::open(Path::new(&argv[1])).unwrap();

    let lines: Vec<String> = BufReader::new(f).lines().map(|r| r.unwrap()).collect();

    return lines;
}

fn main() {}
