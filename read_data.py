import matplotlib.pyplot as plt
import numpy as np
import re

# Configuration
FILE = "data.txt"
VISUALIZE = True


def read_file_coefficients() -> np.ndarray:
    """Read all lines in file and store I,J,Z into buffer"""
    buffer = []
    with open(FILE, "r") as f:
        while line := f.readline():
            i = re.findall(r"I(\d+)", line)[0]
            j = re.findall(r"J(\d+)", line)[0]
            z = re.findall(r"Z(\d+\.\d+)", line)[0]

            buffer.append([int(i), int(j), float(z)])

    # format buffer as 2d array
    x_max, y_max = np.max([[x[0], x[1]] for x in buffer], axis=0)
    np_buffer = np.zeros((x_max + 1, y_max + 1))

    # copy buffer to numpy array
    for (x, y, z) in buffer:
        np_buffer[x, y] = z
    return np_buffer


def print_table(np_coefficient: np.ndarray) -> None:
    """Print table in terminal"""
    x_max, y_max = np_coefficient.shape
    print("------ Coefficient from file [um]: ------")

    # print header
    print(" " * 5, end="")
    for y in range(y_max):
        end = " | " if y != y_max - 1 else ""
        print(f"   {y}     ", end=end)
    print()

    # print body
    for x in range(x_max):
        for y in range(y_max):
            end = " | " if y != y_max - 1 else ""
            number = np_coefficient[x, y] * 1000
            header = f"{x}    " if y == 0 else ""
            spacer = " " * (4 - int(np.log10(number)))
            print(header + spacer + f"{ number: .2f}", end=end)
        print()


def plot_data(z_data: np.ndarray) -> None:
    """Plots coefficient data"""

    # plot mean
    plt.subplot(311)
    projection_x = np.mean(z_data, axis=0)
    projection_y = np.mean(z_data, axis=1)

    plt.plot(projection_x, label="mean horizontal")
    plt.plot(projection_y, label="mean vertical")
    plt.legend()

    # plot variance
    plt.subplot(312)
    projection_x = np.var(z_data, axis=0)
    projection_y = np.var(z_data, axis=1)

    plt.plot(projection_x, label="var horizontal")
    plt.plot(projection_y, label="var vertical")
    plt.legend()

    # plot legend
    plt.subplot(313)
    plt.imshow(z_data)

    plt.show()


def main() -> None:
    """Main function, print coefficients"""
    coefficients = read_file_coefficients()
    print_table(coefficients)

    # Projection in x,y axis
    mean_x = np.mean(coefficients, axis=0)
    mean_y = np.mean(coefficients, axis=1)

    std_x = np.std(coefficients, axis=0)
    std_y = np.std(coefficients, axis=1)

    print(f"Mean average value X: {mean_x.mean(): .3f} Y: {mean_y.mean():.3f}")
    print(f"Mean STD value X: {std_x.mean(): .3f} Y: {std_y.mean():.3f}")

    if VISUALIZE:
        plot_data(coefficients)


if __name__ == "__main__":
    main()
