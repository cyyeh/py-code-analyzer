import networkx as nx


class GraphAnalyzer:
    def __init__(self, is_directed: bool = False, is_multi_edges: bool = False):
        if not is_directed and not is_multi_edges:
            self.graph = nx.Graph()
        elif is_directed and not is_multi_edges:
            self.graph = nx.DiGraph()
        elif not is_directed and is_multi_edges:
            self.graph = nx.MultiGraph()
        else:
            self.graph = nx.MultiDiGraph()

    def add_node(self, node, **kwargs):
        self.graph.add_node(node, **kwargs)

    def add_edge(self, first_node, second_node):
        self.graph.add_edge(first_node, second_node)
