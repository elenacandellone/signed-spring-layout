import igraph as ig
import numpy as np
import matplotlib.pyplot as plt

def signed_fruchterman_reingold(graph, iterations=100, area=100.0, t=1.0, cooling_factor=0.99, radius=50.0, seed=42):
    np.random.seed(seed) 
    pos = np.random.rand(len(graph.vs), 2) * area - area / 2
    k = np.sqrt(area / len(graph.vs))

    def fa(x):
        return (x ** 2) / k

    def fr(x):
        return (k ** 2) / x

    for _ in range(iterations):
        displacement = np.zeros((len(graph.vs), 2))

        # Calculate repulsive forces
        for v in range(len(graph.vs)):
            for u in range(len(graph.vs)):
                if u != v:
                    delta = pos[v] - pos[u]
                    distance = np.linalg.norm(delta)
                    displacement[v] += (delta / distance) * fr(distance)

        # Calculate attractive forces
        for e in graph.es:
            source, target = e.tuple
            delta = pos[source] - pos[target]
            distance = np.linalg.norm(delta)
            if e['sign'] > 0:
                # Attractive force for positive edges
                force = (delta / distance) * fa(distance)
            else:
                # Repulsive force for negative edges
                force = -(delta / distance) * fr(distance)
            displacement[source] -= force
            displacement[target] += force

        # Limit displacement and update positions
        for v in range(len(graph.vs)):
            disp_norm = np.linalg.norm(displacement[v])
            #if disp_norm > 0:
            displacement[v] = (displacement[v] / disp_norm) * min(disp_norm, t)
            pos[v] += displacement[v]

            if np.linalg.norm(pos[v]) > radius:
                pos[v] = (pos[v] / np.linalg.norm(pos[v])) * radius

        # Cool down
        t *= cooling_factor

    return pos


