import argparse

import networkit as nk

from graph_generators import generate_hrg

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a hyperbolic random graph.')
    parser.add_argument('--n', type=int, required=True, help='Number of nodes')
    parser.add_argument('--k', type=float, required=True, help='Average node degree')
    parser.add_argument('--beta', type=float, required=True, help='Power law beta')
    parser.add_argument('--seed', type=int, required=True, help='Seed')
    parser.add_argument('file', type=str, help='Output filename')

    args = parser.parse_args()
    n = args.n
    k = args.k
    beta = args.beta
    seed = args.seed
    filename = args.file

    g = generate_hrg(n, k, beta, seed)
    nk.writeGraph(g, filename, nk.Format.EdgeListSpaceZero)
