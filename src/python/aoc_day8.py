import itertools as it

import numpy as np

TEST_1_INPUT = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""
TEST_1_ANSWER = 6
TEST_2_INPUT = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
TEST_2_ANSWER = 6


def parse_sequence_and_map(input_str: str) -> tuple[str, dict[str, tuple[str, str]]]:
    lines = input_str.splitlines()

    # sequence of indices to traverse. Left is 0 and right is 1
    seq = [int(c == 'R') for c in lines[0]]

    map_ = {}
    for line in lines[2:]:
        src = line[:3]
        left = line[7:10]
        right = line[12:15]
        map_[src] = (left, right)
    return seq, map_


def traverse_until_target(map_, seq, start, target_predicate):
    current = start
    for step, next_ in enumerate(it.cycle(seq), start=1):
        current = map_[current][next_]
        if target_predicate(current):
            return step
    raise ValueError('Empty sequence')


def part_1(input_str: str) -> int:
    seq, map_ = parse_sequence_and_map(input_str)
    return traverse_until_target(map_, seq, 'AAA', 'ZZZ'.__eq__)


def part_2(input_str: str) -> int:
    seq, map_ = parse_sequence_and_map(input_str)
    starts = (key for key in map_ if key.endswith('A'))
    lengths = [
        traverse_until_target(map_, seq, start, lambda s: s.endswith('Z')) for start in starts
    ]
    return np.lcm.reduce(lengths)  # This is true for the input, but not necessarily for any input
