
# CSE 417
# HW2
# Luke Jiang (1560831)
# 22/01/2019

# plot the result 

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


f = open("result_temp.txt", "r")
data = [[float(i) for i in line.split()] for line in f]

# data = [[i[1] + i[0], i[2]] for i in data]
data = np.array(data)
#data.sort(axis=0)
print data
vertices = data[:,0]
edges = data[:,1]
time = data[:,2]

x = edges

slope, intercept, r_value, p_value, std_err = stats.mstats.linregress(x, time)

line = x * slope + intercept

plt.plot(x, time, 'o', x, line)
ax = plt.gca()
fig = plt.gcf()
plt.show()
