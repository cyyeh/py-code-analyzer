import networkx as nx
from pyvis.network import Network


class ImportsGraphVisualizer:
    @classmethod
    def visualize(
        cls,
        imports_graph: nx.Graph,
        width: int = 100,
        height: int = 100,
        display_html_name: str = "nx.html",
    ):
        _pyvis_network = Network(f"{width}%", f"{height}%")
        _pyvis_network.from_nx(imports_graph)
        _pyvis_network.show(display_html_name)
