from pathlib import Path
import math

filename = "input"


def get_name(line: str) -> str:
    return line.split()[0]


def get_node(line: str) -> tuple[str, str]:
    _, _, left, right = line.split()
    return left[1:-1], right[:-1]


def part_one() -> None:
    with open(Path(__file__).parent / filename) as file:
        instructions = file.readline().strip()
        nodes = {
            get_name(line): get_node(line)
            for line in file.readlines()
            if line.strip() != ""
        }

    count = 0
    node = "AAA"
    found = False
    while not found:
        for step in instructions:
            if node == "ZZZ":
                found = True
                break
            left, right = nodes[node]
            if step == "L":
                node = left
            else:
                node = right
            count += 1

    print("Part 1:")
    print(count)


def part_two() -> None:
    with open(Path(__file__).parent / filename) as file:
        instructions = file.readline().strip()
        nodes = {
            get_name(line): get_node(line)
            for line in file.readlines()
            if line.strip() != ""
        }

    starting_nodes = [node for node in nodes if node.endswith("A")]

    multiples = []
    for node in starting_nodes:
        current_node = node
        count = 0
        found = False
        while not found:
            for step in instructions:
                if current_node.endswith("Z"):
                    multiples.append(count)
                    found = True
                    break

                left, right = nodes[current_node]
                if step == "L":
                    current_node = left
                else:
                    current_node = right

                if current_node == node:
                    break

                count += 1

    print("Part 2:")
    print(math.lcm(*multiples))


if __name__ == "__main__":
    part_one()
    part_two()
