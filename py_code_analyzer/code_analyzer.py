import ast
from pprint import pprint

import requests


class CodeAnalyzer:
    class NodeVisitor(ast.NodeVisitor):
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
        self.python_files = python_files
        self._node_visitor = CodeAnalyzer.NodeVisitor(self.imports)

    def analyze_imports(self):
        for python_file in self.python_files:
            program = requests.get(python_file["download_url"]).text
            tree = ast.parse(program)
            self.imports += [{"file_name": python_file["name"], "imports": []}]
            self._node_visitor.visit(tree)

    def report_imports(self):
        pprint(self.imports)
