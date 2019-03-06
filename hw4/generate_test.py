# CSE 417
# HW4
# Luke Jiang
# 8/2/2019

# This program generates two types of input points:
# 1. points are uniformly distributed over unit square
# 2. points are uniformly distributed on line (0.0, 1.0)


import numpy as np


def uniform(filename, n):
    f = open(filename, "a")
    for _ in range(n):
        x = np.random.uniform(0.0, 1.0)
        y = np.random.uniform(0.0, 1.0)
        s = str(x) + ' ' + str(y) + '\n'
        f.write(s)
    f.close()

def lineseg(filename, n):
    f = open(filename, "a")
    for _ in range(n):
        y = np.random.uniform(0.0, 1.0)
        s = "0.0  " + str(y) + '\n'
        f.write(s)
    f.close()


if __name__ == "__main__":
    #uniform("test_grad.txt", 20)
    lineseg("test_line.txt", 50000)
