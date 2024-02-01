from collections import deque

TEST_1_INPUT = TEST_2_INPUT = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
TEST_1_ANSWER = 35
TEST_2_ANSWER = 46


def parse_almanac(input_str: str):
    lines = input_str.splitlines()
    seeds = map(int, lines[0].split()[1:])
    maps = []  # [[(destination, source, length), ...] ...]
    for line in filter(None, lines[2:]):
        if line.endswith(' map:'):
            maps.append(current := [])
            continue
        current.append(list(map(int, line.split())))
    return seeds, maps


def find_relevant_map(node, maps):
    for destination, source, length in maps:
        if source <= node < source + length:
            return destination, source, length
    return node, node, min((source - node for _, source, _ in maps if node < source), default=None)


def collapse_map(maps, incoming: deque):
    while incoming:
        output, length = incoming.pop()

        destination, source, map_length = find_relevant_map(output, maps)
        if map_length is None:
            yield source, length
        else:
            offset = output - source
            valid_length = min(length, map_length - offset)
            if valid_length < length:
                incoming.append((output + valid_length, length - valid_length))
            yield destination + offset, valid_length


def find_final_destination(maps, current):
    for inner_maps in maps:
        for destination, source, length in inner_maps:
            if source <= current < source + length:
                current += destination - source
                break
    return current


# TODO: There are possible speed-ups here if the maps and seeds are sorted before processing as all
# search-loops can be replaced with a single loop


def part_1(input_str: str) -> int:
    seeds, maps = parse_almanac(input_str)
    return min(find_final_destination(maps, seed) for seed in seeds)


def part_2(input_str: str) -> int:
    seeds, maps = parse_almanac(input_str)
    # NOTE: seeds is an iterator so this zip will produce chunks
    current = deque(zip(seeds, seeds, strict=True))
    for inner_maps in maps:
        current = deque(collapse_map(inner_maps, current))
    return min(start for start, _ in current)
