import random
import networkx as nx
import math
from buildNetwork import build_network


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
        for i in G.nodes():
            self.G[i]['weight'] = self.weightDict[i] #put all values inside the graph
            self.G[i]['defector'] = self.defectorDict[i]
            if posDict is not None:
                self.G[i]['pos'] = self.posDict[i]

    def findDistance(self,node, target):#simple function to find disance between nodes
        posN = self.G[node]['pos']#//TODO
        posT = self.G[target]['pos']
        return math.sqrt((posN[0]-posT[0])**2 + (posN[1]-posT[1])**2)

    def findClosestNode(self, node, target):
        allNeighbors = self.G.neighbors(node)#get all neighbors of the node
        allNeighbors = allNeighbors.copy()
        print(nx.get_node_attributes(self.G, 'pos'))
        # print(allNeighbors)
        closeNode = allNeighbors.pop()#get last value and set to closest
        while closeNode in attributes:
            closeNode = allNeighbors.pop()
        print(self.G[closeNode])
        minDist = self.findDistance(closeNode,target)#set last value distance to min
        for i in allNeighbors:#loop to check distance of all neighbors
            if i not in attributes:
                dist = self.findDistance(i,target)
                if dist < minDist:
                    misDist = dist
                    closeNode = i
        return closeNode#return closest

    def getPath(self, node, target, seen=set()):#get closest each time
        if self.G[node]['defector'] == 1 or node in seen:
            return [node]
        nextnode = self.findClosestNode(node, target)
        if nextnode == target:
            return [node] + [nextnode]
        print(node)
        seen.add(node)
        return [node] + self.getPath(nextnode, target, seen=seen)


    def updateWeights(self,nodeList,delieveredBool):
        lastNode = nodeList[-1]
        reverseList = nodeList[::-1]
        for i,l in enumerate(reverseList):
            self.G[i]['weight'] = self.G[i]['weight']+ delieveredBool*(self.b/len(reverseList)) - 1

    def updateConversion(self):
        for node in G.nodes():
            allNeighbors = self.G.neighbors(node)#get all neighbors of the node
            allNeighbors = allNeighbors.copy()
            # print(allNeighbors)
            closeNode =random.choice(allNeighbors)#get last value and set to closest
            while closeNode in attributes:
                closeNode = random.choice(allNeighbors)
            weightj = self.G[closeNode]['weight']
            weighti = self.G[node]['weight']
            print(weighti)
            print(weightj)
            expVal = math.exp((weighti-weightj)/self.k)
            print(expVal)
            probabilityChange = 1 / (1 + expVal)
                                     #calculate proability that the original node will copy its neighbor
            changeBool = random.random() < probabilityChange#make decision based on probability
            if changeBool:
                self.defectorDict[node] = self.G[closeNode]['defector']#store difference in defectorness in another array
        for node in G.nodes():#update and reset weights
            self.G[i]['weight'] = self.weightDict[i]
            self.G[i]['defector'] = self.defectorDict[i]

    def iterate(self, numTimes):
        for i in range(numTimes):
            for i in range(nx.number_of_nodes(self.G)):
                nodeList = random.sample(self.G.nodes(), 2)
                node1 = nodeList[0]
                node2 = nodeList[1]
                path = self.getPath(node1,node2)
                if path[-1] == node2:
                    self.updateWeights(path,1)
                else:
                    self.updateWeights(path,0)
            self.updateConversion()

if __name__ == '__main__':
    n = 100
    gamma = 2.5
    temp = 0.4
    meanDeg = 6
    graph = build_network(n = n, gamma = gamma, temp = temp, mean_deg = meanDeg)
    myCrawler = graphCrawler(graph,5)
    myCrawler.iterate(10)
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
