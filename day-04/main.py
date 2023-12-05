from pathlib import Path

filename = "input"


if __name__ == "__main__":
    # Part 1
    total = 0
    with open(Path(__file__).parent / filename) as file:
        for line in file:
            numbers = line.strip().split(":")[1]
            winners, my_numbers = [
                [int(number) for number in group.split()]
                for group in numbers.split("|")
            ]
            total += int(2 ** (len([x for x in my_numbers if x in winners]) - 1))

    print("Part 1:")
    print(total)

    # Part 2
    num_winners = []  # number of winners for each card
    with open(Path(__file__).parent / filename) as file:
        # Calculate winning numbers for each card
        for line in file:
            numbers = line.strip().split(":")[1]
            winners, my_numbers = [
                [int(number) for number in group.split()]
                for group in numbers.split("|")
            ]
            num_winners.append(len([x for x in my_numbers if x in winners]))

    # Calculate num copies
    copies = [1] * len(num_winners)
    for i, winners in enumerate(num_winners):
        # Add a copy of the next X cards for each copy of this card
        for count in range(0, winners):
            copies[i + count + 1] += copies[i]

    print("Part 2:")
    print(sum(copies))
