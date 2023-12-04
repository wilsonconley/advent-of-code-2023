import re
from pathlib import Path


filename = "input"

if __name__ == "__main__":
    # Part 1
    calibration_sum = 0
    with open(Path(__file__).parent / filename) as file:
        for line in file:
            digits = re.findall("\d", line)
            calibration_sum += int(digits[0] + digits[-1])
    print("Part 1:")
    print(calibration_sum)

    # Part 2
    digits_str = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    calibration_sum = 0
    with open(Path(__file__).parent / filename) as file:
        for line in file:
            digits = [
                m.groups()[0]
                for m in re.finditer(
                    "(?=(" + "|".join(digits_str) + "|\d))", line, flags=re.IGNORECASE
                )
            ]
            calibration_sum += int(
                (
                    str(digits_str.index(digits[0]) + 1)
                    if digits[0] in digits_str
                    else digits[0]
                )
                + (
                    str(digits_str.index(digits[-1]) + 1)
                    if digits[-1] in digits_str
                    else digits[-1]
                )
            )
    print("Part 2:")
    print(calibration_sum)
