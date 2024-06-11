import igraph as ig
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def generate_signed_polarized_network(num_nodes_per_community=10, p_intra=0.8, p_inter=0.2):
    num_nodes = 2 * num_nodes_per_community
    g = ig.Graph()

    # Add vertices
    g.add_vertices(num_nodes)

    # Add positive intra-community edges
    for i in range(num_nodes_per_community):
        for j in range(i + 1, num_nodes_per_community):
            if np.random.rand() < p_intra:
                g.add_edge(i, j, sign=1)
        for j in range(num_nodes_per_community, num_nodes):
            if np.random.rand() < p_inter:
                g.add_edge(i, j, sign=-1)

    for i in range(num_nodes_per_community, num_nodes):
        for j in range(i + 1, num_nodes):
            if np.random.rand() < p_intra:
                g.add_edge(i, j, sign=1)

    return g

def edgelist_from_adjacency_matrix(df: pd.DataFrame):
    source, target = np.where(df != 0)
    weights = df.values[source, target]
    edgelist = pd.DataFrame({
        'source': df.index[source],
        'target': df.columns[target],
        'weight': weights
    })
    return edgelist

def graph_from_edgelist(edgelist: pd.DataFrame):
    g = ig.Graph.TupleList(edgelist.itertuples(index=False), edge_attrs='sign')
    return g