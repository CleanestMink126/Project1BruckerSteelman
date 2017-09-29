import numpy as np
import matplotlib.pyplot as plt
import random
import networkx as nx
from sympy import *
from math import pi, sin


def get_k_min(mean_deg, gamma):
    return mean_deg*((gamma-2)/(gamma-1))


def get_k_prob(val, mean_deg, gamma):
    min_k = get_k_min(mean_deg, gamma)
    return (gamma - 1) * (min_k**(gamma - 1))*((val+1e-10)**(gamma*-1))


def get_k_cdf(val, mean_deg, gamma):
    min_k = get_k_min(mean_deg, gamma)
    k = Symbol('k', positive=True)
    prob = get_k_prob(k, mean_deg, gamma)
    cdf = integrate(prob, (k, 0, val))/integrate(prob, (k, 0, 1e64))
    return cdf


def get_k_cdf_norm(val, mean_deg, gamma):
    return get_k_cdf(val, mean_deg, gamma)/get_k_cdf(1e10, mean_deg, gamma)


def get_k_cdf_inv(val, mean_deg, gamma):
    b = Symbol('b', positive=True)
    y = Symbol('y', positive=True)
    cdf=get_k_cdf(b,mean_deg,gamma)
    soln=solve(y-cdf,b)[0]
    print(soln.subs(y,val))

    min_k = get_k_min(mean_deg, gamma)
    a = (gamma - 1) * (min_k ** (gamma - 1))
    d = (a*1e-10**(1-gamma))/(1-gamma)
    return (-(a+d)*(val**(1-gamma)))**(1/(1-gamma))


def get_k(val, gamma, x0=1e-20, x1=1e20):
    power = -gamma
    return ((x1**(power+1) - x0**(power+1))*val + x0**(power+1))**(1/(power+1))



def k_distribution(mean_deg, gamma):
    k_vals = np.linspace(0.000001, 1, 1e5)
    k_probs = [get_k(point, gamma) for point in k_vals]
    return (k_vals, k_probs)


def get_k_dist(mean_deg, gamma):
    rand_inv_val = random.uniform(0, 1)
    return get_k(rand_inv_val, gamma)


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
        print(d_val, mu, ks[0]*ks[1], prob_connect)
        if random.uniform(0, 1) < prob_connect:  # If we actually connect the nodes
            G.add_edge(*edge)


def build_network(n, gamma, mean_deg, temp):
    G = nx.Graph()
    thetas = [random.uniform(0, 2*pi) for _ in range(n)]  # Map every node to a theta from a uniform distribution
    k_vals = [get_k_dist(mean_deg, gamma) for _ in range(n)]  # Assign each node a k randomly
    print(k_vals)
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
print(new_get_k(.5,2.5))
# plt.loglog(*dist)
# plt.show()

# net = build_network(10, 2.5, 0.1, 0.4)
# print(nx.get_node_attributes(net, 'theta'))
# nx.draw_circular(net)
# plt.show()
