from __future__ import annotations

import dataclasses
import enum
from pathlib import Path


filename = "input"


@dataclasses.dataclass(frozen=True)
class Card:
    symbol: str
    jokers: bool = False

    @property
    def value(self) -> int:
        if self.symbol == "A":
            return 14
        elif self.symbol == "K":
            return 13
        elif self.symbol == "Q":
            return 12
        elif self.symbol == "J":
            if self.jokers:
                return 0
            else:
                return 11
        elif self.symbol == "T":
            return 10
        else:
            return int(self.symbol)

    def __gt__(self, other: Card) -> bool:
        return self.value > other.value

    def __eq__(self, other: Card) -> bool:
        return self.value == other.value


class Type(enum.Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0

    def __gt__(self, other: Type) -> bool:
        return self.value > other.value


class HandCompare(enum.Enum):
    GREATER_THAN = enum.auto()
    EQUAL_TO = enum.auto()
    LESS_THAN = enum.auto()


def compare_hands(a: Hand, b: Hand) -> HandCompare:
    """Returns comparison wrt a, i.e. a > b, a == b, or a < b."""
    if a.type_ > b.type_:
        return HandCompare.GREATER_THAN
    elif a.type_ == b.type_:
        for my_card, other_card in zip(a.cards, b.cards):
            if my_card > other_card:
                return HandCompare.GREATER_THAN
            elif my_card == other_card:
                continue
            else:
                return HandCompare.LESS_THAN
        return HandCompare.EQUAL_TO
    else:
        return HandCompare.LESS_THAN


@dataclasses.dataclass(frozen=True)
class Hand:
    cards: list[Card]
    bid: int

    @property
    def type_(self) -> Type:
        # remove jokers from base count
        joker_card = Card("J", jokers=True)
        cards_to_count = [card for card in self.cards if card != joker_card]
        num_jokers = self.cards.count(joker_card)
        counts = [self.cards.count(card) for card in cards_to_count]
        if len(counts) == 0 or max(counts) + num_jokers == 5:
            return Type.FIVE_OF_A_KIND
        elif max(counts) + num_jokers == 4:
            return Type.FOUR_OF_A_KIND
        elif (
            set(sorted(counts)) == {2, 3}
            or (num_jokers == 3)
            or (num_jokers == 2 and max(counts) >= 2)
            or (num_jokers == 1 and (max(counts) == 3 or counts.count(2) == 4))
        ):
            return Type.FULL_HOUSE
        elif max(counts) + num_jokers == 3:
            return Type.THREE_OF_A_KIND
        elif (
            counts.count(2) == 4
            or (num_jokers == 2)
            or (num_jokers == 1 and (counts.count(2) == 2))
        ):
            return Type.TWO_PAIR
        elif counts.count(2) == 2 or num_jokers == 1:
            return Type.ONE_PAIR
        else:
            return Type.HIGH_CARD

    def __gt__(self, other: Hand) -> bool:
        return compare_hands(self, other) == HandCompare.GREATER_THAN

    def __lt__(self, other: Hand) -> bool:
        return compare_hands(self, other) == HandCompare.LESS_THAN

    def __eq__(self, other: Hand) -> bool:
        return compare_hands(self, other) == HandCompare.EQUAL_TO

    def __ge__(self, other: Hand) -> bool:
        return compare_hands(self, other) != HandCompare.LESS_THAN

    def __le__(self, other: Hand) -> bool:
        return compare_hands(self, other) != HandCompare.GREATER_THAN

    def __ne__(self, other: Hand) -> bool:
        return compare_hands(self, other) != HandCompare.EQUAL_TO


def parse_line(line: str, jokers: bool = False) -> tuple[list[Card], int]:
    cards, bid = line.split()
    return ([Card(card, jokers) for card in cards], int(bid))


def part_one():
    with open(Path(__file__).parent / filename) as file:
        hands = [Hand(*parse_line(line)) for line in file.readlines()]

    winnings = sum([(i + 1) * hand.bid for i, hand in enumerate(sorted(hands))])

    print("Part 1:")
    print(winnings)


def part_two() -> None:
    with open(Path(__file__).parent / filename) as file:
        hands = [Hand(*parse_line(line, jokers=True)) for line in file.readlines()]

    winnings = sum([(i + 1) * hand.bid for i, hand in enumerate(sorted(hands))])

    # last_type = Type.HIGH_CARD
    # print(last_type)
    # for hand in sorted(hands):
    #     if hand.type_ != last_type:
    #         print(hand.type_)
    #         last_type = hand.type_
    #     print([card.value for card in hand.cards])

    print("Part 2:")
    print(winnings)


if __name__ == "__main__":
    part_one()
    part_two()
