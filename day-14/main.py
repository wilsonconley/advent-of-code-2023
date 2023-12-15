from pathlib import Path


filename = "input"


def part_one() -> None:
    total = 0
    with open(Path(__file__).parent / filename) as file:
        grid_t = [list(line) for line in zip(*file.readlines())][:-1]

    # move O in each row from right to left
    for line in grid_t:
        o_idx = [i for i, x in enumerate(line) if x == "O"]
        sq_idx = [i for i, x in enumerate(line) if x == "#"]
        rolled_idx = []
        for o in o_idx:
            stop = [sq for sq in sq_idx if sq < o]
            if stop:
                rolled = stop[-1] + 1
            else:
                rolled = 0
            while rolled in rolled_idx:
                rolled += 1
            rolled_idx.append(rolled)
        total += sum([(len(line) - i) for i in rolled_idx])

    print("Part 1:")
    print(total)


def transpose(grid: list[list[str]]) -> list[list[str]]:
    return [list(line) for line in zip(*grid)]


def rotate(grid: list[list[str]]) -> list[list[str]]:
    return [list(line) for line in list(zip(*reversed(grid)))]


def cycle_grid(grid: list[list[str]]) -> list[list[str]]:
    # rotate N, W, S, E for a full cycle
    for _ in range(0, 4):
        # get transposed version of grid (for easy roll calculation)
        grid_t = transpose(grid)

        # roll, moving all O in each row from right to left
        for row_idx in range(0, len(grid_t)):
            o_idx = [i for i, x in enumerate(grid_t[row_idx]) if x == "O"]
            sq_idx = [i for i, x in enumerate(grid_t[row_idx]) if x == "#"]
            rolled_idx = []
            for o in o_idx:
                # find stop point
                stop = [sq for sq in sq_idx if sq < o]
                if stop:
                    rolled = stop[-1] + 1
                else:
                    rolled = 0
                while rolled in rolled_idx:
                    rolled += 1
                rolled_idx.append(rolled)

                grid_t[row_idx][o] = "."  # stone is no longer in original location

            # update grid with new locations after rolled
            for rolled in rolled_idx:
                grid_t[row_idx][rolled] = "O"

        # rotate grid clockwise
        grid = transpose(grid_t)  # transpose back
        grid = rotate(grid)  # rotate 90 deg clockwise

    return grid


def calculate_load(grid: list[list[str]]) -> int:
    return sum([(len(grid) - i) * row.count("O") for i, row in enumerate(grid)])


def part_two() -> None:
    num_cycles = 1000000000

    # Read original grid
    with open(Path(__file__).parent / filename) as file:
        grid = [list(line.strip()) for line in file.readlines()]

    all_grids = []
    all_loads = []
    repeat_cycle = None
    for cycle in range(0, num_cycles):
        # Save load total for this grid
        all_loads.append(calculate_load(grid))

        # Save grid to check for repeats
        if grid not in all_grids:
            all_grids.append(grid)
        else:
            # Repeat found! We can stop now...
            repeat_cycle = cycle
            break

        # Cycle the grid
        grid = cycle_grid(grid)

    # If we didn't find a repeat, then our algorithm didn't work...
    if repeat_cycle is None:
        raise ValueError("Repeat pattern not found!")

    # Calculate which repeated grid we end on
    repeat_loads = all_loads[
        all_grids.index(grid) : -1
    ]  # get loads for the repeated grids
    repeat_length = len(repeat_loads)  # get number of grids in repeated pattern
    repeat_offset = (
        repeat_cycle - repeat_length
    )  # offset from start of cycles to the start of repeats (repeats don't start at 0)
    final_idx = (num_cycles - repeat_offset) % repeat_length

    print("Part 2:")
    print(repeat_loads[final_idx])


if __name__ == "__main__":
    part_one()
    part_two()
