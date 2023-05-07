import random


def main():
    with open("data.txt", "w") as f:
        for i in range(100_000):
            x = random.uniform(-10000, 10000)
            f.write(str(x) + "\n")


if __name__ == "__main__":
    main()
