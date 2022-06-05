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
    "Enter target directory path. Default: the target directory will be the root directory",
    value="py_code_analyzer",
)
ref = st.text_input(
    "Enter the name of the commit/branch/tag. Default: the repository's default branch",
)
clicked_ok_button = st.button("OK")
st.markdown("---")


def get_python_files(owner, repo, path, ref=""):
    return CodeFetcher().get_python_files(owner, repo, path, ref=ref)


def generate_imports_graph(python_files):
    return CodeImportsAnalyzer(python_files).analyze().generate_imports_graph()


def generate_graph_visualization_file(imports_graph):
    ImportsGraphVisualizer().visualize(imports_graph)


def read_graph_visualization_file():
    return open("nx.html", "r", encoding="utf-8").read()


if clicked_ok_button and owner and repo:
    with st.spinner("Getting python files..."):
        python_files = get_python_files(owner, repo, path, ref=ref)

    with st.spinner("Generating imports graph..."):
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
