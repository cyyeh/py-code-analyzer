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


@st.cache
def get_python_files(owner, repo, path):
    return CodeFetcher().get_python_files(owner, repo, path)


@st.cache(allow_output_mutation=True)
def generate_imports_graph(python_files):
    return CodeImportsAnalyzer(python_files).analyze().generate_imports_graph()


@st.cache
def generate_graph_visualization_file(imports_graph):
    ImportsGraphVisualizer().visualize(imports_graph)


@st.cache
def read_graph_visualization_file():
    imports_graph_html = open("nx.html", "r", encoding="utf-8")
    return imports_graph_html.read()


if owner and repo:
    with st.spinner("Please wait..."):
        generate_graph_visualization_file(
            generate_imports_graph(get_python_files(owner, repo, path))
        )
        components.html(read_graph_visualization_file(), height=800)
