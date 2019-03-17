import numpy as np
import timeit


# use slides convention for OPT table

class Finder:

    def __init__(self):
        self.string = None          # input RNA sequence
        self.len = 0                # length of input sequence
        self.OPT = None             # OPT table
        self.trace = None           # traceback string

    def feed(self, string):
        self.checkstring(string)
        self.string = string
        self.len = len(string)
        self.OPT = [[0 for x in range(self.len)] for y in range(self.len)]
        self.trace = list("." * self.len)

    def nussinov(self):
        for j in range(1, self.len + 1):
            for i in range(j, 0, -1):
                if i < j - 4:
                    maximum = self.getOPT(i, j-1)
                    for t in range(i, j-4):
                        if self.match(t, j):
                            maximum = max(maximum, self.getOPT(i, t-1) + self.getOPT(t+1, j-1) + 1)
                    self.setOPT(i, j, maximum)

    def traceback(self):
        self.tracebackHelper(1, self.len)
        # print "".join(self.trace)

    def tracebackHelper(self, i, j):
        """
        Main traceback algorithm.
        """
        if i >= j - 4:
            return
        if self.getOPT(i, j) == self.getOPT(i, j-1):
            self.tracebackHelper(i, j-1)
        else:
            n = i
            for t in range(i, j-4):
                # Always return the last matching pair
                opt = self.getOPT(i, t-1) + self.getOPT(t+1, j-1) + 1
                if self.match(t, j) and self.getOPT(i, j) == opt:
                    n = t
            self.trace[n-1] = '('
            self.trace[j-1] = ')'
            self.tracebackHelper(i, n-1)
            self.tracebackHelper(n+1, j-1)

    def match(self, i, j):
        """
        check if char at (i-1) and at (j-1) form a Watson-Crick pair
        """
        x = self.string[i-1]
        y = self.string[j-1]
        if x == 'A':
            return y == 'U'
        elif x == 'C':
            return y == 'G'
        elif x == 'G':
            return y == 'C'
        else:
            return y == 'A'

    def checkstring(self, string):
        """
        Check if input string contains characters beside "ACGU".
        Raise exception if found illegal characters.
        """
        for s in string:
            if s not in "ACGU":
                raise Exception("input contains illegal character")

    def getOPT(self, i, j):
        return self.OPT[i-1][j-1]

    def setOPT(self, i, j, val):
        self.OPT[i-1][j-1] = val

    def printOPT(self):
        print np.matrix(self.OPT)

    def oneshot(self, output=True):
        """
        Run Nussinov's and traceback algorithm on self.string
        :param output:
        """
        t_start = timeit.default_timer()
        f.nussinov()
        f.traceback()
        t_end = timeit.default_timer()
        if output:
            print self.string
            print "".join(self.trace)
            print "Length = " + str(self.len) + ", Pairs = " + str(self.getOPT(1, self.len)) + \
                  ", Time = " + str(t_end - t_start) + " sec"
            if self.len <= 25:
                self.printOPT()
            print ""
        else:
            print str(t_end - t_start)

    def generate(self, length):
        """
        Generate a random sequence using uniform distribution
        :param length: length of the generated sequence
        """
        res = ""
        for _ in range(length):
            r = np.random.uniform(0.0, 1.0)
            if r <= 0.25:
                res += "A"
            elif r <= 0.5:
                res += "C"
            elif r <= 0.75:
                res += "G"
            else:
                res += "U"
        return res

    def execute(self, filename, random=False):
        """
        Run Nussinov's and traceback algorithm on each line in input file
        :param filename: filename of input .txt file
        :param random: optionally run automatically generated sequences. Default is False
        """
        f = open(filename, "r")
        strings = f.read().split()
        for s in strings:
            self.feed(s)
            self.oneshot()
        if random:
            for k in range(4, 13):
                s = self.generate(2 ** k)
                self.feed(s)
                self.oneshot(output=False)






if __name__ == '__main__':
    f = Finder()
    f.execute("test.txt", random=False)  # change random to True for stress test
