from pathlib import Path

from tqdm import tqdm

filename = "input"


def part_one():
    with open(Path(__file__).parent / filename) as file:
        times_str, distances_str = file.readlines()

    times = [int(x) for x in times_str.split()[1:]]
    distances = [int(x) for x in distances_str.split()[1:]]

    score = 1
    for time, target_distance in zip(times, distances):

        def distance(hold_time: int) -> int:
            speed = hold_time
            return (time - hold_time) * speed

        winners = [x for x in range(0, time) if distance(x) > target_distance]
        score *= len(winners)

    print("Part 1:")
    print(score)


def part_two() -> None:
    with open(Path(__file__).parent / filename) as file:
        times_str, distances_str = file.readlines()

    time = int("".join(times_str.split()[1:]))
    target_distance = int("".join(distances_str.split()[1:]))

    def distance(hold_time: int) -> int:
        speed = hold_time
        return (time - hold_time) * speed

    winners = 0
    for x in tqdm(range(time)):
        if distance(x) > target_distance:
            winners += 1

    print("Part 2:")
    print(winners)


if __name__ == "__main__":
    part_one()
    part_two()
