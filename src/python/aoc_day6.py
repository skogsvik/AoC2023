import numpy as np

TEST_1_INPUT = TEST_2_INPUT = """Time:      7  15   30
Distance:  9  40  200
"""
TEST_1_ANSWER = 288
TEST_2_ANSWER = 71503


def find_number_of_winners(time, best_distance):
    # inequality to find the width of is charge * (time-charge) > best_distance
    # or 0.5 (time - half_width) < charge < 0.5 (time + half_width)
    # where half_width = sqrt(time**2 - 4 best_distance)
    # NOTE: offset is to win tie-breakers
    half_width = np.sqrt(time**2 - 4 * best_distance) - 1e-3
    min_charge = np.ceil(0.5 * (time - half_width)).astype(int)
    max_charge = np.floor(0.5 * (time + half_width)).astype(int)
    return max_charge - min_charge + 1


def part_1(input_str: str) -> int:
    time_str, distance_str = input_str.split('\n', 1)
    time = np.array(time_str.split()[1:], dtype=int)
    distance = np.array(distance_str.split()[1:], dtype=int)
    return np.prod(find_number_of_winners(time, distance))


def part_2(input_str: str) -> int:
    time_str, distance_str = input_str.replace(' ', '').split('\n', 1)
    time = int(time_str.split(':', 1)[1])
    distance = int(distance_str.split(':', 1)[1])
    return np.prod(find_number_of_winners(time, distance))
