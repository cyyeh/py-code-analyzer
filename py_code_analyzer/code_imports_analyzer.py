"""CodeImportsAnalyzer uses the ast module from Python's standard library
to get what modules are imported in given python files, then uses networkx to generate imports graph
"""
import ast
from pprint import pprint

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
        self.imports = []
        self.imports_graph = nx.DiGraph()  # imports_graph is a directed graph
        self.python_files = python_files
        self._node_visitor = CodeImportsAnalyzer._NodeVisitor(self.imports)

    def analyze(self):
        for python_file in self.python_files:
            program = requests.get(python_file["download_url"]).text
            tree = ast.parse(program)
            self.imports += [
                {
                    "file_name": python_file["name"],
                    "file_path": python_file["path"],
                    "imports": [],
                }
            ]
            self._node_visitor.visit(tree)
        return self

    def generate_imports_graph(self):
        for _import in self.imports:
            _nodes = _import["file_path"].split("/")
            if len(_nodes):
                if len(_nodes) > 1:
                    for first_node, second_node in zip(_nodes, _nodes[1:]):
                        self.imports_graph.add_edge(first_node, second_node)
                else:
                    self.imports_graph.add_node(_nodes[0])

        return self.imports_graph

    def report(self):
        pprint(self.imports)
