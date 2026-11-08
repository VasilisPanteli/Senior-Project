import networkx as nx
import matplotlib.pyplot as plt

edge_list = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5), (2, 5), (2, 6), (4, 7), (5, 6), (5, 7), (1, 8), (1, 9), (8, 9), (3, 10)]

G = nx.from_edgelist(edge_list)

n = G.number_of_nodes()
print("Total nodes in graph:", n)

pos = nx.spring_layout(G, seed=45)

fig, axes = plt.subplots(2, 2, figsize=(10, 10))

# Plot 1: Original Graph
nx.draw(G, pos=pos, with_labels=True, node_color="lightblue", ax=axes[0,0])
axes[0,0].set_title("Original Graph")

# Compute Maximal Independent Set
I = nx.maximal_independent_set(G)
print("Maximal Independent Set I:", I)
print("Size of I:", len(I))

# Plot 2: MIS (green) BEFORE removal
node_color_mis = ['green' if node in I else 'lightblue' for node in G.nodes()]
nx.draw(G, pos=pos, with_labels=True, node_color=node_color_mis, ax=axes[0,1])
axes[0,1].set_title("Maximal Independent Set (Green Nodes)")

k = 3  # number of nodes to remove
non_I_nodes = [node for node in G.nodes() if node not in I]
print("Nodes outside I:", non_I_nodes)

if k > len(non_I_nodes):
    print("Error: k is too large. Not enough nodes outside the independent set.")
else:
    centrality = nx.degree_centrality(G)
    sorted_nodes = sorted(non_I_nodes, key=lambda x: centrality[x], reverse=True)
    nodes_to_remove = sorted_nodes[:k]
    print("Nodes selected for removal:", nodes_to_remove)

    # Plot 3: Show nodes to remove in RED + MIS in GREEN (BEFORE removal)
    node_color_remove = ["red" if node in nodes_to_remove else "green" if node in I else "lightblue" for node in G.nodes()]
    nx.draw(G, pos=pos, with_labels=True, node_color=node_color_remove, ax=axes[1,0])
    axes[1,0].set_title(f"Nodes to be Removed (Red) and MIS (Green)")

    # Actually remove the nodes
    G.remove_nodes_from(nodes_to_remove)

    # Plot 4: Final graph after removal (MIS in green, others lightblue, removed nodes gone)
    node_color_final = ["green" if node in I else "lightblue" for node in G.nodes()]
    nx.draw(G, pos=pos, with_labels=True, node_color=node_color_final, ax=axes[1,1])
    axes[1,1].set_title(f"Final Graph")

    plt.show()