import networkx as nx
import matplotlib.pyplot as plt

edge_list = [(1, 2), (1, 3), (2, 3),(4, 5), (4, 6), (6, 5), (7, 3), (7, 4), (7, 8), (8, 9), (8, 10), (9, 10)]


G = nx.from_edgelist(edge_list)


pos = nx.spring_layout(G)

node_colors = ["red" if node == 7 else "lightblue" for node in G.nodes()]

plt.title("Node 7 High Betweenness Centrality")
nx.draw_spring (G, with_labels=True, node_color=node_colors)


plt.show()

#centrality = nx.degree_centrality(G)

#print("Degree Centrality:")
#for node, value in centrality.items():
#    print(node, ":", f"{value:10.2f}")

#critical_node = max(centrality, key=centrality.get)

#print("Node selected by greedy algorithm:", critical_node) 

#node_color =['red' if node == critical_node else 'lightblue' for node in G.nodes()]

#nx.draw_spring (G, with_labels=True, node_color=node_color)

#plt.title("Greedy Selection: Most Important Node Highlighted")
#plt.show()

#G.remove_node(critical_node)

#nx.draw_spring (G, with_labels=True, node_color="lightblue")

#plt.title("Graph After Removing Critical Node")
#plt.show()

