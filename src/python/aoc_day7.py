import enum

TEST_1_INPUT = TEST_2_INPUT = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
TEST_1_ANSWER = 6440
TEST_2_ANSWER = 5905


class Card(enum.IntEnum):
    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2
    JOKER = 1

    @classmethod
    def parse(cls, card: str, *, jokers_enabled: bool):  # noqa: PLR0911
        match card:
            case 'A':
                return cls.ACE
            case 'K':
                return cls.KING
            case 'Q':
                return cls.QUEEN
            case 'J' if jokers_enabled:
                return cls.JOKER
            case 'J':
                return cls.JACK
            case 'T':
                return cls.TEN
            case _:
                return cls(int(card))


class HandType(enum.IntEnum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0

    @classmethod
    def from_cards(cls, cards: list[Card]):  # noqa: PLR0911
        counts = {}
        for card in cards:
            counts[card] = counts.get(card, 0) + 1

        n_jokers = counts.pop(Card.JOKER, 0)

        match max(counts.values(), default=0) + n_jokers:
            case 5:
                return cls.FIVE_OF_A_KIND
            case 4:
                return cls.FOUR_OF_A_KIND
            case 3 if len(counts) == 2:
                return cls.FULL_HOUSE
            case 3:
                return cls.THREE_OF_A_KIND
            case 2 if len(counts) == 3:
                return cls.TWO_PAIR
            case 2:
                return cls.ONE_PAIR
            case 1:
                return cls.HIGH_CARD
            case _:
                raise ValueError(cards)


class Hand:
    hand: HandType
    cards: list[Card]

    def __init__(self, cards: list[str], *, jokers_enabled: bool):
        self.cards = [Card.parse(card, jokers_enabled=jokers_enabled) for card in cards]
        self.hand = HandType.from_cards(self.cards)

    def __lt__(self, other):
        # Compare first hands, falling back to lexical comparison of cards in case of ties
        return self.hand < other.hand if self.hand != other.hand else self.cards < other.cards


def parse_input(input_str: str, *, jokers_enabled: bool):
    for row in input_str.splitlines():
        cards, bid = row.split()
        yield Hand(cards, jokers_enabled=jokers_enabled), int(bid)


def solve(input_str: str, *, jokers_enabled: bool):
    # Sort hands and bids based on hand strength
    hands_and_bids = sorted(parse_input(input_str, jokers_enabled=jokers_enabled))
    # Return sum of bids weighted by strnegth order
    return sum(i * bid for i, (_, bid) in enumerate(hands_and_bids, start=1))


def part_1(input_str: str) -> int:
    return solve(input_str, jokers_enabled=False)


def part_2(input_str: str) -> int:
    return solve(input_str, jokers_enabled=True)
