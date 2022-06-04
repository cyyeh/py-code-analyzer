from py_code_analyzer.code_analyzer import CodeAnalyzer
from py_code_analyzer.code_fetcher import get_repository_python_files

python_files = get_repository_python_files("cyyeh", "gradio")

code_analyzer = CodeAnalyzer(python_files)
code_analyzer.analyze_imports()
code_analyzer.report_imports()
