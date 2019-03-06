# CSE 417
# HW4
# Luke Jiang
# 8/2/2019

# plot stress test result.

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

f = open("result_small.txt", "r")
data = [[float(i) for i in line.split()] for line in f]

data = np.array(data)

points = data[:,0]
#m1 = data[:,1]
m2 = data[:,1]
m3 = data[:,2]

#plt.plot(points, m1, color='blue')
plt.plot(points, m2, color='red')
plt.plot(points, m3, color='green')
plt.show()
