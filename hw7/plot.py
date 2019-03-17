import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

f = open("result.txt", "r")
data = [[float(i) for i in line.split()] for line in f]

data = np.array(data)

sizes = np.array([2 ** i for i in range(4, 13)])

plt.plot(sizes, data)
plt.show()