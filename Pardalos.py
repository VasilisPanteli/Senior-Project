import networkx as nx
import matplotlib.pyplot as plt

edge_list = [(1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5), (2, 5), (2, 6), (4, 7), (5, 6), (5, 7), (1, 8), (1, 9), (8, 9), (3, 10)]

G = nx.from_edgelist(edge_list)

n = G.number_of_nodes()
k = 3
print("Total nodes in graph:", n)

pos = nx.spring_layout(G, seed=45)

fig, axes = plt.subplots(2, 2, figsize=(10, 10))

# Plot 1: Original Graph
nx.draw(G, pos=pos, with_labels=True, node_color="lightblue", ax=axes[0,0])
axes[0,0].set_title("Original Graph")

# Compute Maximal Independent Set
MIS = nx.maximal_independent_set(G)
print("Maximal Independent Set:", MIS)

# Plot 2: MIS in GREEN
node_color_mis = ['green' if node in MIS else 'lightblue' for node in G.nodes()]
nx.draw(G, pos=pos, with_labels=True, node_color=node_color_mis, ax=axes[0,1])
axes[0,1].set_title("Maximal Independent Set (GREEN)")

# Store the nodes that will be removed (nodes NOT in MIS)
removed_nodes = [node for node in G.nodes() if node not in MIS]

# Plot 3: Show nodes to remove in RED before removal
node_color_remove = ['red' if node in removed_nodes else 'green' if node in MIS else 'lightblue' for node in G.nodes()]
nx.draw(G, pos=pos, with_labels=True, node_color=node_color_remove, ax=axes[1,0])
axes[1,0].set_title("Nodes to Remove (RED) and MIS (GREEN)")

# Now run Pardalo's algorithm
current_nodes = set(MIS)
remaining_nodes = [node for node in G.nodes() if node not in MIS]
H = G.subgraph(current_nodes).copy()

def largest_component_size(graph):
    if len(graph.nodes()) == 0:
        return 0
    return len(max(nx.connected_components(graph), key=len))

target_size = n - k
added_nodes = []

while H.number_of_nodes() < target_size:
    best_node = None
    best_score = float('inf')

    for node in remaining_nodes:
        temp_graph = H.copy()
        temp_graph.add_node(node)
        for neighbor in G.neighbors(node):
            if neighbor in temp_graph:
                temp_graph.add_edge(node, neighbor)
        score = largest_component_size(temp_graph)
        if score < best_score:
            best_score = score
            best_node = node

    H.add_node(best_node)
    for neighbor in G.neighbors(best_node):
        if neighbor in H:
            H.add_edge(best_node, neighbor)

    added_nodes.append(best_node)
    remaining_nodes.remove(best_node)
    print("Added nodes:", added_nodes)

# Plot 4: Final graph (MIS = GREEN, Added back = ORANGE, Removed = gone)
node_colors_final = []
for node in H.nodes():
    if node in MIS:
        node_colors_final.append("green")
    elif node in added_nodes:
        node_colors_final.append("orange")
    else:
        node_colors_final.append("lightblue")

nx.draw(H, pos=pos, with_labels=True, node_color=node_colors_final, ax=axes[1,1])
axes[1,1].set_title("Final Graph (Green=MIS, Orange=Added Back)")

plt.tight_layout()
plt.show()