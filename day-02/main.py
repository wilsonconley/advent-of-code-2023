import re
from pathlib import Path
from dataclasses import dataclass

filename = "input"


@dataclass(frozen=True)
class ColorSet:
    red: int
    green: int
    blue: int


if __name__ == "__main__":
    # Part 1
    id_sum = 0
    game_id = 1
    bag = ColorSet(red=12, green=13, blue=14)
    with open(Path(__file__).parent / filename) as file:
        for line in file:
            sets = line.split(": ")[1].split(";")
            valid = True
            for set_ in sets:
                red = re.findall("\d+(?= red)", set_)
                green = re.findall("\d+(?= green)", set_)
                blue = re.findall("\d+(?= blue)", set_)
                if (
                    (red and int(red[0]) > bag.red)
                    or (green and int(green[0]) > bag.green)
                    or (blue and int(blue[0]) > bag.blue)
                ):
                    valid = False
                    break
            if valid:
                id_sum += game_id
            game_id += 1
    print("Part 1:")
    print(id_sum)

    # Part 2
    total_power = 0
    with open(Path(__file__).parent / filename) as file:
        for line in file:
            sets = line.split(": ")[1].split(";")
            red_max = 0
            green_max = 0
            blue_max = 0
            for set_ in sets:
                red = re.findall("\d+(?= red)", set_)
                green = re.findall("\d+(?= green)", set_)
                blue = re.findall("\d+(?= blue)", set_)
                if red:
                    red_max = max(int(red[0]), red_max)
                if green:
                    green_max = max(int(green[0]), green_max)
                if blue:
                    blue_max = max(int(blue[0]), blue_max)
            power = red_max * green_max * blue_max
            total_power += power

    print("Part 2:")
    print(total_power)
