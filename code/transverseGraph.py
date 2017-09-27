import random
import networkx as nx
import math



def findClosestNode(G, node, target,posDict):
    allNeighbors = G[node]
    closeNode = random.choice(allNeighbors.())\\TODO
    minDist = findDistance(closeNode,target,posDict)
    for i,w in allNeighbors:
        dist = findDistance(i,target,posDict)
        if dist < minDist:
            misDist = dist
            closeNode = i
    return closeNode

def findDistance(node, target, posDict):
    posN = posDict[node]
    posT = posDict[target]
    return math.sqrt((posN[0]-posT[0])**2 + (posN[1]-posT[1])**2)



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
# nx.draw(G, pos,
#         node_color=COLORS[1],
#         node_shape='s',
#         node_size=2500,
#         with_labels=True)
#
# nx.draw_networkx_edge_labels(G, pos,
#                              edge_labels=drive_times)
#
