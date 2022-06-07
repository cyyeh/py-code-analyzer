import streamlit as st
import streamlit.components.v1 as components

from py_code_analyzer import CodeFetcher, CodeImportsAnalyzer, ImportsGraphVisualizer
from utils import time_function

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

owner = st.text_input("Fill in the GitHub username", value="cyyeh")
repo = st.text_input("Fill in the GitHib repository", value="py-code-analyzer")
path = st.text_input(
    "Fill in the target directory path. Default: the root directory",
)
ref = st.text_input(
    "Fill in the name of the commit/branch/tag. Default: the repository's default branch",
)
clicked_ok_button = st.button("OK")
st.markdown("---")


@time_function
def get_python_files(owner, repo, path, ref=""):
    return CodeFetcher().get_python_files(owner, repo, path, ref=ref)


@time_function
def generate_imports_graph(python_files):
    return CodeImportsAnalyzer(python_files).analyze().generate_imports_graph()


@time_function
def generate_graph_visualization_file(imports_graph):
    ImportsGraphVisualizer().visualize(imports_graph)


@time_function
def read_graph_visualization_file():
    return open("nx.html", "r", encoding="utf-8").read()


if clicked_ok_button and owner and repo:
    with st.spinner("Getting python files..."):
        python_files = get_python_files(owner, repo, path, ref=ref)

    with st.spinner("Parsing python files and generating imports graph..."):
        imports_graph = generate_imports_graph(python_files)

    with st.spinner("Generating graph visualization file..."):
        generate_graph_visualization_file(imports_graph)

    with st.spinner("Showing the graph..."):
        graph_visualization_file = read_graph_visualization_file()
        st.download_button(
            "Download the result file",
            graph_visualization_file,
            file_name="result.html",
            mime="text/html",
        )
        components.html(graph_visualization_file, height=600, scrolling=True)
