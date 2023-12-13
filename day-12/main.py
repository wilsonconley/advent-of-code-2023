import itertools
import re
from pathlib import Path

from tqdm import tqdm

filename = "input"


def combinations(size: int, min_size: int = 0) -> set[tuple[int]]:
    combos = set()
    for r in range(min_size, size):
        for combo in itertools.combinations(range(0, size), r=r):
            combos.add(combo)
    if min_size == size:
        combos.add(range(0, size))
    return combos


def part_one() -> None:
    total = 0
    with open(Path(__file__).parent / filename) as file:
        for line in tqdm(file):
            springs, groups_str = line.split()
            groups = [int(group) for group in groups_str.split(",")]
            num_unknown = springs.count("?")
            num_broken_desired = sum(groups)
            num_broken_current = springs.count("#")
            num_broken_needed = num_broken_desired - num_broken_current

            arrangements = 0
            for combo in combinations(num_unknown, min_size=num_broken_needed):
                count = 0
                tmp = ""
                for spring in springs:
                    if spring == "?":
                        if count in combo:
                            tmp += "#"
                        else:
                            tmp += "."
                        count += 1
                    else:
                        tmp += spring

                if [len(group) for group in re.findall("#+", tmp)] == groups:
                    arrangements += 1

            total += arrangements

    print("Part 1:")
    print(total)


def part_two() -> None:
    total = 0
    with open(Path(__file__).parent / filename) as file:
        for line in tqdm(file):
            springs, groups_str = line.split()
            groups = [int(group) for group in groups_str.split(",")]

            unfolded_springs = springs
            unfolded_groups = groups
            for _ in range(0, 4):
                unfolded_springs = unfolded_springs + "?" + springs
                unfolded_groups = unfolded_groups + groups

            springs = unfolded_springs
            groups = unfolded_groups

            num_unknown = springs.count("?")
            num_broken_desired = sum(groups)
            num_broken_current = springs.count("#")
            num_broken_needed = num_broken_desired - num_broken_current

            arrangements = 0
            for combo in combinations(num_unknown, min_size=num_broken_needed):
                count = 0
                tmp = ""
                for spring in springs:
                    if spring == "?":
                        if count in combo:
                            tmp += "#"
                        else:
                            tmp += "."
                        count += 1
                    else:
                        tmp += spring

                if [len(group) for group in re.findall("#+", tmp)] == groups:
                    arrangements += 1

            total += arrangements

    print("Part 2:")
    print(total)


if __name__ == "__main__":
    part_one()
    part_two()
