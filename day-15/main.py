import dataclasses
from pathlib import Path


filename = "input"


def part_one() -> None:
    total = 0
    with open(Path(__file__).parent / filename) as file:
        strings = file.readline().strip().split(",")

    for string in strings:
        total += calculate_hash(string)

    print("Part 1:")
    print(total)


def calculate_hash(string: str) -> int:
    value = 0
    for char in string:
        value += ord(char)
        value = (value * 17) % 256
    return value


@dataclasses.dataclass(frozen=True)
class Lens:
    label: str
    focal_length: int

    def focusing_power(self, box_number: int, slot_number: int) -> int:
        return (1 + box_number) * (1 + slot_number) * self.focal_length


@dataclasses.dataclass(frozen=True)
class Box:
    lenses: list[Lens] = dataclasses.field(default_factory=lambda: [])

    def add_lens(self, lens: Lens) -> None:
        if lens.label in self.labels:
            self.lenses[self.labels.index(lens.label)] = lens
        else:
            self.lenses.append(lens)

    def remove_lens(self, label: str) -> None:
        if label in self.labels:
            self.lenses.pop(self.labels.index(label))

    @property
    def labels(self) -> list[str]:
        return [x.label for x in self.lenses]


def part_two() -> None:
    total = 0
    with open(Path(__file__).parent / filename) as file:
        strings = file.readline().strip().split(",")

    boxes = [Box() for _ in range(0, 256)]
    for string in strings:
        if "=" in string:
            # add to box
            label, focal_length = string.split("=")
            box = calculate_hash(label)
            boxes[box].add_lens(Lens(label, int(focal_length)))

        else:
            # remove from box
            label = string.split("-")[0]
            box = calculate_hash(label)
            boxes[box].remove_lens(label)

    for box_number, box in enumerate(boxes):
        total += sum(
            [
                lens.focusing_power(box_number, slot_number)
                for slot_number, lens in enumerate(box.lenses)
            ]
        )

    print("Part 2:")
    print(total)


if __name__ == "__main__":
    part_one()
    part_two()
