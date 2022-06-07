"""CodeImportsAnalyzer uses the ast module from Python's standard library
to get what modules are imported in given python files, then uses networkx to generate imports graph
"""
import ast

import aiohttp

from .graph_analyzer import GraphAnalyzer


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
        self.graph_analyzer = GraphAnalyzer(is_directed=True)
        self.python_files = python_files
        self._node_visitor = CodeImportsAnalyzer._NodeVisitor(self.python_imports)

    async def analyze(self):
        async with aiohttp.ClientSession() as session:
            for python_file in self.python_files:
                async with session.get(
                    python_file["download_url"],
                    headers={"Accept": "application/vnd.github.v3+json"},
                ) as response:
                    program = await response.text()
                    tree = ast.parse(program)
                    self.python_imports += [
                        {
                            "file_name": python_file["name"],
                            "file_path": python_file["path"],
                            "imports": [],
                        }
                    ]
                    self._node_visitor.visit(tree)

    def generate_imports_graph(self):
        # TODO: thought on how to improve the graph generation logic
        # generate a dictionary of lists data structure
        # generate a graph based on a dictionary of lists

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
                    self.graph_analyzer.add_edges_from_nodes(_nodes)
                else:
                    self.graph_analyzer.add_node(_nodes[0])

                # generate graph based on imported modules in each file
                if python_import["file_name"] != "__init__.py":
                    for _import in python_import["imports"]:
                        if _import["module"] is None:
                            _import_names = _import["name"].split(".")
                            _new_nodes = _import_names + [_nodes[-1]]
                            self.graph_analyzer.add_edges_from_nodes(_new_nodes)
                        else:
                            _import_names = _import["module"].split(".") + [
                                _import["name"]
                            ]
                            _new_nodes = _import_names + [_nodes[-1]]
                            self.graph_analyzer.add_edges_from_nodes(_new_nodes)

        return self.graph_analyzer.graph

    def report(self):
        from pprint import pprint

        pprint(self.python_imports)
