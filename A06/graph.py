from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


DATA_FILE = Path(__file__).with_name("graph.csv")
OUTPUT_FILE = Path(__file__).with_name("graph.png")


def main():
    data = np.genfromtxt(DATA_FILE, delimiter=",", names=True)
    x = data["x"]
    y = data["y"]

    plt.plot(x, y, marker="o", label="y = 2x")
    plt.title("Linear relationship: y = 2x")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=150)
    plt.close()
    print("Graph saved to {}".format(OUTPUT_FILE))


if __name__ == "__main__":
    main()
