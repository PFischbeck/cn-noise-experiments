import math
from typing import Optional

import networkit as nk


def generate_er(n: int, k: float, seed: Optional[int] = None):
    """Generates an Erdos-Renyi random graph"""

    if seed is not None:
        seed = abs(seed)
        nk.engineering.setSeed(seed, False)

    return nk.generators.ErdosRenyiGenerator(n, k / (n - 1)).generate()


def generate_hrg(n: int, k: float, beta: float, seed: Optional[int] = None):
    """Generates a hyperbolic random graph"""

    if seed is not None:
        nk.engineering.setSeed(seed, False)

    # Set temperature zero --> threshold model
    T = 0
    return nk.generators.HyperbolicGenerator(n, k, beta, T).generate()


def generate_rgg(n: int, k: float, seed: Optional[int] = None):
    """Generates a 2-dimensional random geometric graph"""

    import random

    import igraph

    if seed is not None:
        random.seed(seed)

    r = math.sqrt(k / (math.pi * (n - 1)))

    g_igraph = igraph.Graph.GRG(n, r, torus=True)

    g = nk.Graph(n)
    for u, l in enumerate(g_igraph.get_adjlist()):
        for v in l:
            if u < v:
                g.addEdge(u, v)
    return g
