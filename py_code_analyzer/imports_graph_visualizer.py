"""This file generates a pyvis graph locally given a networkx graph
"""
import networkx as nx

from pyvis import Network


class ImportsGraphVisualizer:
    @classmethod
    def visualize(
        cls,
        imports_graph: nx.Graph,
        directed: bool = True,
        layout: bool = False,  # Use hierarchical if True
        neighborhood_highlight: bool = True,
        select_menu: bool = True,
        width: int = 100,
        height: int = 800,
        show_buttons: bool = False,
        display_html_name: str = "nx.html",
    ):
        _pyvis_network = Network(
            width=f"{width}%",
            height=f"{height}px",
            directed=directed,
            layout=layout,
            neighborhood_highlight=neighborhood_highlight,
            select_menu=select_menu,
        )
        _pyvis_network.toggle_hide_edges_on_drag(True)

        _pyvis_network.from_nx(imports_graph)
        if show_buttons:
            _pyvis_network.show_buttons()
        _pyvis_network.show(display_html_name)
