import random
import networkx as nx
import math
import numpy as np
from buildNetwork import build_synthetic_network, draw_net
import matplotlib.pyplot as plt



attributes = ['pos','weight','defector','theta','k']
class graphCrawler:

    def __init__(self,G,b,posDict=None,weightDict = None,defectorDict = None):
        self.G = G #the graph
        self.b = b #the payoff
        self.k = 1 #a randomness factor
        self.posDict = posDict #dictionary of positions
        self.weightDict = weightDict #initialized weights
        self.defectorDict = defectorDict #initialized defection
        if weightDict is None:
            self.weightDict = dict.fromkeys(G.nodes(),0)
        if defectorDict is None:
            self.defectorDict = dict.fromkeys(G.nodes(),0)
        # print(self.weightDict)
        nx.set_node_attributes(self.G, 'weight',self.weightDict)
        # nx.set_node_attributes(self.G, 'defector',self.defectorDict)


    def findDistance(self,node, target):#simple function to find disance between nodes
        posDict = nx.get_node_attributes(self.G, 'pos')
        posN = posDict[node]#//TODO
        posT = posDict[target]
        return math.sqrt((posN[0]-posT[0])**2 + (posN[1]-posT[1])**2)

    def findClosestNode(self, node, target):
        allNeighbors = self.G.neighbors(node)#get all neighbors of the node
        allNeighbors = allNeighbors.copy()
        print(allNeighbors)
        if not (allNeighbors):
            return node

        closeNode = allNeighbors.pop()#get last value and set to closest
        print(closeNode)
        minDist = self.findDistance(closeNode,target)#set last value distance to min
        for i in allNeighbors:#loop to check distance of all neighbors
            dist = self.findDistance(i,target)
            if dist < minDist:
                misDist = dist
                closeNode = i
        return closeNode#return closest

    def getPath(self, node, target, seen=set()):#get closest each time
        defectDict = nx.get_node_attributes(self.G, 'defector')
        if defectDict[node] == 1 or node in seen:
            return [node]
        nextnode = self.findClosestNode(node, target)
        if nextnode == target:
            return [node] + [nextnode]
        seen.add(node)
        return [node] + self.getPath(nextnode, target, seen=seen)


    def updateWeights(self,nodeList,delieveredBool):
        lastNode = nodeList[-1]
        reverseList = nodeList[::-1]
        weightDict = nx.get_node_attributes(self.G, 'weight')
        for l,i in enumerate(reverseList):
            weightDict[i] = weightDict[i]+ delieveredBool*(self.b/len(reverseList)) - 1

    def updateConversion(self):
        weightDict = nx.get_node_attributes(self.G, 'weight')
        defectorDict = nx.get_node_attributes(self.G, 'defector')

        for node in self.G.nodes():

            allNeighbors = self.G.neighbors(node)#get all neighbors of the node
            allNeighbors = allNeighbors.copy()
            # print(allNeighbors)
            closeNode =random.choice(allNeighbors)#get last value and set to closest
            print(node)
            print(closeNode)
            weightj = weightDict[closeNode]
            weighti = weightDict[node]
            # print(weighti)
            # print(weightj)
            expVal = math.exp((weighti-weightj)/self.k)
            print(expVal)
            probabilityChange = 1 / (1 + expVal)
                                     #calculate proability that the original node will copy its neighbor
            changeBool = random.random() < probabilityChange#make decision based on probability
            if changeBool:
                self.defectorDict[node] = defectorDict[closeNode]#store difference in defectorness in another array
        for node in self.G.nodes():#update and reset weights
            weightDict[node] = self.weightDict[node]
            defectorDict[node] = self.defectorDict[node]



    def iterate(self, numTimes):
        for i in range(numTimes):
            for i in range(nx.number_of_nodes(self.G)):
                print('PATH-------')
                nodeList = random.sample(self.G.nodes(), 2)
                node1 = nodeList[0]
                node2 = nodeList[1]
                path = self.getPath(node1,node2)
                if path[-1] == node2:
                    self.updateWeights(path,1)
                else:
                    self.updateWeights(path,0)
            print('UPDATING-------')
            self.updateConversion()

    def get_defector_state(self):
        defectors = nx.get_node_attributes(self.G, 'defector')
        d_list = list(defectors.values())
        return sum(d_list)/len(d_list)


def make_punchline(n=100, gamma=2.5, temp=0.4, mean_deg=30, d=10):
    out_vals = np.zeros((d,d))
    C0_vals = np.linspace(0.2,0.8,d)
    b_vals = np.linspace(5,25,d)
    for i, C0 in enumerate(C0_vals):
        for j, b in enumerate(b_vals):
            graph = build_synthetic_network(n = n, gamma = gamma, temp = temp, mean_deg = mean_deg, C = C0)
            myCrawler = graphCrawler(graph, b)
            myCrawler.iterate(100)
            out_vals[i,j] = myCrawler.get_defector_state() # Record the output state of the system
    plt.imshow(out_vals,cmap='hot')
    plt.show()


if __name__ == '__main__':
    # n = 500
    # gamma = 2.5
    # temp = 0.4
    # meanDeg = 30
    # c = .8
    # graph = build_synthetic_network(n = n, gamma = gamma, temp = temp, mean_deg = meanDeg, C = c)
    # myCrawler = graphCrawler(graph, 5)
    # draw_net(myCrawler.G)
    # myCrawler.iterate(10)
    # print('Defector state', myCrawler.get_defector_state())
    # draw_net(myCrawler.G)

    make_punchline()

# n = 100
# k = 10
# C = .6
# G = nx.generators.random_graphs.powerlaw_cluster_graph(n, k, C, seed=None)
# posDict = {}
# for i in G.nodes():
#     posDict[i] = (random.randint(0,100),random.randint(0,100))
# # print(posDict)
# myCrawler = graphCrawler(G,10,posDict)
# myCrawler.iterate(10)
# pos = dict(Albany=(-74, 43),
#           Boston=(-71, 42),
#           NYC=(-74, 41),
#           Philly=(-75, 40))
# pos['Albany']
# G = nx.Graph()
# G.add_nodes_from(pos)
# G.nodes()
# drive_times = {('Albany', 'Boston'): 3,
#                ('Albany', 'NYC'): 4,
#                ('Boston', 'NYC'): 4,
#                ('NYC', 'Philly'): 2}
# G.add_edges_from(drive_times)
# G.edges()
# print(findClosestNode(G,'Albany','Philly',pos))
# print(getPath(G,'Albany','Philly',pos))
# nx.draw(G, pos,
#         node_color=COLORS[1],
#         node_shape='s',
#         node_size=2500,
#         with_labels=True)
#
# nx.draw_networkx_edge_labels(G, pos,
#                              edge_labels=drive_times)
#
