from py_code_analyzer.code_fetcher import CodeFetcher
from py_code_analyzer.code_imports_analyzer import CodeImportsAnalyzer
from py_code_analyzer.imports_graph_visualizer import ImportsGraphVisualizer

python_files = CodeFetcher().get_python_files("cyyeh", "gradio", "gradio")
imports_graph = CodeImportsAnalyzer(python_files).analyze().generate_imports_graph()
ImportsGraphVisualizer().visualize(imports_graph)
