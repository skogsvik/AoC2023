import numpy as np

TEST_1_INPUT = TEST_2_INPUT = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
TEST_1_ANSWER = 13
TEST_2_ANSWER = 30


def parse_scratcher(input_str: str) -> (np.ndarray, np.ndarray):
    n_lines = len(lines := input_str.splitlines())
    first = lines[0].split()
    n_winning = first.index('|') - 2
    n_ours = len(first) - n_winning - 3

    winning_series = np.empty((n_lines, n_winning), dtype=np.int32)
    our_series = np.empty((n_lines, n_ours), dtype=np.int32)

    for winning_line, our_line, line in zip(winning_series, our_series, lines, strict=True):
        winning, our = line.split(': ', 1)[1].split(' | ')
        winning_line[:] = winning.split()
        our_line[:] = our.split()

    return winning_series, our_series


def intersecting_per_row(winning, ours):
    for winning_line, our_line in zip(winning, ours, strict=True):
        yield np.intersect1d(winning_line, our_line).size


def part_1(input_str: str) -> int:
    winning, ours = parse_scratcher(input_str)
    counts = intersecting_per_row(winning, ours)
    return sum(p and 2 ** (p - 1) for p in counts)


def part_2(input_str: str) -> int:
    winning, ours = parse_scratcher(input_str)
    scratchers = np.ones(winning.shape[0], dtype=np.int32)
    for row, count in enumerate(intersecting_per_row(winning, ours)):
        scratchers[row + 1 : row + 1 + count] += scratchers[row]
    return scratchers.sum()
