use std::collections::{HashSet, VecDeque};
use std::fs::File;
use std::io::BufReader;
use std::path::Path;
struct State {
    ore: u32,
    clay: u32,
    obsidian: u32,
    geode: u32,
    ore_bots: u32,
    clay_bots: u32,
    obsidian_bots: u32,
    geode_bots: u32,
    minute: u32,
}

fn state_max_geode_heuristic(st: &State) -> u32 {
    return st.minute * st.geode_bots + st.geode + st.minute * (st.minute + 1) / 2;
}

fn encoded_state(st: &State) -> (u32, u32, u32, u32, u32, u32, u32, u32, u32) {
    return (
        st.ore,
        st.clay,
        st.obsidian,
        st.geode,
        st.ore_bots,
        st.clay_bots,
        st.obsidian_bots,
        st.geode_bots,
        st.minute,
    );
}

fn update_state(st: &mut State) {
    st.ore += st.ore_bots;
    st.clay += st.clay_bots;
    st.obsidian += st.obsidian_bots;
    st.geode += st.geode_bots;
    st.minute -= 1;
}

fn main() {
    let mut q: VecDeque<State> = VecDeque::new();

    while q.len() != 0 {
        let st = q.pop_front().unwrap();
    }
}
