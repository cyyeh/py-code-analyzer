import asyncio
import os

import streamlit as st
import streamlit.components.v1 as components

from py_code_analyzer import CodeFetcher, CodeImportsAnalyzer, ImportsGraphVisualizer
from utils import conditonal_decorator, time_function

DEV = int(os.environ.get("DEV", "1"))

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
tree_sha = st.text_input(
    "Fill in SHA", value="2f387d0adea72a7b4c99a5e8fc3e4fd83b5469b8"
)
show_graph_visualization = st.checkbox(
    "Show graph visualization",
    value=True,
    help="If the graph is large, then consider uncheck the checkbox. "
    "For example, the result graph of fetching TensorFlow repo would be large.",
)
clicked_ok_button = st.button("OK", disabled=not owner or not repo or not tree_sha)
st.markdown("---")


@st.cache
@conditonal_decorator(time_function, DEV)
def get_python_files(owner, repo, tree_sha):
    return CodeFetcher().get_python_files(owner, repo, tree_sha)


@conditonal_decorator(time_function, DEV)
def parse_python_files(analyzer):
    asyncio.run(analyzer.analyze())


@conditonal_decorator(time_function, DEV)
def generate_imports_graph(analyzer):
    return analyzer.generate_imports_graph()


@conditonal_decorator(time_function, DEV)
def generate_graph_visualization_file(imports_graph, heading):
    ImportsGraphVisualizer().visualize(imports_graph, heading=heading)


@conditonal_decorator(time_function, DEV)
def read_graph_visualization_file():
    return open("nx.html", "r", encoding="utf-8").read()


if clicked_ok_button and owner and repo:
    with st.spinner("Getting python files..."):
        python_files = get_python_files(owner, repo, tree_sha)

    analyzer = CodeImportsAnalyzer(python_files)
    with st.spinner("Parsing python files..."):
        parse_python_files(analyzer)

    with st.spinner("Generating imports graph..."):
        imports_graph = generate_imports_graph(analyzer)

    with st.spinner("Generating graph visualization file..."):
        generate_graph_visualization_file(imports_graph, f"{owner}/{repo}")

    with st.spinner("Showing the graph..."):
        graph_visualization_file = read_graph_visualization_file()
        st.download_button(
            "Download the result file",
            graph_visualization_file,
            file_name="result.html",
            mime="text/html",
        )
        if show_graph_visualization:
            components.html(graph_visualization_file, height=600, scrolling=True)
