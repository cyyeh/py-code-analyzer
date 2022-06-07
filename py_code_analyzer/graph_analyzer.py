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
