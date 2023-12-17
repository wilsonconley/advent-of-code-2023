from __future__ import annotations

import dataclasses
import enum
import typing as t
from pathlib import Path

filename = "input"

Mirror = t.Literal["/", "\\"]
MIRRORS: tuple[Mirror, ...] = t.get_args(Mirror)
Splitter = t.Literal["|", "-"]
SPLITTERS: tuple[Splitter, ...] = t.get_args(Splitter)


class Direction(enum.Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def clockwise(self) -> Direction:
        return Direction((self.value + 1) % len(Direction))

    def counterclockwise(self) -> Direction:
        return Direction((self.value - 1) % len(Direction))

    def opposite(self) -> Direction:
        return Direction((self.value + 2) % len(Direction))


@dataclasses.dataclass(unsafe_hash=True)
class Beam:
    row: int
    col: int
    direction: Direction

    def reflect(self, mirror: Mirror) -> Beam:
        if mirror == "/":
            if self.direction in (Direction.EAST, Direction.WEST):
                return Beam(self.row, self.col, self.direction.counterclockwise())
            else:
                return Beam(self.row, self.col, self.direction.clockwise())
        elif mirror == "\\":
            if self.direction in (Direction.EAST, Direction.WEST):
                return Beam(self.row, self.col, self.direction.clockwise())
            else:
                return Beam(self.row, self.col, self.direction.counterclockwise())

    def split(self, splitter: Splitter) -> tuple[Beam, Beam]:
        if splitter == "-":
            return Beam(self.row, self.col, Direction.EAST), Beam(
                self.row, self.col, Direction.WEST
            )
        elif splitter == "|":
            self.direction = Direction.NORTH
            return Beam(self.row, self.col, Direction.NORTH), Beam(
                self.row, self.col, Direction.SOUTH
            )

    def move(self) -> Beam:
        if self.direction == Direction.NORTH:
            return Beam(self.row - 1, self.col, self.direction)
        elif self.direction == Direction.EAST:
            return Beam(self.row, self.col + 1, self.direction)
        elif self.direction == Direction.SOUTH:
            return Beam(self.row + 1, self.col, self.direction)
        elif self.direction == Direction.WEST:
            return Beam(self.row, self.col - 1, self.direction)
        else:
            raise ValueError("Invalid direction")


def main(grid: list[list[str]], start_beam: Beam) -> int:
    energized = [[False] * len(line) for line in grid]

    beams: list[Beam] = [start_beam]
    prev_beams = set()
    while beams:
        new_beams = []
        for beam in beams:
            # move beam
            new_beam = beam.move()

            # check if beam is out of bounds or a repeat
            if (
                new_beam.row < 0
                or new_beam.row >= len(grid)
                or new_beam.col < 0
                or new_beam.col >= len(grid[0])
                or new_beam in prev_beams
            ):
                continue

            # save beam to existing beams
            prev_beams.add(new_beam)

            # energize spot
            energized[new_beam.row][new_beam.col] = True

            # check for reflection or split
            spot = grid[new_beam.row][new_beam.col]
            if spot in MIRRORS:
                new_beams.append(new_beam.reflect(spot))
            elif spot in SPLITTERS and (
                (
                    new_beam.direction in (Direction.NORTH, Direction.SOUTH)
                    and spot == "-"
                )
                or (
                    new_beam.direction in (Direction.EAST, Direction.WEST)
                    and spot == "|"
                )
            ):
                new_beams.extend(new_beam.split(spot))
            else:
                new_beams.append(new_beam)

        beams = new_beams

    return sum([line.count(True) for line in energized])


def part_one() -> None:
    with open(Path(__file__).parent / filename) as file:
        grid = [list(line.strip()) for line in file.readlines()]
    total = main(grid, Beam(0, -1, Direction.EAST))
    print("Part 1:")
    print(total)


def part_two() -> None:
    total = 0
    with open(Path(__file__).parent / filename) as file:
        grid = [list(line.strip()) for line in file.readlines()]

    num_row = len(grid)
    num_col = len(grid[0])

    # check starting from left
    total = max(
        total,
        *[
            main(grid, Beam(row=r, col=-1, direction=Direction.EAST))
            for r in range(0, num_row)
        ],
    )

    # from top
    total = max(
        total,
        *[
            main(grid, Beam(row=-1, col=c, direction=Direction.SOUTH))
            for c in range(0, num_col)
        ],
    )

    # from right
    total = max(
        total,
        *[
            main(grid, Beam(row=r, col=num_col, direction=Direction.WEST))
            for r in range(0, num_row)
        ],
    )

    # from bottom
    total = max(
        total,
        *[
            main(grid, Beam(row=num_row, col=c, direction=Direction.NORTH))
            for c in range(0, num_col)
        ],
    )

    print("Part 2:")
    print(total)


if __name__ == "__main__":
    part_one()
    part_two()
