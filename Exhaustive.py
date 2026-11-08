import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

edge_list = [(1, 2), (1, 3), (2, 3), (3, 4), (3, 5), (2, 5), (5, 6), (5, 7)]


G = nx.from_edgelist(edge_list)

n = G.number_of_nodes()
print("Total nodes in graph:", n)

pos = nx.spring_layout(G, seed=45)

fig, axes = plt.subplots(2, 2, figsize=(10, 10))


nx.draw (G, pos=pos, with_labels=True, node_color="lightblue", ax=axes[0,0])
axes[0,0].set_title("Original Graph")
#plt.show()

bc = nx.betweenness_centrality(G)

k=2 

def largest_component_size(graph):
    if len(graph.nodes()) == 0:
        return 0
    return len(max(nx.connected_components(graph), key=len))

best_score = float('inf')
best_set = None

for nodes in combinations(G.nodes(), k):
    temp_graph = G.copy()
    temp_graph.remove_nodes_from(nodes)

    score = largest_component_size(temp_graph)

    if score < best_score:
        best_score = score
        best_set = nodes


if best_set is None:
    print("No solution found.")
    exit()

print("\nBest nodes to remove:", best_set)
print("Best score (smallest largest component):", best_score)

node_colors = ["red" if node in best_set else "lightblue" for node in G.nodes()]
nx.draw(G, pos=pos, with_labels=True, node_color=node_colors, ax=axes[0,1])
axes[0,1].set_title("Optimal Nodes (Red)")

G_final = G.copy()
G_final.remove_nodes_from(best_set)

nx.draw(G_final, pos=pos, with_labels=True, node_color="lightblue", ax=axes[1,0])
axes[1,0].set_title("Graph After Optimal Removal")

axes[1,1].axis("off")

plt.show()

