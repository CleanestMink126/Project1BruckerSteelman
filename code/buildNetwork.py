import numpy as np
import matplotlib.pyplot as plt
import random


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


dist = k_distribution(5, 2.5)
print(get_k_dist(5, 2.5))
plt.loglog(*dist)
plt.show()
