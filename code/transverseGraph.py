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
        thetaN = self.thetas_dict[node]#Thetas are the angles of nodes with respect to the center of the graph
        thetaT = self.thetas_dict[target]
        # print('Theta'+  str(thetaN))
        delta = math.pi - abs(math.pi - abs(thetaN - thetaT))
        rN = self.r_dict[node] #This part did not work I believe hyperbolic is two dimensional parameters
        rT = self.r_dict[target]
        try:
            dist = rN + rT + 2 * math.log(delta/2)
        except:
            dist = None

        ########################################
        #Alternative using pythagorean distance
        posN = self.posDict[node]
        posT = self.posDict[target]

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
            if i == target:
                return i
            dist = self.findDistance(i,target)
            if (minDist is None) or (dist is not None and dist < minDist):
                misDist = dist
                closeNode = i
        return closeNode#return closest

    def getPath(self, node, target, seen=None):#get closest each time
        if seen is None:#initialize the set
            seen = set()
        # print(self.findDistance(node,target))
        if self.defectorDict[node] == 1 or node in seen:#if we reach a defector or enter into a loop
            return [node]#return
        nextnode = self.findClosestNode(node, target)
        if nextnode == target:#if we reach the end, return the end
            return [node] + [nextnode]
        seen.add(node)
        return [node] + self.getPath(nextnode, target, seen=seen)


    def updateWeights(self,nodeList,delieveredBool):
        lastNode = nodeList[-1]
        reverseList = nodeList[::-1]#run through the path and update each weight according to length
        weightDict = nx.get_node_attributes(self.G, 'weight')
        for l,i in enumerate(reverseList):
            weightDict[i] = weightDict[i]+ delieveredBool*(self.b/len(reverseList)) - 1
        nx.set_node_attributes(self.G, name = 'weight',values=weightDict)

    def updateConversion(self):
        weightDict = nx.get_node_attributes(self.G, 'weight')
        defectorDict = nx.get_node_attributes(self.G, 'defector')

        for node in self.G.nodes():

            allNeighbors = list(self.G[node].keys())#get all neighbors of the node
            if allNeighbors:
                otherNode =random.choice(allNeighbors)#get last value and set to closest
                weightj = weightDict[otherNode]
                weighti = weightDict[node]
                try:
                    expVal = math.exp((weighti-weightj)/self.k)#find e value
                    # print(expVal)
                    probabilityChange = 1 / (1 + expVal)#calculate proability that the original node will copy its neighbor
                    changeBool = random.random() < probabilityChange#make decision based on probability
                    if changeBool:
                        self.defectorDict[node] = defectorDict[otherNode]#store difference in defectorness in another dict
                except:
                    continue

        nx.set_node_attributes(self.G,name = 'weight',values = self.weightDict)
        nx.set_node_attributes(self.G, name ='defector',values = self.defectorDict)



    def iterate(self, numTimes):
        allNodes = self.G.nodes()#get all the nodes
        for i in range(numTimes):#number of iterations and updates to execute
            for i in range(nx.number_of_nodes(self.G)):
                nodeList = random.sample(allNodes, 2)#get random 2 nodes
                node1 = nodeList[0]
                node2 = nodeList[1]
                path = self.getPath(node1,node2)
                # print(node1)
                # print(node2)
                # print(path)
                if path[-1] == node2:#if the last node is the target node
                    # print('Success!')
                    self.updateWeights(path,1)
                else:
                    # print('FAIl!')
                    self.updateWeights(path,0)
            # print('UPDATING-------')
            self.updateConversion()

    def get_defector_state(self):
        defectors = nx.get_node_attributes(self.G, 'defector')
        d_list = list(defectors.values())
        return sum(d_list)/len(d_list)


def make_punchline(n=100, gamma=2.5, temp=0.4, mean_deg=6, d=10,avg = 10):
    now = time.time()#get current time
    out_vals = np.zeros((d,d))#initialize array to store information
    C0_vals = np.linspace(0.2,0.8,d) #iterate over statrting rate of defectors
    '''I did a hacky fix here, the paper specified C as
    the rate of good boyos but we defined it as defectors so I just do 1 - C'''
    b_vals = np.linspace(5,25,d) # iterate over reward given
    for i, C0 in enumerate(C0_vals):
        for j, b in enumerate(b_vals):
            graph = buildNetwork.build_synthetic_network(n = n, gamma = gamma, temp = temp, mean_deg = mean_deg, C = 1-C0)
            # buildNetwork.draw_net(graph)
            myCrawler = graphCrawler(graph, b)#create crawler object
            myCrawler.iterate(avg) #iterate avg number of times than take the mean of the next avg iterations
            states = np.zeros(avg)
            print('INIT')
            for k in range(avg):
                myCrawler.iterate(1)
                states[k] = myCrawler.get_defector_state()
            out_vals[i,j] = np.mean(states) # Record the output state of the system
    times = time.time() - now #time difference
    print(times)#below are some quick calculations to see how long it should run on  full graph
    nO = 10000
    avg0 = 250
    iterations = 50
    qual= 20 * 60
    mult = (nO / n) * (avg0 / avg) * (iterations) * (qual / (d**2))
    print('Hours' + str(mult * (times/3600)))
    print(out_vals)
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(out_vals, cmap=plt.cm.bwr, alpha=0.8)
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
