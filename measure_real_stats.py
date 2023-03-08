import argparse
import csv
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


def experiment(file: str, no_header: bool, only_header: bool):
    writer = csv.writer(sys.stdout)
    if not no_header:
        writer.writerow(['graph', 'n', 'm', 'gcc'])
    if only_header:
        return

    g: nk.Graph = nk.readGraph(file, nk.Format.EdgeListSpaceZero)
    n = g.numberOfNodes()
    m = g.numberOfEdges()
    gcc = nk.globals.ClusteringCoefficient.exactGlobal(g)

    writer.writerow([Path(file).stem, n, m, gcc])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Measure statistics of real-world graphs.')
    parser.add_argument('--file', type=str, help='Input graph.')
    parser.add_argument('--no-header', action='store_true', help='Print no header.')
    parser.add_argument('--only-header', action='store_true', help='Print only the header.')

    args = parser.parse_args()
    if not args.only_header and not args.file:
        parser.error('--file is required if --only-header is not set.')

    experiment(args.file, args.no_header, args.only_header)

