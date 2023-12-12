import itertools
from pathlib import Path

filename = "input"
debug = False


def part_one() -> None:
    print("Part 1:")
    print(main(multiplier=2))


def part_two() -> None:
    print("Part 2:")
    print(main(multiplier=1000000))


def main(multiplier: int) -> int:
    with open(Path(__file__).parent / filename) as file:
        grid = [list(line.strip()) for line in file.readlines()]

    expanded_grid = []
    for line in grid:
        if "#" not in line:
            expanded_grid.append(["X"] * len(line))
        expanded_grid.append(line)
    offset = 0
    for c in range(0, len(grid[0])):
        if len([line[c] for line in grid if line[c] == "#"]) == 0:
            expanded_grid = [
                line[0 : c + offset] + ["X"] + line[c + offset :]
                for line in expanded_grid
            ]
            offset += 1

    locs = []
    count = 0
    for r in range(0, len(expanded_grid)):
        for c in range(0, len(expanded_grid[0])):
            if expanded_grid[r][c] == "#":
                expanded_grid[r][c] = count
                count += 1
                locs.append((r, c))

    if debug:
        for line in expanded_grid:
            print(" ".join([str(x) for x in line]))

    total = 0
    for a, b in itertools.combinations(range(0, count), r=2):
        a_r, a_c = locs[a]
        b_r, b_c = locs[b]
        num_expanded = 0
        for r in range(min(a_r, b_r), max(a_r, b_r)):
            if expanded_grid[r][a_c] == "X":
                num_expanded += 1
        for c in range(min(a_c, b_c), max(a_c, b_c)):
            if expanded_grid[a_r][c] == "X":
                num_expanded += 1

        total += (
            abs(a_r - b_r) + abs(a_c - b_c) + (num_expanded) * (multiplier - 2)
        )  # -1 for num_r, num_c, -1 for original empty row

    return total


if __name__ == "__main__":
    part_one()
    part_two()
