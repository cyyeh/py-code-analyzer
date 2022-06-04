from py_code_analyzer import CodeFetcher, CodeImportsAnalyzer, ImportsGraphVisualizer

python_files = CodeFetcher().get_python_files(
    "cyyeh", "py-code-analyzer", "py_code_analyzer"
)
imports_graph = CodeImportsAnalyzer(python_files).analyze().generate_imports_graph()
ImportsGraphVisualizer().visualize(imports_graph)
