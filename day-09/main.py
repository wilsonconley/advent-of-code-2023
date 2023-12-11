from pathlib import Path

filename = "input"


def part_one() -> None:
    with open(Path(__file__).parent / filename) as file:
        total = 0
        for line in file:
            history = [[int(x) for x in line.split()]]
            diff = [
                history[0][i + 1] - history[0][i] for i in range(len(history[0]) - 1)
            ]
            while set(diff) != {0}:
                history.append(diff)
                diff = [
                    history[-1][i + 1] - history[-1][i]
                    for i in range(len(history[-1]) - 1)
                ]
            history.append(diff)

            for i in range(len(history) - 2, -1, -1):
                history[i].append(history[i + 1][-1] + history[i][-1])

            total += history[0][-1]

    print("Part 1:")
    print(total)


def part_two() -> None:
    with open(Path(__file__).parent / filename) as file:
        total = 0
        for line in file:
            history = [[int(x) for x in line.split()]]
            diff = [
                history[0][i + 1] - history[0][i] for i in range(len(history[0]) - 1)
            ]
            while set(diff) != {0}:
                history.append(diff)
                diff = [
                    history[-1][i + 1] - history[-1][i]
                    for i in range(len(history[-1]) - 1)
                ]
            history.append(diff)

            for i in range(len(history) - 2, -1, -1):
                history[i].insert(0, history[i][0] - history[i + 1][0])

            total += history[0][0]

    print("Part 2:")
    print(total)


if __name__ == "__main__":
    part_one()
    part_two()
