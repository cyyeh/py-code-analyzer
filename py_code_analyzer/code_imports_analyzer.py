"""CodeImportsAnalyzer uses the ast module from Python's standard library
to get what modules are imported in given python files, then uses networkx to generate imports graph
"""
import ast
import asyncio

import aiohttp
import pybase64

from .graph_analyzer import GraphAnalyzer


def construct_fetch_program_text_api_url(api_url):
    import os

    # to increase api rate limiting
    # https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting
    USER = os.environ.get("USER", "")
    PERSONAL_ACCESS_TOKEN = os.environ.get("PERSONAL_ACCESS_TOKEN", "")

    if USER and PERSONAL_ACCESS_TOKEN:
        protocol, api_url_components = api_url.split("://")
        new_api_url_components = f"{USER}:{PERSONAL_ACCESS_TOKEN}@{api_url_components}"
        return f"{protocol}://{new_api_url_components}"
    else:
        return api_url


async def get_program_text(session, python_file):
    # about Retry-After
    # https://docs.github.com/en/rest/guides/best-practices-for-integrators#dealing-with-secondary-rate-limits
    async with session.get(
        construct_fetch_program_text_api_url(python_file["url"]),
        headers={"Accept": "application/vnd.github.v3+json", "Retry-After": "5"},
    ) as response:
        if response.status == 200:
            data = await response.json()
            if data["encoding"] == "base64":
                return data["content"], python_file["path"]
            else:
                print(
                    f"WARNING: {python_file['path']}'s encoding is {data['encoding']}, not base64"
                )


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

    async def parse_python_files(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for python_file in self.python_files:
                tasks.append(
                    asyncio.ensure_future(get_program_text(session, python_file))
                )

            results = await asyncio.gather(*tasks)
            if results:
                for base64_program_text, python_file_path in results:
                    if base64_program_text:
                        self.python_imports += [
                            {
                                "file_name": python_file_path.split("/")[-1],
                                "file_path": python_file_path,
                                "imports": [],
                            }
                        ]
                        program = pybase64.b64decode(base64_program_text)
                        tree = ast.parse(program)
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
