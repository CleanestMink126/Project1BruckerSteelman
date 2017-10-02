import numpy as np
import matplotlib.pyplot as plt
import random
import networkx as nx
from math import pi, sin, cos, log


# Controls the value of the mean degree
def get_k_min(mean_deg, gamma):
    return mean_deg*((gamma-2)/(gamma-1))


# Returns a value of k based on a value from uniform distribution (0,1).
def get_k(val, mean_deg, gamma, x0=.508, x1=1e30):
    power = -gamma
    min_k = get_k_min(mean_deg, gamma)
    C = (gamma-1)*min_k**(gamma-1)
    # return (((power+1)/C)*val + x0**(power+1))**(1/(power+1))
    return ((x1**(power+1) - x0**(power+1))*val + x0**(power+1))**(1/(power+1))*(C**(9/10))


def k_distribution(mean_deg, gamma):
    k_vals = np.linspace(0.000001, 1, 1e5)
    k_probs = [get_k(point, gamma) for point in k_vals]
    return (k_vals, k_probs)


# Gets a value of K from the power-law distribution
def get_k_dist(mean_deg, gamma):
    rand_inv_val = random.uniform(0, 1)
    return get_k(rand_inv_val, mean_deg, gamma)


def all_possible_edges(G):
    for i, u in enumerate(G.nodes()):
        for j, v in enumerate(G.nodes()):
            if i > j:
                yield u, v


def connect_nodes(G, mean_deg, temp):
    edges_set = all_possible_edges(G)
    theta_vals = nx.get_node_attributes(G, 'theta')
    k_vals = nx.get_node_attributes(G, 'k')
    for edge in edges_set:
        thetas = (theta_vals[edge[0]], theta_vals[edge[1]])
        ks = (k_vals[edge[0]], k_vals[edge[1]])

        delta_theta = abs(pi-abs(pi-abs(thetas[1]-thetas[0])))
        d_val = (len(G.nodes())/(2*pi))*delta_theta
        mu = sin(temp*pi)/(2*mean_deg*temp*pi)

        prob_connect = 1/(1+((d_val/(mu*ks[0]*ks[1]))**(1/temp)))
        if random.uniform(0, 1) < prob_connect:  # If we actually connect the nodes
            G.add_edge(*edge)


def set_r_vals(G, gamma, mean_deg, temp, BA=False):
    k_vals = nx.get_node_attributes(G, 'k')
    c = mean_deg*(sin(temp*pi)/2*temp)*(((gamma-2)/(gamma-1))**2)
    R = 2*log(len(G.nodes())/c)
    k_min = get_k_min(mean_deg, gamma)
    if BA:  # If we're using a BA graph, the r value is simply based on the degree of the node
        max_deg = max(degrees(G))
        r_vals = [max_deg - G.degree(node) for node in G.nodes()]
    else:  # Otherwise, use the standard formula for computing r values
        r_vals = [R-2*log(k_vals[node]/k_min) for node in G.nodes()]
    r_dict = dict(zip(G.nodes(), r_vals))
    nx.set_node_attributes(G, name = 'r', values = r_dict)
    return r_dict


"""
Assigns the theta, r, k, and position values of the graph.
"""
def assign_network_attributes(G, C, gamma, mean_deg, temp, BA=False):
    all_nodes = G.nodes()
    n = len(all_nodes)
    thetas = [random.uniform(0, 2*pi) for _ in range(n)]  # Map every node to a theta from a uniform distribution
    k_vals = [get_k_dist(mean_deg, gamma) for _ in range(n)]  # Assign each node a k randomly
    if BA:  # If we're using a BA graph, distribute defectors according to their degree
        max_deg = max(degrees(G))
        defector_list = [random.uniform(0, max_deg) < G.degree(node)*C for node in all_nodes]
    else:
        defector_list = [random.uniform(0, 1) < C for _ in range(n)]


    thetas_dict = dict(zip(all_nodes, thetas))
    k_dict = dict(zip(all_nodes, k_vals))
    defect_dict = dict(zip(all_nodes, defector_list))
    # Assign node attributes
    nx.set_node_attributes(G, name ='theta', values= thetas_dict)
    nx.set_node_attributes(G, name ='k', values=k_dict)
    nx.set_node_attributes(G, name ='defector', values= defect_dict)

    r_vals = set_r_vals(G, gamma, mean_deg, temp, BA=BA)

    pos_vals = [(r_vals[node]*cos(thetas_dict[node]), r_vals[node]*sin(thetas_dict[node])) for node in all_nodes]
    pos_dict = dict(zip(all_nodes, pos_vals))

    nx.set_node_attributes(G, name ='pos', values=pos_dict)


# Builds a synthetic network based on the network building algorithm defined in the paper.
def build_synthetic_network(n, C, gamma, mean_deg, temp):
    G = nx.Graph()
    G.add_nodes_from(range(n))
    assign_network_attributes(G, C, gamma, mean_deg, temp)
    connect_nodes(G, mean_deg, temp)
    return G


def build_ba_network(n, C, gamma, mean_deg, temp, num_connect=1):
    G = nx.barabasi_albert_graph(n, num_connect)
    assign_network_attributes(G, C, gamma, mean_deg, temp, BA=True)
    return G


def degrees(G):
    """List of degrees for nodes in `G`.

    G: Graph object

    returns: list of int
    """
    return [G.degree(u) for u in G]


def draw_net(graph, **kwargs):
    defect_dict = nx.get_node_attributes(graph, 'defector')
    print(defect_dict)
    colors = {True: 'orange', False: 'b'}
    defect_list = [colors[defect_dict[node]] for node in graph.nodes()]
    nx.draw(graph, nx.get_node_attributes(graph, 'pos'), node_color=defect_list, node_size=20, width=0.1, **kwargs)
    plt.show()


if __name__ == '__main__':
    # net = build_synthetic_network(250, 0.1, 2.5, 20, 0.4)
    net = build_ba_network(100, 0.2, 2.5, 20, 0.4, num_connect=15)
    # print(np.mean(degrees(net)))
    draw_net(net)
