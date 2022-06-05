"""CodeImportsAnalyzer uses the ast module from Python's standard library
to get what modules are imported in given python files, then uses networkx to generate imports graph
"""
import ast

import networkx as nx
import requests


class CodeImportsAnalyzer:
    class _NodeVisitor(ast.NodeVisitor):
        def __init__(self, imports):
            self.imports = imports

        def visit_Import(self, node):
            for alias in node.names:
                self.imports[-1]["imports"].append(
                    {"module": None, "name": alias.name, "level": -1}
                )
            self.generic_visit(node)

        def visit_ImportFrom(self, node):
            for alias in node.names:
                self.imports[-1]["imports"].append(
                    {"module": node.module, "name": alias.name, "level": node.level}
                )
            self.generic_visit(node)

    def __init__(self, python_files):
        self.python_imports = []
        self.imports_graph = nx.DiGraph()  # imports_graph is a directed graph
        self.python_files = python_files
        self._node_visitor = CodeImportsAnalyzer._NodeVisitor(self.python_imports)

    def analyze(self):
        for python_file in self.python_files:
            program = requests.get(python_file["download_url"]).text
            tree = ast.parse(program)
            self.python_imports += [
                {
                    "file_name": python_file["name"],
                    "file_path": python_file["path"],
                    "imports": [],
                }
            ]
            self._node_visitor.visit(tree)
        return self

    def _add_edges(self, nodes):
        for first_node, second_node in zip(nodes, nodes[1:]):
            self.imports_graph.add_node(first_node, color="gray")
            self.imports_graph.add_node(second_node, color="gray")
            self.imports_graph.add_edge(first_node, second_node)

    def generate_imports_graph(self):
        for python_import in self.python_imports:
            _nodes = python_import["file_path"].split("/")
            if len(_nodes):
                # generate graph based on file_path
                # node/edge relationship means file/folder structure
                if len(_nodes) > 1:
                    # make last node and second last node as one node
                    # to solve the issue of duplicated file names using only last node
                    if len(_nodes) >= 3:
                        _nodes[-2] = _nodes[-2] + "/" + _nodes[-1]
                        del _nodes[-1]
                    self._add_edges(_nodes)
                else:
                    self.imports_graph.add_node(_nodes[0])

                # generate graph based on imported modules in each file
                if python_import["file_name"] != "__init__.py":
                    for _import in python_import["imports"]:
                        if _import["module"] is None:
                            _import_names = _import["name"].split(".")
                            _new_nodes = _import_names + [_nodes[-1]]
                            self._add_edges(_new_nodes)
                        else:
                            _import_names = _import["module"].split(".") + [
                                _import["name"]
                            ]
                            _new_nodes = _import_names + [_nodes[-1]]
                            self._add_edges(_new_nodes)

        return self.imports_graph

    def report(self):
        from pprint import pprint

        pprint(self.python_imports)
