
# CSE 417
# HW2
# Luke Jiang (1560831)
# 22/01/2019


# This program implements a DFS search algorithm that can calculate number of vertices,
# number of edges, number of biconnected components, number of articulation points,
# and also list the articulation points and edges in each biconnected components.
# The program assumes that the input does not contain malformed graphs.
# The program assumes that there is a folder named 'data' containing the test graphs
# in the same directory of this file.




import os
import timeit

# path of folder of biconnectivity tests
PATH = "/Users/jiangyuxuan/PycharmProjects/Graph/venv/data"

class Graph:
    def __init__(self):
        self.graph = dict()             # graph as adjacency list
        self.dfsnum = dict()            # DFS number of each vertex
        self.low = dict()               # LOW value of each vertex
        self.ap = list()                # articulation points
        self.components = list()        # biconnected components
        self.vertexNum = 0              # number of vertices in the graph
        self.edgeNum = 0                # number of edges in the graph
        self.graphName = None           # name of the graph (input file name)
        self.root = "0"                 # DFS start vertex
        self.dfscounter = 0             # DFS counter
        self.runtime = 0                # runtime of DFS algorithm
        self.rootchild = 0              # number of children of the root
        self.stack = list()             # stack of edges

    def feed(self, filename):
        """
        Feed an input graph file (in .txt format). Construct the graph and initialize
        the DFS number and LOW value to -1 for all vertices. Find out the vertex number
        and edge number of the input graph.
        Assume the file 'filename' is in a folder called 'data'.
        :param filename: the name of input file.
        """
        self.graphName = filename
        self.clearStates()
        # assume the file 'filename' is in a folder called 'data'
        file = open("./data/" + filename)
        str = file.read().split()
        file.close()
        self.vertexNum = str[0]
        self.edgeNum = (len(str) - 1) / 2
        for i in range(1, len(str), 2):
            v1 = str[i]
            v2 = str[i+1]
            if v1 not in self.graph:
                ls = list()
                ls.append(v2)
                self.graph[v1] = ls
            else:
                self.graph[v1].append(v2)
            if v2 not in self.graph:
                ls = list()
                ls.append(v1)
                self.graph[v2] = ls
            else:
                self.graph[v2].append(v1)
            self.dfsnum[v1] = -1
            self.dfsnum[v2] = -1
            self.low[v1] = -1
            self.low[v2] = -1

    def clearStates(self):
        """
        Clear all information relevant to the graph and its DFS state.
        """
        self.graph.clear()
        self.dfsnum.clear()
        self.low.clear()
        self.ap[:] = []
        self.components[:] = []
        self.root = "0"
        self.dfscounter = 0
        self.runtime = 0
        self.rootchild = 0
        self.stack[:] = []

    def dfs(self):
        """
        Call dfs_helper() on the root node, find run time of the algorithm.

        """
        # start the timer
        start = timeit.default_timer()
        self.dfs_helper(self.root)
        # pop additional edges
        if len(self.stack) > 0:
            res = list()
            while len(self.stack) > 0:
                nxt = self.stack.pop()
                res.append(nxt)
            self.components.append(res)
        # check if root node is an AP
        if self.rootchild >= 2:
            self.ap.append(self.root)
        # end the timer and save the runtime
        end = timeit.default_timer()
        self.runtime = end - start

    def dfs_helper(self, v, p=None):
        """
        Recursive method for DFS implementation.

        """
        self.dfscounter += 1
        self.dfsnum[v] = self.dfscounter
        self.low[v] = self.dfscounter
        for w in self.graph[v]:
            if self.dfsnum[w] == -1:
                self.addEdge(v, w)
                self.dfs_helper(w, v)
                if v == self.root:
                    self.rootchild += 1
                wLow = self.low[w]
                self.low[v] = min(self.low[v], wLow)
                if wLow >= self.dfsnum[v]:
                    if v not in self.ap and v != self.root:
                        self.ap.append(v)
                    self.components.append(self.removeEdge(v, w))
            elif p is not None and w != p:
                self.addEdge(v, w)
                self.low[v] = min(self.low[v], self.dfsnum[w])

    def edge(self, v, w):
        """
        Return an edge represented by a tuple of vertices v, w in ascending order.

        """
        if int(v) < int(w):
            return v, w
        else:
            return w, v

    def addEdge(self, v, w):
        """
        Add edge (v, w) to self.stack and mark it as discovered.
        """
        vw = self.edge(v, w)
        if self.dfsnum[v] > self.dfsnum[w]:
            self.stack.append(vw)

    def removeEdge(self, v, w):
        """
        Remove edge (v, w) from self.stack.
        :param v, w: two vertices of the edge (order doesn't matter).
        :return: a list of edges popped from self.stack until (v, w) is popped.
        """
        vw = self.edge(v, w)
        res = list()
        while len(self.stack) > 0:
            nxt = self.stack.pop()
            res.append(nxt)
            if nxt == vw:
                break
        return res

    def report(self):
        """
        Print out results of DFS.
        """
        print "graph: " + self.graphName
        print "number of vertices: " + str(self.vertexNum)
        print "number of edges: " + str(self.edgeNum)
        print "number of articulation points: " + str(len(self.ap))
        print "articulation points: " + str(self.ap)
        print "number of biconnected components: " + str(len(self.components))
        print "components: " + str(self.components)
        print "time: " + str(self.runtime)
        print "============================================================="

    def report_txt(self):
        """
        Generate runtime data (as a string) for each input graph.
        :return: vertex number, edge number and runtume separated by tabs.
        """
        return str(self.vertexNum) + '\t' + str(self.edgeNum) + '\t' + str(self.runtime) + '\n'

    def feed_batch(self, dst):
        """
        Append output data generated in format specified in report_txt to dst.
        create dst if dst does not exist.
        :param dst: name of the .txt file for appending output data.
        """
        f = open(dst, "a+")
        for eachfile in os.listdir(PATH):
            print eachfile
            if eachfile.endswith(".txt"):
                self.feed(eachfile)
                self.dfs()
                f.write(g.report_txt())
        f.close()


if __name__ == '__main__':
    g = Graph()
    # feed test folder whose location is specified by PATH
    g.feed_batch("result_tmp2.txt")

    # feed individual file
    #g.feed("n16d3s17.txt")
    #g.dfs()
    #g.report()

