import glob
import importlib
import re

import pytest

pytestmark = [
    pytest.mark.parametrize(
        'day', [int(re.search(r'\d+', file_)[0]) for file_ in glob.glob('src/python/aoc_day*.py')]
    ),
    pytest.mark.parametrize('part', [1, 2]),
]

with open('input/answers') as f0:
    ANSWERS = dict(line.rstrip().split(':') for line in f0)


@pytest.fixture
def module(day):
    return importlib.import_module(f'python.aoc_day{day}')


@pytest.fixture
def solution(module, part):
    return getattr(module, f'part_{part}')


@pytest.fixture
def example_input(module, part):
    return getattr(module, f'TEST_{part}_INPUT')


@pytest.fixture
def example_answer(module, part):
    return getattr(module, f'TEST_{part}_ANSWER')


@pytest.fixture
def actual_input(day):
    with open(f'input/AoC{day}') as f0:
        return f0.read()


@pytest.fixture
def actual_answer(day, part):
    return ANSWERS[f'AoC{day}-{part}']


def test_examples(solution, example_input, example_answer):
    assert solution(example_input) == example_answer


def test_solutions(solution, actual_input, actual_answer):
    sol = solution(actual_input)
    ans = type(sol)(actual_answer)  # Cast to same type
    assert sol == ans
