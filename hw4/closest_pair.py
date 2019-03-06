# CSE 417
# HW2
# Luke Jiang
# 8/2/2019

# This program implements three algorithms for finding the closest pair.
# The first algorithm is a O(n^2) naive implementation. The second one
# is the divide-and-conquer algorithm covered in the class tha has an
# O(n(logn)^2) runtime. The third one is the one discussed in the book
# (pre-sort x and y) that has an O(nlogn) runtime.

# The program reads a file that contains the coordinate of all points
# separated by spaces, and report number of points, closest pair, closest
# distance, and runtime for each method to stdout and optionally append
# the runtime to a txt file.


import math
import timeit


class ClosestPair:
    def __init__(self):
        self.points = list()
        self.pointNum = 0
        self.pointFile = None
        self.size = 0

    def feed(self, file):
        self.pointFile = file.name
        str = file.read().split()
        self.size = len(str) / 2
        for i in range(0, len(str), 2):
            self.points.append((float(str[i]), float(str[i+1])))
        self.pointNum = len(self.points)

    def method1(self):
        """
        brute-force O(n^2) algorithm
        """
        t_start = timeit.default_timer()
        d = float('inf')
        closest = None
        for i in range(0, self.pointNum):
            pi = self.points[i]
            for j in range(i+1, self.pointNum):
                pj = self.points[j]
                dst = self.dist(pi, pj)
                if dst < d:
                    d = dst
                    closest = (pi, pj)
        t_end = timeit.default_timer()
        self.report(closest, d, t_end - t_start, version="method1", oneline=True)
        return t_end - t_start

    def method2(self):
        """
        Divide-and-conquer O(n(logn)^2) algorithm
        """
        t_start = timeit.default_timer()
        # pin = sorted(self.points, key=lambda x: x[0])
        d, p = self.method2_helper(self.points)
        t_end = timeit.default_timer()
        self.report(p, d, t_end - t_start, version="method2", oneline=True)
        return t_end - t_start

    def method2_helper(self, P):
        if len(P) <= 1:
            return float('inf'), None
        P.sort(key=lambda x: x[0])

        L = P[len(P) / 2][0]
        Q = list()
        R = list()
        for point in P:
            if point[0] < L:
                Q.append(point)
            elif point[0] > L:
                R.append(point)

        d1, p1 = self.method2_helper(Q)
        d2, p2 = self.method2_helper(R)

        if d1 < d2:
            d, p = d1, p1
        else:
            d, p = d2, p2

        S = list(filter(lambda (x, y): abs(x - L) < d, P))
        S.sort(key=lambda x: x[1])

        for i in range(0, len(S)):
            pi = S[i]
            k = 1
            while i + k < len(S) and S[i+k][1] < pi[1] + d:
                d_ = self.dist(pi, S[i+k])
                if d_ < d:
                    d, p = d_, (pi, S[i+k])
                k += 1
        return d, p

    def method3(self):
        """
        Divide-and-conquer O(nlogn) algorithm (in the book)
        pre-sort x and y
        """
        t_start = timeit.default_timer()
        Px = sorted(self.points, key=lambda x: x[0])
        Py = sorted(self.points, key=lambda x: x[1])
        d, p = self.method3_helper(Px, Py)
        t_end = timeit.default_timer()
        self.report(p, d, t_end - t_start, version="method3", oneline=True)
        return t_end - t_start

    def method3_helper(self, Px, Py):
        if len(Px) <= 1:
            return float('inf'), None

        L = Px[len(Px) / 2][0]

        Qx = list()
        Rx = list()
        Qy = list()
        Ry = list()
        for point in Px:
            if point[0] < L:
                Qx.append(point)
            elif point[0] > L:
                Rx.append(point)
        for point in Py:
            if point[0] < L:
                Qy.append(point)
            elif point[0] > L:
                Ry.append(point)

        d1, p1 = self.method3_helper(Qx, Qy)
        d2, p2 = self.method3_helper(Rx, Ry)
        if d1 < d2:
            d, p = d1, p1
        else:
            d, p = d2, p2

        S = list(filter(lambda (x, y): abs(x - L) < d, Py))
        for i in range(0, len(S)):
            pi = S[i]
            k = 1
            while i + k < len(S) and S[i+k][1] < pi[1] + d:
                d_ = self.dist(pi, S[i + k])
                if d_ < d:
                    d, p = d_, (pi, S[i + k])
                k += 1
        return d, p

    def report(self, p, d, t, version, oneline=False):
        if oneline:
            print version + " " + str(self.pointNum) + " " + str(p) + " " + str(d) + " " + str(t)
        else:
            print version
            print "total number of points: " + str(self.size)
            print "the closest pair is: " + str(p)
            print "the distance is: " + str(d)
            print "total time is: " + str(t)

    def find(self, output=None, m1=True):
        """
        Iteratively calls [method1] method2 and method3, append the runtime result
        to output.
        :param output: the file to append runtime result
        :param m1: if runs method 1 or not
        """
        print "finding closest pair for file " + str(self.pointFile)
        print "=========="
        if m1:
            t1 = self.method1()
        t2 = self.method2()
        t3 = self.method3()
        if output is not None:
            if m1:
                s = str(self.pointNum) + "\t" + str(t1) + "\t" + str(t2) + "\t" + str(t3) + "\n"
            else:
                s = str(self.pointNum) + "\t" + str(t2) + "\t" + str(t3) + "\n"
            output.write(s)

    def dist(self, a, b):
        return math.sqrt(math.pow((a[0] - b[0]), 2) + math.pow((a[1] - b[1]), 2))

    def print_points(self):
        print str(self.points)


if __name__ == '__main__':
    testfile = "test2.txt"    # file for input points
    f = open(testfile, "r")
    a = ClosestPair()
    a.feed(f)
    f.close()

    # result = open("result_small.txt", "a")
    a.find(output=None, m1=True)  # does not run method 1
    # result.close()
