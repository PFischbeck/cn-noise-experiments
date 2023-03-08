import argparse
import csv
import random
import sys
from pathlib import Path

import networkit as nk


def calc_common_neighbors(g: nk.Graph) -> dict:
    cni = nk.linkprediction.CommonNeighborsIndex(g)
    counts = {}

    def edge_func(u, v, _, id):
        counts[id] = cni.run(u, v)
    g.forEdges(edge_func)
    return counts


def experiment(file: str, ratio: float, no_header: bool, only_header: bool):
    writer = csv.writer(sys.stdout)
    if not no_header:
        writer.writerow(['graph', 'ratio', 'n', 'm',
                        'gcc', 'components', 'avg_val'])
    if only_header:
        return

    edges = []
    feature = "common_neighbors"
    n = 0
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            u = int(row["u"])
            v = int(row["v"])
            n = max([n, u + 1, v + 1])
            edges.append((float(row[feature]), random.random(), u, v))

    m = len(edges)
    m_intrusion = int(m * ratio)
    m_base = m - m_intrusion
    # Sort by feature, tie by random value to have random ordering for same feature value
    edges.sort()

    g_base = nk.Graph(n)
    g_intrusion = nk.Graph(n)
    vals_base = []
    vals_intrusion = []
    for index, (feature_val, _, u, v) in enumerate(edges):
        if index < m_intrusion:
            g_intrusion.addEdge(u, v)
            vals_intrusion.append(feature_val)
        else:
            g_base.addEdge(u, v)
            vals_base.append(feature_val)

    for name, g, vals in [("base", g_base, vals_base), ("intrusion", g_intrusion, vals_intrusion)]:
        n = g.numberOfNodes()
        m = g.numberOfEdges()
        gcc = nk.globals.ClusteringCoefficient.exactGlobal(g)
        avg_val = sum(vals) / len(vals) if vals else 0
        cc = nk.components.ConnectedComponents(g)
        cc.run()
        components = cc.numberOfComponents()
        writer.writerow((f"{Path(file).stem}_{name}",
                        ratio, n, m, gcc, components, avg_val))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Measure statistics of real-world mixed graphs.')
    parser.add_argument('--file', type=str, help='Input edge stats file.')
    parser.add_argument('--ratio', type=float,
                        help='Ratio of edges that should be treated as overlay.')
    parser.add_argument('--no-header', action='store_true',
                        help='Print no header.')
    parser.add_argument('--only-header', action='store_true',
                        help='Print only the header.')

    args = parser.parse_args()
    if not args.only_header and not args.file:
        parser.error('--file is required if --only-header is not set.')
    experiment(args.file, args.ratio, args.no_header, args.only_header)
