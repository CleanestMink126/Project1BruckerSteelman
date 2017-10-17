import random
import networkx as nx
import math
import numpy as np
import buildNetwork
import matplotlib.pyplot as plt
import time
from collections import Counter


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
        self.bottomVal = -150
        self.degrees = {}
        for node in G.nodes():
            self.degrees[node] = len(list(self.G[node].keys()))
        self.topDegrees = dict(Counter(self.degrees).most_common(int(len(G.nodes)/20)))

        if weightDict is None:
            self.weightDict = dict.fromkeys(G.nodes(),5)
        if defectorDict is None:
            self.defectorDict = nx.get_node_attributes(self.G, name ='defector')
        if posDict is None:
            self.posDict = nx.get_node_attributes(self.G, name ='pos')

        # print(self.weightDict)

        nx.set_node_attributes(self.G, name ='time',values = {key: random.randint(-15,0) for key in G.nodes()})
        # print({key: random.randint(-10,0) for key in G.nodes()})
        nx.set_node_attributes(self.G, name ='weight',values = self.weightDict)
        nx.set_node_attributes(self.G, name ='degrees',values = self.degrees)
        # nx.set_node_attributes(self.G, 'defector',self.defectorDict)


    def findDistance(self,node, target):#simple function to find disance between nodes
        thetaN = self.thetas_dict[node]#Thetas are the angles of nodes with respect to the center of the graph
        thetaT = self.thetas_dict[target]
        # print('Theta'+  str(thetaN))
        delta = abs(math.pi - abs(math.pi - abs(thetaN - thetaT)))
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
            return [] #return
        nextnode = self.findClosestNode(node, target)
        if nextnode == target:#if we reach the end, return the end
            return [node] + [nextnode]
        seen.add(node)
        return [node] + self.getPath(nextnode, target, seen=seen)


    def updateWeights(self,nodeList,deliveredBool):
        if not nodeList:
            return
        lastNode = nodeList[-1]
        reverseList = nodeList[::-1]#run through the path and update each weight according to length
        weightDict = nx.get_node_attributes(self.G, 'weight')
        for l,i in enumerate(reverseList):
            weightDict[i] = weightDict[i]+ deliveredBool*(self.b/len(reverseList)) - 1
        nx.set_node_attributes(self.G, name = 'weight',values=weightDict)

    def updateConversion(self):
        weightDict = nx.get_node_attributes(self.G, 'weight')
        defectorDict = nx.get_node_attributes(self.G, 'defector')
        timeDict = nx.get_node_attributes(self.G, 'time')


        for node in self.G.nodes():
            if defectorDict[node] == 0:
                weighti = weightDict[node]
                try:
                    expVal = math.exp((weighti)/self.k)#find e value
                    # print(expVal)
                    probabilityChange = 1 / (1 + expVal)#calculate proability that the original node will copy its neighbor
                    changeBool = random.random() < probabilityChange#make decision based on probability
                    if changeBool:
                        self.defectorDict[node] = 1#store difference in defectorness in another dict
                        timeDict[node] = -15
                except:
                    continue
            elif defectorDict[node] == 1:
                time = timeDict[node]
                try:
                    expVal = math.exp((-1 * time)/2)#find e value
                    # print(expVal)
                    probabilityChange = 1 / (1 + expVal)#calculate proability that the original node will copy its neighbor
                    changeBool = random.random() < probabilityChange#make decision based on probability
                    if changeBool:
                        self.defectorDict[node] = 0#store difference in defectorness in another dict
                    else:
                        timeDict[node] = timeDict[node] + 1
                except:
                    continue

        # nx.set_node_attributes(self.G,name = 'weight',values = self.weightDict)
        nx.set_node_attributes(self.G, name ='defector',values = self.defectorDict)
        nx.set_node_attributes(self.G, name ='time',values = timeDict)



    def iterate(self, numTimes):
        results = []
        allNodes = self.G.nodes()#get all the nodes
        for i in range(numTimes):#number of iterations and updates to execute
            for i in range(nx.number_of_nodes(self.G)):
                nodeList = random.sample(allNodes, 2)#get random 2 nodes
                node1 = nodeList[0]
                node2 = nodeList[1]
                path = self.getPath(node1,node2)
                seen_nodes = [True if node in path else False for node in self.G.nodes()]
                nx.set_node_attributes(self.G, name='path', values = dict(zip(self.G.nodes(),seen_nodes)))

                # buildNetwork.draw_net(self.G, path=True)
                # print(node1)
                # print(node2)
                # print(path)
                if path and path[-1] == node2:#if the last node is the target node
                    # print('Success!')
                    self.updateWeights(path,1)
                    results.extend([1])
                else:
                    # print('FAIl!')
                    self.updateWeights(path,0)
                    results.extend([0])
            # print('UPDATING-------')
            self.updateConversion()
        return results

    def get_cooperator_state(self):
        defectors = nx.get_node_attributes(self.G, 'defector')
        d_list = list(defectors.values())
        return 1 - sum(d_list)/len(d_list)

    def get_cooperator_state_weighted(self):
        defectors = nx.get_node_attributes(self.G, 'defector')
        numDef = 0
        print('Top Degrees',self.topDegrees)
        for i in self.topDegrees.keys():
            numDef += defectors[i]

        return numDef/len(self.topDegrees)


def make_punchline(n=100, gamma=2.5, temp=0.4, mean_deg=.5, d=10, avg = 5):
    now = time.time()#get current time
    out_vals = np.zeros((d,d))#initialize array to store information
    sent_vals = np.zeros((d,d))
    C0_vals = np.linspace(0.0,0.6,d) #iterate over statrting rate of defectors
    '''I did a hacky fix here, the paper specified C as
    the rate of good boyos but we defined it as defectors so I just do 1 - C'''
    b_vals = np.linspace(0,35,d) # iterate over reward given
    for i, C0 in enumerate(C0_vals):
        for j, b in enumerate(b_vals):
            states = []
            sent = []
            print(str(i) + ' ' + str(j))
            for l in range(3):
                graph = buildNetwork.build_synthetic_network(n = n, gamma = gamma, temp = temp, mean_deg = mean_deg, C = C0)
                # buildNetwork.draw_net(graph)
                myCrawler = graphCrawler(graph, b)#create crawler object
                myCrawler.iterate(50) #iterate avg number of times than take the mean of the next avg iterations
                for k in range(avg):
                    res = myCrawler.iterate(1)
                    sent.append((sum(res)/len(res)))
                    states.append(myCrawler.get_cooperator_state())
            out_vals[i,j] = np.mean(sent) # Record the output state of the system
    times = time.time() - now #time difference
    # print(times)#below are some quick calculations to see how long it should run on  full graph
    # nO = 10000
    # avg0 = 250
    # iterations = 50
    # qual= 20 * 60
    # mult = (nO / n) * (avg0 / avg) * (iterations) * (qual / (d**2))
    # print('Hours' + str(mult * (times/3600)))
    # print(out_vals)
    # f, axarr = plt.subplots(2)
    # heatmap = axarr[0].pcolor(out_vals, cmap=plt.cm.bwr, alpha=0.8)
    # plt.colorbar(heatmap, ax=axarr[0])
    # axarr[0].set_xticklabels(np.around(b_vals,0), minor=False)
    # axarr[0].set_yticklabels(np.around(C0_vals,2), minor=False)
    # axarr[0].set_title('Percent Defector Versus Payoff and Initial Percent Defector')
    # axarr[0].set_xlabel('Payoff (with cost 1)')
    # axarr[0].set_ylabel('Initial Defector Rate')
    # heatmap = axarr[1].pcolor(sent_vals, cmap=plt.cm.bwr, alpha=0.8)
    # plt.colorbar(heatmap, ax=axarr[1])
    # axarr[1].set_xticklabels(np.around(b_vals,0), minor=False)
    # axarr[1].set_yticklabels(np.around(C0_vals,2), minor=False)
    # axarr[1].set_xlabel('Payoff (with cost 1)')
    # axarr[1].set_ylabel('Initial Defector Rate')
    # axarr[1].set_title('Percent Not Sent Versus Payoff and Initial Percent Defector')
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(out_vals, cmap=plt.cm.RdYlBu, alpha=0.8)
    cbar = fig.colorbar(heatmap, ticks = [0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_xticklabels(np.around(b_vals,0), minor=False)
    ax.set_yticklabels(np.around(C0_vals,2), minor=False)
    plt.show()


if __name__ == '__main__':
    n = 100
    gamma = 2.5
    temp = 0.4
    meanDeg = 3.5
    c = 0.0
    graph = buildNetwork.build_synthetic_network(n = n, gamma = gamma, temp = temp, mean_deg = meanDeg, C = c)
    myCrawler = graphCrawler(graph, 5)
    buildNetwork.draw_net(myCrawler.G)
    # res = myCrawler.iterate(10)
    numGraphs = 10
    top5List = np.zeros((numGraphs,50),dtype ='float_')
    prcList = np.zeros((numGraphs,50),dtype ='float_')
    for j in range(numGraphs):
        graph = buildNetwork.build_synthetic_network(n = n, gamma = gamma, temp = temp, mean_deg = meanDeg, C = c)
        myCrawler = graphCrawler(graph, 8)
        for i in range(50):
            # print(nx.get_node_attributes(myCrawler.G, 'weight'))
            top5List[j][i] = myCrawler.get_cooperator_state_weighted()
            prcList[j][i] = 1 - myCrawler.get_cooperator_state()
            res = myCrawler.iterate(1)
            defectorDict = nx.get_node_attributes(myCrawler.G, 'defector')
            for i in myCrawler.topDegrees.keys():
                defectorDict[i] = 1
                myCrawler.defectorDict[i] = 1
            nx.set_node_attributes(myCrawler.G, name ='defector',values = defectorDict)
            print('Sent:',sum(res)/len(res))
            print('Cooperator state', myCrawler.get_cooperator_state())
            # buildNetwork.draw_net(myCrawler.G)
    top5List = np.mean(top5List, axis=0)
    prcList = np.mean(prcList, axis=0)
    plt.plot(np.linspace(1,len(top5List),len(top5List)),top5List,label="5 Highest Degree Nodes")    #linspace(start,end,number of points
    plt.plot(np.linspace(1,len(top5List),len(top5List)),prcList,label="All Nodes")    #linspace(start,end,number of points)
    plt.legend()
    plt.xlabel('Iterations')
    plt.ylabel('Percent Defector')
    plt.show()

    # coops = []
    # for _ in range(100):
    #     myCrawler.iterate(1)
    #     coops.extend([myCrawler.get_cooperator_state()])
    #
    # graph = buildNetwork.build_synthetic_network(n = n, gamma = gamma, temp = temp, mean_deg = meanDeg, C = c)
    # myCrawler = graphCrawler(graph, 10)
    # buildNetwork.draw_net(myCrawler.G)
    # coops2 = []
    # for _ in range(100):
    #     myCrawler.iterate(1)
    #     coops2.extend([myCrawler.get_cooperator_state()])
    #
    # coop_plot, = plt.plot(coops, label='b=25')
    # coop_plot2, = plt.plot(coops2, label='b=10')
    # plt.legend(handles=[coop_plot, coop_plot2])
    # plt.xlabel('Iterations')
    # plt.ylabel('Proportion of cooperators')
    # plt.title('Proportion of cooperators over time')
    # plt.show()
    # print(sum(res2)/len(res2))

    # make_punchline()
