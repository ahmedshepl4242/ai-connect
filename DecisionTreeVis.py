import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from DecisionTree import DecisionTree  # Import your decision tree implementation
from Node import Node
from Heustric import HeuristicFunction

class DecisionTreeVisualizer:
    def __init__(self, tree):
        self.tree = tree

    def traverse_tree(self, node, graph, positions, labels, x=0, y=0, depth=5, x_offset=1.0):
        """
        Recursively traverse the decision tree and populate the graph for visualization.
        """
        if not node or depth < 0:
            return

        node_id = id(node)
        
        # Add the current node to the graph
        graph.add_node(node_id)
        positions[node_id] = (x, y)
        labels[node_id] = f"{node.score}\n{node.move}"

        # Traverse children if they exist
        if node.children:
            child_offset = x_offset / 1.5
            for i, child in enumerate(node.children):
                child_x = x - x_offset + i * (2 * x_offset / len(node.children))
                child_y = y - 1

                # Add child to graph and traverse
                graph.add_edge(node_id, id(child))
                self.traverse_tree(child, graph, positions, labels, child_x, child_y, depth - 1, child_offset)

    def visualize_tree(self):
        """
        Visualize the decision tree using NetworkX and Matplotlib.
        """
        graph = nx.DiGraph()
        positions = {}
        labels = {}

        # Traverse the tree starting from the root
        self.traverse_tree(self.tree.root, graph, positions, labels, depth=5)

        # Check for consistency: Ensure all nodes have positions
        missing_positions = set(graph.nodes) - set(positions.keys())
        if missing_positions:
            raise ValueError(f"Missing positions for nodes: {missing_positions}")

        # Draw the graph
        plt.figure(figsize=(12, 8))
        ax = plt.gca()
        nx.draw(
            graph,
            pos=positions,
            with_labels=True,
            labels=labels,
            node_size=2000,
            node_color="lightblue",
            font_size=10,
            ax=ax
        )
        plt.show()

# Example Usage
if __name__ == "__main__":
   
    initial_board = [[0] * 7 for _ in range(6)]  # Empty board

    heuristic_function= HeuristicFunction()
    tree = DecisionTree(initial_board,"aggressive",heuristic_function)
    tree.generate_tree(tree.root, depth=4, is_maximizing=True)


    visualizer = DecisionTreeVisualizer(tree)
    visualizer.visualize_tree()
