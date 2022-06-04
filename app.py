import streamlit as st
import streamlit.components.v1 as components

from py_code_analyzer import CodeFetcher, CodeImportsAnalyzer, ImportsGraphVisualizer

TITLE = "Python Code Analyzer"
st.set_page_config(page_title=TITLE, layout="wide")
st.title(TITLE)
st.markdown(
    "The main purpose of the app is to allow Python developers navigate Python code base much "
    + "easier by showing dependencies among files included in the directory with better visualization."
)
st.markdown(
    "**Checkout the source code [here](https://github.com/cyyeh/py-code-analyzer)**"
)

owner = st.text_input("Enter GitHub username", value="cyyeh")
repo = st.text_input("Enter GitHib repo name", value="py-code-analyzer")
path = st.text_input(
    "Enter target directory path, if the value is empty, then the target directory will be the root directory",
    value="py_code_analyzer",
)

python_files = CodeFetcher().get_python_files(owner, repo, path)
imports_graph = CodeImportsAnalyzer(python_files).analyze().generate_imports_graph()
ImportsGraphVisualizer().visualize(imports_graph)

imports_graph_html = open("nx.html", "r", encoding="utf-8")
imports_graph_html_text = imports_graph_html.read()
components.html(imports_graph_html_text, height=800)
