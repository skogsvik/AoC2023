import re

TEST_1_INPUT = '1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet'
TEST_1_ANSWER = 142
TEST_2_INPUT = (
    'two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n'
    '4nineeightseven2\nzoneight234\n7pqrstsixteen'
)
TEST_2_ANSWER = 281

NUMBER_MAP = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
}


def part_1(input_str: str) -> int:
    total = 0
    for line in input_str.splitlines():
        digits = re.findall(r'\d', line)
        total += int(digits[0] + digits[-1])
    return total


def part_2(input_str: str) -> int:
    total = 0
    for line in input_str.splitlines():
        # NOTE: The hacky lookahead is used to catch overlapping matches
        numbers = re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)
        total += 10 * NUMBER_MAP[numbers[0]] + NUMBER_MAP[numbers[-1]]
    return total
