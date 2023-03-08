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
    mixed = nk.readGraph(file, nk.Format.EdgeListSpaceZero)

    mixed.indexEdges()

    common_neighbor_scores = calc_common_neighbors(mixed)

    writer = csv.writer(sys.stdout)
    writer.writerow(['u', 'v', 'common_neighbors', 'jaccard', 'hpi', 'hdi'])

    def edge_func(u, v, _, id):
        deg_u = mixed.degree(u)
        deg_v = mixed.degree(v)
        common_neighbors = common_neighbor_scores[id]
        jaccard = common_neighbors / (deg_u + deg_v - common_neighbors)
        hpi = common_neighbors / min(deg_u, deg_v)
        hdi = common_neighbors / max(deg_u, deg_v)
        writer.writerow([u, v, common_neighbors, jaccard, hpi, hdi])

    mixed.forEdges(edge_func)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Measure statistics of real-world mixed graphs.')
    parser.add_argument('--file', type=str, required=True, help='Input graph.')

    args = parser.parse_args()
    experiment(args.file)

