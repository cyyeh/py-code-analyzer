"""GraphAnalyzer uses some open source graph library for network analysis
"""
import networkx as nx


class GraphAnalyzer:
    def __init__(self, is_directed: bool = False):
        self.graph = nx.DiGraph() if is_directed else nx.Graph()

    def add_node(self, node, **kwargs):
        self.graph.add_node(node, **kwargs)

    def add_edge(self, first_node, second_node):
        self.graph.add_edge(first_node, second_node)

    def add_edges_from_nodes(self, nodes):
        assert len(nodes) > 1
        for first_node, second_node in zip(nodes, nodes[1:]):
            self.add_node(first_node, color="gray")  # set default node color
            self.add_node(second_node, color="gray")  # set default node color
            self.add_edge(first_node, second_node)
