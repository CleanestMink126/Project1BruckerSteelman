import random
import networkx as nx
import math

class graphCrawler:
    def __init__(self,G,b,posDict,weightDict = None,defectorDict = None):
        self.G = G #the graph
        self.b = b #the payoff
        self.k = 1 #a randomness factor
        self.posDict = posDict #dictionary of positions
        self.weightDict = weightDict #initialized weights
        self.defectorDict = defectorDict #initialized defection
        if weightDict is None:
            self.weightDict = dict.fromkeys(G.nodes(),[0]*number_of_nodes(G))
        if defectorDict is None:
            self.defectorDict = dict.fromkeys(G.nodes(),[0]*number_of_nodes(G))
        for i in G.nodes():
            self.G[i]['weight'] = self.weightDict[i] #put all values inside the graph
            self.G[i]['defector'] = self.defectorDict[i]
            self.G[i]['pos'] = self.posDict[i]

    def findDistance(self,node, target):#simple function to find disance between nodes
        posN = self.G[node]['pos']#//TODO
        posT = self.G[target]['pos']
        return math.sqrt((posN[0]-posT[0])**2 + (posN[1]-posT[1])**2)

    def findClosestNode(self, node, target):
        allNeighbors = self.G[node]#get all neighbors of the node
        allNeighbors = allNeighbors.copy()
        closeNode = allNeighbors.popitem()[0]#get last value and set to closest
        minDist = self.findDistance(closeNode,target)#set last value distance to min
        for i,v in allNeighbors.items():#loop to check distance of all neighbors
            dist = findDistance(self,i,target)
            if dist < minDist:
                misDist = dist
                closeNode = i
        return closeNode#return closest

    def getPath(self, node, target):#get closest each time
        if self.G[node]['defector'] == 1:
            return [node]
        nextnode = findClosestNode(self, node, target)
        if nextnode == target:
            return [node] + [nextnode]
        return [node] + getPath(self, nextnode, target)


    def updateWeights(self,nodeList,delieveredBool):
        lastNode = nodeList[-1]
        reverseList = nodeList[::-1]
        for i,l in enumerate(reverseList):
            self.G[i]['weight'] = self.G[i]['weight']+ delieveredBool*(self.b/len(reverseList)) - 1

    def updateConversion(self):
        for node in G.nodes():
            allNeighbors = self.G[node]#get all neighbors of the node
            closeNode = random.choice(allNeighbors.keys())#random node
            probabilityChange = 1 / (1 + math.exp((self.G[node]['weight']-self.G[closenode]['weight'])/self.k)
                                     #calculate proability that the original node will copy its neighbor
            changeBool = random.random() < probabilityChange#make decision based on probability
            if changeBool:
                self.defectorDict[node] = self.G[closenode]['defector']#store difference in defectorness in another array
        for node in G.nodes():#update and reset weights
            self.G[i]['weight'] = self.weightDict[i]
            self.G[i]['defector'] = self.defectorDict[i]

pos = dict(Albany=(-74, 43),
          Boston=(-71, 42),
          NYC=(-74, 41),
          Philly=(-75, 40))
pos['Albany']
G = nx.Graph()
G.add_nodes_from(pos)
G.nodes()
drive_times = {('Albany', 'Boston'): 3,
               ('Albany', 'NYC'): 4,
               ('Boston', 'NYC'): 4,
               ('NYC', 'Philly'): 2}
G.add_edges_from(drive_times)
G.edges()
print(findClosestNode(G,'Albany','Philly',pos))
print(getPath(G,'Albany','Philly',pos))
# nx.draw(G, pos,
#         node_color=COLORS[1],
#         node_shape='s',
#         node_size=2500,
#         with_labels=True)
#
# nx.draw_networkx_edge_labels(G, pos,
#                              edge_labels=drive_times)
#
