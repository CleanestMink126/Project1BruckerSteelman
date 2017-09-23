
#### Abstract:
The paper “Collective navigation of complex networks: Participatory greedy routing” explores the world of IoT devices
and their abstraction into graphical models. The paper modeled the affect of "defector" nodes in the network's ability to send information from one side of the network to the other. Defector nodes are instantiated in the model and can spread their defector property to their neighbors as well as lose that property. The probability of a node becoming a defector is determined by the presence of defectors in its proximity, the amount of messages sent, and the amount of reward the node gets from sending a message. The paper found compelling results on the importance of the reward each node recieves when it sucessfully delivers a message and the imporance of the state of "hubs" in the network, but their model was tested under very specific circumstances. We plan to investigate into the role of different graph types, algorithms to determine defection,  algorithms to determine kickback, and initial states of the board on the spread of defection.

#### Bibiliography


##### Citation:
Kleineberg, Kaj-Kolja, and Dirk Helbing. “Collective navigation of complex networks: Participatory greedy routing.” Nature News,
Nature Publishing Group, 6 June 2017, www.nature.com/articles/s41598-017-02910-x. Accessed 21 Sept. 2017.

##### Summary:
This paper dives into abstracting a simulating systems such as the emerging network of IoT devices which desire
to send data to a desired location. Since it is not efficient for every node to know the state of the entire system,
a method of communication can be a form of "greedy algorithm" in which each nodes sends the data to the nearest neighbor
closest to the destination. However, they added in a probability that a node would become a "defector" which renders the
message unsendable and in large numbers invalidates the network. This probability is based on the number of defector neighbors
and how much a reward the node gets for properly delivering a message. They found that each graph they instantiate either
collapses into nearly all defector or participant given enough time. The probability of collapsing into each is heavily
influenced by both the size of the kickback the nodes recieve and the state of some "hubs" in the graph that connect to 
a large number of nodes. Additionally, they found the state of defectors tend to first organize themselves into clusters
of all participant or all defector.



##### Citation:
Krapivsky, P. L., and S. Redner. “Emergent Network Modularity.” [1706.01514] Emergent Network Modularity,
20 June 2017, arxiv.org/abs/1706.01514. Accessed 18 Sept. 2017.

##### Summary:
This paper explored a model of graph growth and it's emergent properties. The method of growth was 
for every new node added, it was randomly assigned to a node in the graph, and then randomly connected
to a neighbor of that node. The paper cited several applications of this application in the past with
directed graphs and proposed to further explore the concept in the context of undirected graphs, which 
better approximate topics such as social media connections, which are often two way. However, they did
not much go into the connection of this growth to real world systems, but rather explored some
conterintuitive properties of the network, mostly the surprising amount of "star structures" that arise.
Star structures are when a single node is the only connection between all other nodes in the graph. They
appear at a startling amount for this growth, with a 2/(N-1) occurence for N nodes. The same rate applies
for star graphs with little imperfections. Additionally, the likelyhood for very large star structures to
develop with very large graphs (~E6 Nodes) is also very likely, with the graphs appearing as shallowly linked
individual structures rather than a cohesive unit.


##### Citation:
  Kallus, Zsofia, Daniel Kondor, Jozsef Steger, Istvan Csabai, Eszter Bokanyi, and Gabor Vattay. "Video Pandemics: Worldwide Viral Spreading of Psy's Gangnam Style Video." [1707.04460] Video Pandemics: Worldwide Viral Spreading of Psy's Gangnam Style Video. 14 July 2017. Web. 15 Sept. 2017.

##### Summary:
  This paper explored the spread of viral videos, specifically "Gangnam Style" on the internet. The group showed that they were
able to construct a model that accurately portrayed the spread of viral videos by examining the number of common followers
between different regions.
First, they constructed a graph of 261 large administrative geographical regions in the internet, then connected the nodes
and weighted each node based on individual level followers between regions. Next, by using both google trends
and tweet keyword analysis was able to map the prevalence of Gangnam Style in each region over time. By approximating the
origin of the video, they were able to model the time it took for gangnam style to reach each region based on either
geographical distance from origin, or the graphical model distance from the origin. They were then able to indicate the
validity of their model by showing the linear trend between time to region and distance in their model compared to the lack of
a trend in time to region and geographical distance to region.


#### Replication and Extension


#### Results


#### Causes for Concern:
Some problems we may run into include making decisions about how to map the graph into a 2 dimensional space. The paper the
experiment is based on uses some somewhat complex functions to determine distance, so we will need to either determine how to use those and which parts are important or make our own graph with a its compelling explanation for architecture. Additionally, it may be difficult to determine the best qualities of the graph to vary in order to yield interesting results.

#### Next Steps
1. Agree on best way to contruct the positions and connections inside the graph.
2. Write code to make the graph
3. Write function to simulate message transmission across nodes.
4. Write functions to update individual nodes with defection probabilities.
