import dataclasses
import typing as t
from pathlib import Path

filename = "sample"


@dataclasses.dataclass(frozen=True)
class Range:
    src: int
    dst: int
    length: int

    def __contains__(self, value: int) -> bool:
        return value >= self.src and value < self.src + self.length

    def transform(self, value: int) -> int:
        return self.dst + value - self.src


def part_one():
    with open(Path(__file__).parent / filename) as file:
        contents = file.readlines()

    seeds = contents[0].split(":")[1].split()

    mappings: list[list[Range]] = []
    temp_list: list[Range] = []
    idx = 3
    while idx < len(contents):
        line = contents[idx].strip()
        if line == "":
            mappings.append(temp_list)
            temp_list = []
            idx += 1
        else:
            dst, src, length = [int(x) for x in line.split()]
            temp_list.append(Range(src, dst, length))
        idx += 1
    mappings.append(temp_list)

    mapped_values = []
    for seed in seeds:
        my_val = int(seed)
        for stage in mappings:
            for range_ in stage:
                if my_val in range_:
                    my_val = range_.transform(my_val)
                    break
        mapped_values.append(my_val)

    print("Part 1:")
    print(min(mapped_values))


def part_two() -> None:
    with open(Path(__file__).parent / filename) as file:
        contents = file.readlines()

    values = contents[0].split(":")[1].split()
    seed_max = 0
    for idx in range(0, len(values), 2):
        # start = int(values[idx])
        # stop = start + int(values[idx + 1])
        seed_max = max(seed_max, int(values[idx]) + int(values[idx + 1]) - 1)

    # ranges = [0]
    # transforms = [0]

    mappings: list[list[Range]] = []
    temp_list: list[Range] = []
    idx = 3
    while idx < len(contents):
        line = contents[idx].strip()
        if line == "":
            mappings.append(temp_list)
            temp_list = []
            idx += 1
        else:
            dst, src, length = [int(x) for x in line.split()]
            temp_list.append(Range(src, dst, length))
        idx += 1
    mappings.append(temp_list)

    print(mappings)

    ranges = []
    transforms = []

    for mapping in mappings:
        for range_ in mapping:
            pass
            # transforms[(range_.src] = range_.dst - range_.src

    print("Part 2:")
    # print(min(mapped_values))


if __name__ == "__main__":
    part_one()
    part_two()
