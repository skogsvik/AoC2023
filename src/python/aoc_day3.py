import itertools as it
import re

import numpy as np

TEST_1_INPUT = TEST_2_INPUT = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
TEST_1_ANSWER = 4361
TEST_2_ANSWER = 467835

EMPTY = -1
TARGET = -2
NOT_A_NUMBER_INDEX = {EMPTY, TARGET}
N_NUMBERS_IN_A_GEAR = 2


def parse_input(input_str: str, target_filter):
    rows = input_str.count('\n')
    if input_str[-1] != '\n':
        rows += 1
    cols = input_str.index('\n')
    schematic = np.full((rows, cols), EMPTY, dtype=np.int32)

    input_str = input_str.replace('\n', '')

    found_numbers = list(re.finditer(r'\d+', input_str))
    numbers = np.asanyarray([int(match[0]) for match in found_numbers])
    for idx, num in enumerate(found_numbers):
        schematic.flat[num.start() : num.end()] = idx

    for i, c in enumerate(input_str):
        if target_filter(c):
            schematic.flat[i] = TARGET

    return numbers, schematic


def find_adjacent_indices(schematic, x, y):
    xd, yd = zip(*it.product([-1, 0, 1], repeat=2), strict=True)
    x_len, y_len = schematic.shape
    adjacent_x = np.clip(x[:, None] + xd, 0, x_len - 1).ravel()
    adjacent_y = np.clip(y[:, None] + yd, 0, y_len - 1).ravel()
    return list(set(schematic[adjacent_x, adjacent_y]) - NOT_A_NUMBER_INDEX)


def is_part(character):
    return character != '.' and not character.isdigit()


def part_1(input_str: str) -> int:
    numbers, schematic = parse_input(input_str, is_part)
    adjacent_number_indices = find_adjacent_indices(schematic, *np.nonzero(schematic == TARGET))
    return numbers[adjacent_number_indices].sum()


def part_2(input_str: str) -> int:
    numbers, schematic = parse_input(input_str, '*'.__eq__)
    total = 0
    for x, y in np.argwhere(schematic == TARGET)[:, :, None]:
        adjacent_number_indices = find_adjacent_indices(schematic, x, y)
        if len(adjacent_number_indices) == N_NUMBERS_IN_A_GEAR:
            total += np.prod(numbers[adjacent_number_indices])
    return total
