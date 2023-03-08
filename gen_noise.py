import argparse
import csv

import networkit as nk

from graph_generators import generate_er


def experiment(g1: nk.Graph, ratio: float, output: str, seed: int):
    n = g1.numberOfNodes()
    m = g1.numberOfEdges()
    new_edges = m * ratio
    g2 = generate_er(n, 2 * new_edges / n, seed)

    combined = nk.Graph(n)
    for u, v in g1.iterEdges():
        combined.addEdge(u, v)
    for u, v in g2.iterEdges():
        combined.addEdge(u, v)

    combined.indexEdges()

    with open(output, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["u", "v", "is_random"])

        def edge_func(u, v, _, id):
            is_random = not g1.hasEdge(u, v)
            writer.writerow([u, v, is_random])

        combined.forEdges(edge_func)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate noise on top of a graph.')
    parser.add_argument('--file', type=str, help='Input graph.')
    parser.add_argument('--m', type=float, required=True, help='Ratio of additional edges to base edges')
    parser.add_argument('output', type=str, help='Output file.')

    args = parser.parse_args()
    output = args.output
    m = args.m
    # Use file name and m as seed
    seed = hash((output, m))
    g = nk.readGraph(args.file, nk.Format.EdgeListSpaceZero)
    experiment(g, m, output, seed)

