import networkx as nx
import matplotlib.pyplot as plt

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

sorted_nodes = sorted(bc, key=bc.get, reverse=True)
critical_nodes = sorted_nodes[:k]

print("Betweenness Centrality:")
for node, value in bc.items():
    print(node, ":", f"{value:.2f}")
print("\nNodes selected for removal:", critical_nodes)

before = nx.number_connected_components(G)
print("Connected components BEFORE:", before)

node_colors = ["red" if node in critical_nodes else "lightblue" for node in G.nodes()]

nx.draw(G, pos=pos, with_labels=True, node_color=node_colors, ax=axes[0,1])
axes[0,1].set_title("Nodes with Highest Betweenness Centrality")
#plt.show()

G_removed = G.copy()
G_removed.remove_nodes_from(critical_nodes)

after = nx.number_connected_components(G_removed)
print("Connected components AFTER:", after)

nx.draw(G_removed, pos=pos, with_labels=True, node_color="lightblue", ax=axes[1,0])
axes[1,0].set_title("Graph After Removing Critical Nodes")
axes[1,1].axis("off")
plt.show()