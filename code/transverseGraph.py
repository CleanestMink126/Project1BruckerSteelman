import random
import networkx as nx
import math
import numpy as np
import buildNetwork
import matplotlib.pyplot as plt
import time


attributes = ['pos','weight','defector','theta','k']
class graphCrawler:

    def __init__(self,G,b,posDict=None,weightDict = None,defectorDict = None):
        self.G = G #the graph
        self.b = b #the payoff
        self.k = 1 #a randomness factor
        self.posDict = posDict #dictionary of positions
        self.weightDict = weightDict #initialized weights
        self.defectorDict = defectorDict #initialized defection
        self.thetas_dict = nx.get_node_attributes(G, name ='theta')
        self.r_dict = nx.get_node_attributes(G, name ='r')
        if weightDict is None:
            self.weightDict = dict.fromkeys(G.nodes(),0)
        if defectorDict is None:
            self.defectorDict = nx.get_node_attributes(self.G, name ='defector')
        if posDict is None:
            self.posDict = nx.get_node_attributes(self.G, name ='pos')

        # print(self.weightDict)
        nx.set_node_attributes(self.G, name ='weight',values = self.weightDict)
        # nx.set_node_attributes(self.G, 'defector',self.defectorDict)


    def findDistance(self,node, target):#simple function to find disance between nodes
        thetaN = self.thetas_dict[node]
        thetaT = self.thetas_dict[target]
        # print('Theta'+  str(thetaN))
        delta = math.pi - abs(math.pi - abs(thetaN - thetaT))
        rN = self.r_dict[node]
        rT = self.r_dict[target]
        try:
            dist = rN + rT + 2 * math.log(delta/2)
        except:
            dist = None
        return dist

    def findClosestNode(self, node, target):
        allNeighbors = list(self.G[node].keys())#get all neighbors of the node
        # allNeighbors = allNeighbors.copy()
        # print(allNeighbors)
        if not (allNeighbors):
            return node
        dist = None
        closeNode = allNeighbors.pop()#get last value and set to closest
        # print(closeNode)
        minDist = self.findDistance(closeNode,target)#set last value distance to min
        for i in allNeighbors:#loop to check distance of all neighbors
            dist = self.findDistance(i,target)
            if (minDist is None) or (dist is not None and dist < minDist):
                misDist = dist
                closeNode = i
        return closeNode#return closest

    def getPath(self, node, target, seen=None):#get closest each time
        if seen is None:
            seen = set()
        if self.defectorDict[node] == 1 or node in seen:
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
        nx.set_node_attributes(self.G, name = 'weight',values=weightDict)

    def updateConversion(self):
        weightDict = nx.get_node_attributes(self.G, 'weight')
        defectorDict = nx.get_node_attributes(self.G, 'defector')

        for node in self.G.nodes():

            allNeighbors = list(self.G[node].keys())#get all neighbors of the node
            # allNeighbors = allNeighbors.copy()
            # allNeighbors.pop()
            # assert len(allNeighbors) != len(list(self.G[node].keys()))
            # print(allNeighbors)
            if allNeighbors:
                closeNode =random.choice(allNeighbors)#get last value and set to closest
                # print(node)
                # print(closeNode)
                weightj = weightDict[closeNode]
                weighti = weightDict[node]
                # print(weighti)
                # print(weightj)
                try:
                    expVal = math.exp((weighti-weightj)/self.k)
                    # print(expVal)
                    probabilityChange = 1 / (1 + expVal)
                                             #calculate proability that the original node will copy its neighbor
                    changeBool = random.random() < probabilityChange#make decision based on probability
                    if changeBool:
                        self.defectorDict[node] = defectorDict[closeNode]#store difference in defectorness in another array
                except:
                    continue

        nx.set_node_attributes(self.G,name = 'weight',values = self.weightDict)
        nx.set_node_attributes(self.G, name ='defector',values = self.defectorDict)



    def iterate(self, numTimes):
        allNodes = self.G.nodes()
        for i in range(numTimes):
            for i in range(nx.number_of_nodes(self.G)):
                # print('PATH-------')
                nodeList = random.sample(allNodes, 2)
                node1 = nodeList[0]
                node2 = nodeList[1]
                path = self.getPath(node1,node2)
                print(node1)
                print(node2)
                print(path)
                if path[-1] == node2:
                    print('Success!')
                    self.updateWeights(path,1)
                else:
                    print('FAIl!')
                    self.updateWeights(path,0)
            # print('UPDATING-------')
            self.updateConversion()

    def get_defector_state(self):
        defectors = nx.get_node_attributes(self.G, 'defector')
        d_list = list(defectors.values())
        return sum(d_list)/len(d_list)


def make_punchline(n=1000, gamma=2.5, temp=0.4, mean_deg=6, d=5,avg = 10):
    now = time.time()
    out_vals = np.zeros((d,d))
    C0_vals = np.linspace(0,0.8,d)
    '''I did a hacky fix here, the paper specified C as
    the rate of good boyos but we defined it as defectors so I just do 1 - C'''
    b_vals = np.linspace(5,25,d)
    for i, C0 in enumerate(C0_vals):
        for j, b in enumerate(b_vals):
            graph = buildNetwork.build_synthetic_network(n = n, gamma = gamma, temp = temp, mean_deg = mean_deg, C = C0)
            myCrawler = graphCrawler(graph, b)
            myCrawler.iterate(10)
            states = np.zeros(avg)
            print('INIT')
            for k in range(avg):
                myCrawler.iterate(1)
                states[k] = myCrawler.get_defector_state()
            out_vals[i,j] = np.mean(states) # Record the output state of the system
    times = time.time() - now
    print(times)
    nO = 10000
    avg0 = 250
    iterations = 50
    qual= 20 * 60
    mult = (nO / n) * (avg0 / avg) * (iterations) * (qual / (d**2))
    print('MULT' + str(mult))
    print(out_vals)
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(out_vals, cmap=plt.cm.YlOrRd, alpha=0.8)
    ax.set_xticklabels(b_vals, minor=False)
    ax.set_yticklabels(C0_vals, minor=False)
    plt.show()


if __name__ == '__main__':
    # n = 100
    # gamma = 2.5
    # temp = 0.4
    # meanDeg = 15
    # c = .5
    # graph = buildNetwork.build_synthetic_network(n = n, gamma = gamma, temp = temp, mean_deg = meanDeg, C = c)
    # myCrawler = graphCrawler(graph, 10)
    # buildNetwork.draw_net(myCrawler.G)
    # myCrawler.iterate(100)
    # print('Defector state', myCrawler.get_defector_state())
    # buildNetwork.draw_net(myCrawler.G)

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
