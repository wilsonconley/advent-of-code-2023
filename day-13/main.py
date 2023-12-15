from pathlib import Path


filename = "input"


def check_rows(pattern: list[list[str]]) -> int:
    num_rows = len(pattern)
    found = False
    r = 0
    for r in range(1, num_rows):
        num_check = min(r, num_rows - r)
        top = pattern[r - num_check : r]
        bottom = pattern[r : r + num_check]
        bottom.reverse()
        if top == bottom:
            found = True
            break
    if not found:
        r = 0
    return r


def check_cols(pattern: list[list[str]]) -> int:
    num_cols = len(pattern[0])
    found = False
    c = 0
    for c in range(1, num_cols):
        num_check = min(c, num_cols - c)
        left = [row[c - num_check : c] for row in pattern]
        right = [row[c : c + num_check] for row in pattern]
        for i in range(0, len(right)):
            right[i].reverse()
        if left == right:
            found = True
            break
    if not found:
        c = 0
    return c


def check_pattern(pattern: list[list[str]]) -> int:
    # check row
    reflecting_row = check_rows(pattern)
    if reflecting_row:
        return 100 * reflecting_row

    # check column
    reflecting_col = check_cols(pattern)
    if reflecting_col:
        return reflecting_col

    raise ValueError("Neither row or column found")


def check_pattern_smudge(pattern: list[list[str]]) -> int:
    # check row
    reflecting_row = check_rows(pattern)

    # check column
    reflecting_col = check_cols(pattern)

    # check rows with smudge
    smudge_row = check_rows_smudge(pattern, reflecting_row)
    if smudge_row:
        return 100 * smudge_row

    # check columns with smudge
    smudge_col = check_cols_smudge(pattern, reflecting_col)
    if smudge_col:
        return smudge_col

    for line in pattern:
        print(line)

    raise ValueError("Neither smudge row or column found")


def check_rows_smudge(pattern: list[list[str]], exclude: int) -> int:
    num_rows = len(pattern)
    found = False
    r = 0

    for r in range(1, num_rows):
        if r == exclude:
            continue

        num_check = min(r, num_rows - r)
        top = pattern[r - num_check : r]
        bottom = pattern[r : r + num_check]
        bottom.reverse()

        num_diff = 0
        for check_r in range(0, len(top)):
            for check_c in range(0, len(top[0])):
                if top[check_r][check_c] != bottom[check_r][check_c]:
                    num_diff += 1
                if num_diff > 1:
                    break
            if num_diff > 1:
                break

        if num_diff == 1:
            found = True
            break
    if not found:
        r = 0
    return r


def check_cols_smudge(pattern: list[list[str]], exclude: int) -> int:
    num_cols = len(pattern[0])
    found = False
    c = 0

    for c in range(1, num_cols):
        if c == exclude:
            continue

        num_check = min(c, num_cols - c)
        left = [row[c - num_check : c] for row in pattern]
        right = [row[c : c + num_check] for row in pattern]
        for i in range(0, len(right)):
            right[i].reverse()

        num_diff = 0
        for check_r in range(0, len(left)):
            for check_c in range(0, len(left[0])):
                if left[check_r][check_c] != right[check_r][check_c]:
                    num_diff += 1
                if num_diff > 1:
                    break
            if num_diff > 1:
                break

        if num_diff == 1:
            found = True
            break
    if not found:
        c = 0
    return c


def part_one() -> None:
    total = 0
    pattern: list[list[str]] = []
    with open(Path(__file__).parent / filename) as file:
        for line in file:
            if line.strip() != "":
                pattern.append(list(line.strip()))
            else:
                total += check_pattern(pattern)
                pattern = []
    if pattern:
        total += check_pattern(pattern)

    print("Part 1:")
    print(total)


def part_two() -> None:
    total = 0
    pattern: list[list[str]] = []
    with open(Path(__file__).parent / filename) as file:
        for line in file:
            if line.strip() != "":
                pattern.append(list(line.strip()))
            else:
                total += check_pattern_smudge(pattern)
                pattern = []
    if pattern:
        total += check_pattern_smudge(pattern)

    print("Part 2:")
    print(total)


if __name__ == "__main__":
    part_one()
    part_two()
