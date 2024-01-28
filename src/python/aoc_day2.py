import numpy as np

TEST_1_INPUT = TEST_2_INPUT = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
TEST_1_ANSWER = 8
TEST_2_ANSWER = 2286

color_to_index = ['red', 'green', 'blue'].index


def iter_game_max(input_str: str):
    game = np.empty(3, dtype=np.int32)
    for line in input_str.splitlines():
        game[:] = 0
        for incoming_round in line.split(': ', 1)[1].split('; '):
            for color_pair in incoming_round.split(', '):
                count, color = color_pair.split(' ')
                idx = color_to_index(color)
                game[idx] = max(int(count), game[idx])
        yield game


def part_1(input_str: str) -> int:
    limit = np.arange(12, 15)
    return sum(
        id_ for id_, game_max in enumerate(iter_game_max(input_str), 1) if np.all(game_max <= limit)
    )


def part_2(input_str: str) -> int:
    return sum(game_min.prod() for game_min in iter_game_max(input_str))
