import argparse

import networkit as nk

from graph_generators import generate_rgg

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a random geometric graph.')
    parser.add_argument('--n', type=int, required=True, help='Number of nodes')
    parser.add_argument('--k', type=float, required=True, help='Average degree')
    parser.add_argument('--seed', type=int, required=True, help='Random seed')
    parser.add_argument('file', type=str, help='Output filename')

    args = parser.parse_args()
    n = args.n
    k = args.k
    seed = args.seed
    filename = args.file

    g = generate_rgg(n, k, seed)
    nk.writeGraph(g, filename, nk.Format.EdgeListSpaceZero)
