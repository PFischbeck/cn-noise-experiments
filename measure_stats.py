import argparse
import csv
import sys

import networkit as nk


def calc_common_neighbors(g: nk.Graph) -> dict:
    cni = nk.linkprediction.CommonNeighborsIndex(g)
    counts = {}

    def edge_func(u, v, _, id):
        counts[id] = cni.run(u, v)
    g.forEdges(edge_func)
    return counts


def experiment(file: str):
    edges = []

    is_random = {}
    with open(file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            u = int(row['u'])
            v = int(row['v'])
            is_edge_random = row['is_random'] == 'True'
            edges.append((u, v))
            is_random[(u, v)] = is_edge_random

    n = max(max(u, v) for u, v in edges) + 1
    combined = nk.Graph(n)
    for u, v in edges:
        combined.addEdge(u, v)

    combined.indexEdges()

    common_neighbor_scores = calc_common_neighbors(combined)

    writer = csv.writer(sys.stdout)
    writer.writerow(['common_neighbors', 'jaccard', 'hpi', 'hdi', 'is_random'])

    def edge_func(u, v, _, id):
        deg_u = combined.degree(u)
        deg_v = combined.degree(v)
        common_neighbors = common_neighbor_scores[id]
        jaccard = common_neighbors / (deg_u + deg_v - common_neighbors)
        hpi = common_neighbors / min(deg_u, deg_v)
        hdi = common_neighbors / max(deg_u, deg_v)
        is_edge_random = is_random[(u, v)]
        writer.writerow([common_neighbors, jaccard, hpi, hdi, is_edge_random])

    combined.forEdges(edge_func)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Measure statistics of generated graphs.')
    parser.add_argument('--file', type=str, required=True, help='Input graph.')

    args = parser.parse_args()
    experiment(args.file)

