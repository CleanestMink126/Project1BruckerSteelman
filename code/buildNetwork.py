import numpy as np
import matplotlib.pyplot as plt
import random
import networkx as nx
from math import pi, sin


def get_k_min(mean_deg, gamma):
    return mean_deg*((gamma-2)/(gamma-1))


def get_k_prob(val, mean_deg, gamma):
    min_k = get_k_min(mean_deg, gamma)
    return (gamma - 1) * (min_k**(gamma - 1))*(val**(gamma*-1))


def get_k_cdf(val, mean_deg, gamma):
    min_k = get_k_min(mean_deg, gamma)
    return (-min_k**(gamma-1))*val**(1-gamma)-(-min_k**(gamma-1))*0.00001**(1-gamma)


def get_k_cdf_inv(val, mean_deg, gamma):
    min_k = get_k_min(mean_deg, gamma)
    a = (gamma - 1) * (min_k ** (gamma - 1))
    d = (a*0.000001**(1-gamma))/(1-gamma)
    return (-(a+d)*(val**(1-gamma)))**(1/(1-gamma))


def k_distribution(mean_deg, gamma):
    k_vals = np.linspace(0.000001, 1, 1e5)
    k_probs = [get_k_cdf_inv(point, mean_deg, gamma) for point in k_vals]
    return (k_vals, k_probs)


def get_k_dist(mean_deg, gamma):
    rand_inv_val = random.uniform(0, 68041381.74397714)
    return get_k_cdf_inv(rand_inv_val, mean_deg, gamma)


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

        prob_connect = 1/(1+(d_val/(mu*ks[0]*ks[1])**(1/temp)))
        if random.uniform(0, 1) < prob_connect:  # If we actually connect the nodes
            G.add_edge(*edge)


def build_network(n, gamma, mean_deg, temp):
    G = nx.Graph()
    thetas = [random.uniform(0, 2*pi) for _ in range(n)]  # Map every node to a theta from a uniform distribution
    k_vals = [get_k_dist(mean_deg, gamma) for _ in range(n)]  # Assign each node a k randomly
    all_nodes = range(n)

    thetas_dict = dict(zip(all_nodes, thetas))
    k_dict = dict(zip(all_nodes, k_vals))
    G.add_nodes_from(all_nodes)
    # Assign node attributes
    nx.set_node_attributes(G, 'theta', thetas_dict)
    nx.set_node_attributes(G, 'k', k_dict)

    connect_nodes(G, mean_deg, temp)

    return G


# dist = k_distribution(5, 2.5)
# print(get_k_dist(5, 2.5))
# plt.loglog(*dist)
# plt.show()

net = build_network(100, 2.5, 10, 0.5)
nx.draw_circular(net)
