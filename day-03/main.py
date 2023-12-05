import contextlib
import itertools
from pathlib import Path

filename = "input"

SYMBOL = -1
NO_SYMBOL = 0


def parse_line(line: str) -> list[int]:
    output = []
    num = ""
    for char in line:
        if char in "0123456789":
            # begin number
            num += char
        else:
            if num:
                # end number
                for _ in range(0, len(num)):
                    output.append(int(num))
                num = ""
            if char == ".":
                # not symbol
                output.append(NO_SYMBOL)
            else:
                # is symbol
                output.append(SYMBOL)
    if num:
        # check for number at end of line
        for _ in range(0, len(num)):
            output.append(int(num))
    return output


def parse_line_2(line: str) -> list[int]:
    output = []
    num = ""
    for char in line:
        if char in "0123456789":
            # begin number
            num += char
        else:
            if num:
                # end number
                for _ in range(0, len(num)):
                    output.append(int(num))
                num = ""
            if char == "*":
                # gear
                output.append(SYMBOL)
            else:
                # not gear
                output.append(NO_SYMBOL)
    if num:
        # check for number at end of line
        for _ in range(0, len(num)):
            output.append(int(num))
    return output


if __name__ == "__main__":
    # Part 1
    with open(Path(__file__).parent / filename) as file:
        grid = [parse_line(line.strip()) for line in file.readlines()]

    total = 0
    for r, line in enumerate(grid):
        c = 0
        while c < len(line):
            number = line[c]
            if number > 0:  # this is a number
                start_c = c - 1
                stop_c = c + 1
                while stop_c < len(line) and line[stop_c] == number:
                    stop_c += 1
                for pos in itertools.product(
                    range(r - 1, r + 2),
                    range(start_c, stop_c + 1),
                ):
                    with contextlib.suppress(IndexError):
                        if grid[pos[0]][pos[1]] == SYMBOL:
                            total += number
                            break
                c = stop_c
            else:
                c += 1
    print("Part 1:")
    print(total)

    # Part 2
    with open(Path(__file__).parent / filename) as file:
        grid = [parse_line_2(line.strip()) for line in file.readlines()]

    total = 0
    for r, line in enumerate(grid):
        for c, number in enumerate(line):
            if number == SYMBOL:
                my_numbers = []
                for check_r in range(max(r - 1, 0), min(r + 2, len(grid))):
                    check_c = c - 1
                    while (
                        check_c >= 0
                        and check_c < len(grid[check_r])
                        and check_c <= c + 1
                    ):
                        if grid[check_r][check_c] > 0:
                            my_numbers.append(grid[check_r][check_c])
                            check_c += 1
                            while (
                                check_c < len(grid[check_r])
                                and grid[check_r][check_c] == my_numbers[-1]
                            ):
                                check_c += 1
                        else:
                            check_c += 1
                if len(my_numbers) == 2:
                    total += my_numbers[0] * my_numbers[1]
    print("Part 2:")
    print(total)
