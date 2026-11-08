import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


#Tree graph
#G = nx.random_labeled_tree(30, seed=45)

#GNP graph
G = nx.fast_gnp_random_graph(30, 0.15, seed=45)

#Newman graph
#G = nx.newman_watts_strogatz_graph(30, 4, 0.2, seed=45)


k = 4
n = G.number_of_nodes()

pos = nx.spring_layout(G, seed=45)


def connectivity(graph):
    if len(graph.nodes()) == 0:
        return 0
    return len(max(nx.connected_components(graph), key=len))

#def connectivity(graph):
#    if graph.number_of_nodes() <= 1:
#        return 0
#    return nx.node_connectivity(graph)



#GREEDY ALGORITHM
def greedy_algorithm(graph, k):
    G_copy = graph.copy()

    I = nx.maximal_independent_set(G_copy)

    non_I_nodes = [node for node in G_copy.nodes() if node not in I]

    centrality = nx.degree_centrality(G_copy)

    sorted_nodes = sorted(
        non_I_nodes,
        key=lambda x: centrality[x],
        reverse=True
    )

    nodes_to_remove = sorted_nodes[:k]

    G_copy.remove_nodes_from(nodes_to_remove)

    return G_copy, nodes_to_remove



#PARDALOS ALGORITHM
def pardalos_algorithm(graph, k):
    MIS = nx.maximal_independent_set(graph)

    current_nodes = set(MIS)

    removed_nodes = [
        node for node in graph.nodes()
        if node not in MIS
    ]

    H = graph.subgraph(current_nodes).copy()

    target_size = n - k

    added_nodes = []

    while H.number_of_nodes() < target_size:
        best_node = None
        best_score = float('inf')

        for node in removed_nodes:
            temp_graph = H.copy()
            temp_graph.add_node(node)

            for neighbor in graph.neighbors(node):
                if neighbor in temp_graph:
                    temp_graph.add_edge(node, neighbor)

            score = connectivity(temp_graph)

            if score < best_score:
                best_score = score
                best_node = node

        H.add_node(best_node)

        for neighbor in graph.neighbors(best_node):
            if neighbor in H:
                H.add_edge(best_node, neighbor)

        added_nodes.append(best_node)
        removed_nodes.remove(best_node)

    final_removed = [
        node for node in graph.nodes()
        if node not in H.nodes()
    ]

    return H, final_removed



#BETWEENNESS CENTRALITY ALGORITHM
def betweenness_algorithm(graph, k):
    G_copy = graph.copy()

    bc = nx.betweenness_centrality(G_copy)

    sorted_nodes = sorted(
        bc,
        key=bc.get,
        reverse=True
    )

    critical_nodes = sorted_nodes[:k]

    G_copy.remove_nodes_from(critical_nodes)

    return G_copy, critical_nodes


#EXHAUSTIVE ALGORITHM
def exhaustive_algorithm(graph, k):
    best_score = float('inf')
    best_set = None

    for nodes in combinations(graph.nodes(), k):
        temp_graph = graph.copy()
        temp_graph.remove_nodes_from(nodes)

        score = connectivity(temp_graph)

        if score < best_score:
            best_score = score
            best_set = nodes

    G_final = graph.copy()
    G_final.remove_nodes_from(best_set)

    return G_final, best_set


#plt.figure(figsize=(8, 8))
fig, ax = plt.subplots(figsize=(8, 8))
nx.draw(
    G,
    pos=pos,
    with_labels=True,
    node_color="lightblue",
    ax=ax
)

ax.set_title(f"Original Graph\nConnectivity: {connectivity(G)}")
plt.show()


G_greedy, removed_greedy = greedy_algorithm(G, k)
G_pardalos, removed_pardalos = pardalos_algorithm(G, k)
G_between, removed_between = betweenness_algorithm(G, k)
G_exhaustive, removed_exhaustive = exhaustive_algorithm(G, k)





print("\nGreedy removed:", removed_greedy)
print("Greedy connectivity:", connectivity(G_greedy))

print("\nPardalos removed:", removed_pardalos)
print("Pardalos connectivity:", connectivity(G_pardalos))

print("\nBetweenness removed:", removed_between)
print("Betweenness connectivity:", connectivity(G_between))

print("\nExhaustive removed:", removed_exhaustive)
print("Exhaustive connectivity:", connectivity(G_exhaustive))




fig, axes = plt.subplots(2, 2, figsize=(12, 12))

nx.draw(
    G_greedy,
    pos=pos,
    with_labels=True,
    node_color="lightblue",
    ax=axes[0, 0]
)
axes[0, 0].set_title(f"Greedy\nRemoved: {removed_greedy}\nConnectivity: {connectivity(G_greedy)}")

#axes[0, 0].set_title("Greedy")

nx.draw(
    G_pardalos,
    pos=pos,
    with_labels=True,
    node_color="lightblue",
    ax=axes[0, 1]
)
axes[0, 1].set_title(f"Pardalos\nRemoved: {removed_pardalos}\nConnectivity: {connectivity(G_pardalos)}")

#axes[0, 1].set_title("Pardalos")

nx.draw(
    G_between,
    pos=pos,
    with_labels=True,
    node_color="lightblue",
    ax=axes[1, 0]
)
axes[1, 0].set_title(f"Betweenness\nRemoved: {removed_between}\nConnectivity: {connectivity(G_between)}")

nx.draw(
    G_exhaustive,
    pos=pos,
    with_labels=True,
    node_color="lightblue",
    ax=axes[1, 1]
)
axes[1, 1].set_title(f"Exhaustive\nRemoved: {removed_exhaustive}\nConnectivity: {connectivity(G_exhaustive)}")

plt.show()