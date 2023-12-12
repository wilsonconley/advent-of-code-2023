import enum
import itertools
from dataclasses import dataclass
from pathlib import Path

filename = "sample5"


class Directions(enum.Enum):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"


@dataclass(frozen=True)
class Position:
    row: int
    col: int


def move(
    pos: Position, grid: list[list[str]], prev_direction: Directions
) -> tuple[Position, Directions]:
    num_row = len(grid)
    num_col = len(grid[0])

    val = grid[pos.row][pos.col]
    if val == "S":
        if (
            prev_direction != Directions.SOUTH
            and pos.row > 0
            and grid[pos.row - 1][pos.col] in ("|", "7", "F")
        ):
            return (Position(pos.row - 1, pos.col), Directions.NORTH)
        elif (
            prev_direction != Directions.WEST
            and pos.col < num_col - 1
            and grid[pos.row][pos.col + 1] in ("-", "J", "7")
        ):
            return (Position(pos.row, pos.col + 1), Directions.EAST)
        elif (
            prev_direction != Directions.NORTH
            and pos.row < num_row - 1
            and grid[pos.row + 1][pos.col] in ("|", "L", "J")
        ):
            return (Position(pos.row + 1, pos.col), Directions.SOUTH)
        elif (
            prev_direction != Directions.EAST
            and pos.col > 0
            and grid[pos.row][pos.col - 1] in ("-", "F", "L")
        ):
            return (Position(pos.row, pos.col - 1), Directions.WEST)
        else:
            # for r in range(pos.row - 1, pos.row + 2):
            #     print(grid[r][pos.col - 1 : pos.col + 2])
            #     for c in range(pos.col - 1, pos.col + 2):
            #         print(grid[r][c])
            raise ValueError("No path found")
    elif val == "|":
        if prev_direction == Directions.NORTH:
            return (Position(pos.row - 1, pos.col), Directions.NORTH)
        elif prev_direction == Directions.SOUTH:
            return (Position(pos.row + 1, pos.col), Directions.SOUTH)
        else:
            raise ValueError("No path found")
    elif val == "-":
        if prev_direction == Directions.EAST:
            return (Position(pos.row, pos.col + 1), Directions.EAST)
        elif prev_direction == Directions.WEST:
            return (Position(pos.row, pos.col - 1), Directions.WEST)
        else:
            raise ValueError("No path found")
    elif val == "L":
        if prev_direction == Directions.SOUTH:
            return (Position(pos.row, pos.col + 1), Directions.EAST)
        elif prev_direction == Directions.WEST:
            return (Position(pos.row - 1, pos.col), Directions.NORTH)
        else:
            raise ValueError("No path found")
    elif val == "J":
        if prev_direction == Directions.SOUTH:
            return (Position(pos.row, pos.col - 1), Directions.WEST)
        elif prev_direction == Directions.EAST:
            return (Position(pos.row - 1, pos.col), Directions.NORTH)
        else:
            raise ValueError("No path found")
    elif val == "7":
        if prev_direction == Directions.NORTH:
            return (Position(pos.row, pos.col - 1), Directions.WEST)
        elif prev_direction == Directions.EAST:
            return (Position(pos.row + 1, pos.col), Directions.SOUTH)
        else:
            raise ValueError("No path found")
    elif val == "F":
        if prev_direction == Directions.NORTH:
            return (Position(pos.row, pos.col + 1), Directions.EAST)
        elif prev_direction == Directions.WEST:
            return (Position(pos.row + 1, pos.col), Directions.SOUTH)
        else:
            raise ValueError("No path found")
    else:
        raise ValueError("No path found")


def part_one() -> list[list[int]]:
    with open(Path(__file__).parent / filename) as file:
        grid = [list(line.strip()) for line in file.readlines()]

    # num_row = len(grid)
    # num_col = len(grid[0])

    # Find starting position
    start_pos = None
    for i, row in enumerate(grid):
        if "S" in row:
            start_pos = Position(i, row.index("S"))
            break
    assert start_pos is not None

    # print(start_pos)

    # Get possible starting directions
    start_directions = set()
    for check_direction in Directions:
        _, direction = move(start_pos, grid, prev_direction=check_direction)
        start_directions.add(direction)
    # print(start_directions)

    if start_directions == {Directions.NORTH, Directions.SOUTH}:
        start_char = "|"
    elif start_directions == {Directions.EAST, Directions.WEST}:
        start_char = "-"
    elif start_directions == {Directions.EAST, Directions.NORTH}:
        start_char = "L"
    elif start_directions == {Directions.NORTH, Directions.WEST}:
        start_char = "J"
    elif start_directions == {Directions.SOUTH, Directions.WEST}:
        start_char = "7"
    elif start_directions == {Directions.EAST, Directions.SOUTH}:
        start_char = "F"
    else:
        raise ValueError("No start char")

    grid[start_pos.row][start_pos.col] = start_char

    # Calculate each route
    counts = [[0] * len(row) for row in grid]
    for start_direction in start_directions:
        # print("---")
        # print("begin")
        # print(start_direction)
        # print("---")
        count = 0
        pos = start_pos
        if start_direction == Directions.NORTH:
            direction = Directions.SOUTH
        elif start_direction == Directions.SOUTH:
            direction = Directions.NORTH
        elif start_direction == Directions.EAST:
            direction = Directions.WEST
        else:
            direction = Directions.EAST

        # direction = start_direction
        while count == 0 or pos != start_pos:
            print(pos)
            print(direction)
            if counts[pos.row][pos.col] == 0:
                counts[pos.row][pos.col] = count
            else:
                counts[pos.row][pos.col] = min(count, counts[pos.row][pos.col])
            pos, direction = move(pos, grid, direction)
            count += 1
            # for line in counts:
            #     print(line)

    # for line in counts:
    #     print(line)

    print("Part 1:")
    print(max([max(line) for line in counts]))

    return counts


def part_two(counts: list[list[int]]) -> None:
    # with open(Path(__file__).parent / filename) as file:
    #     total = 0
    for line in counts:
        print(line)

    counts = [[int(bool(x)) for x in line] for line in counts]

    num_row = len(counts)
    num_col = len(counts[0])

    # prev_counts = [line for line in counts]

    # check initial exposed locations
    for r, c in itertools.product(range(0, num_row), range(0, num_col)):
        if counts[r][c] == 0 and (
            r == 0
            or c == 0
            or r == num_row - 1
            or c == num_col - 1
            or len([line[c] for line in counts[0 : r + 1] if line[c] > 0]) == 0
            or len([line[c] for line in counts[r:num_row] if line[c] > 0]) == 0
            or len([x for x in counts[r][0 : c + 1] if x > 0]) == 0
            or len([x for x in counts[r][c:num_col] if x > 0]) == 0
        ):
            counts[r][c] = -1

    changed = True
    while changed:
        changed = False
        for r, c in itertools.product(range(1, num_row - 1), range(1, num_col - 1)):
            if counts[r][c] == 0:
                for check_r in range(r - 1, -1, -1):  # up
                    if counts[check_r][c] == -1:
                        counts[r][c] = -1
                        changed = True
                        break
                    elif counts[check_r][c] > 0:
                        break
                for check_r in range(r + 1, num_row):  # down
                    if counts[check_r][c] == -1:
                        counts[r][c] = -1
                        changed = True
                        break
                    elif counts[check_r][c] > 0:
                        break
                for check_c in range(c - 1, -1, -1):  # left
                    if counts[r][check_c] == -1:
                        counts[r][c] = -1
                        changed = True
                        break
                    elif counts[r][check_c] > 0:
                        break
                for check_c in range(c + 1, num_col):  # right
                    if counts[r][check_c] == -1:
                        counts[r][c] = -1
                        changed = True
                        break
                    elif counts[r][check_c] > 0:
                        break

        # print("in loop")
        for line in counts:
            print(line)

    # print("done")
    # for line in counts:
    #     fmt = ""
    #     for x in line:
    #         if x == -1:
    #             fmt += "O"
    #         elif x == 0:
    #             fmt += "I"
    #         else:
    #             fmt += "X"
    #     print(fmt)
    # print(prev_counts)
    # print(counts)
    # if prev_counts == counts:
    #     check = False

    print("Part 2:")
    print(sum([line.count(0) for line in counts]))


if __name__ == "__main__":
    counts = part_one()
    part_two(counts)
