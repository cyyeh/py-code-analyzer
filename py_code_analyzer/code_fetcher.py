"""This file deals with every detail of how to get all python files in the given directory
"""
import requests


def get_repository_python_files(owner: str, repo: str, path: str = "", ref: str = ""):
    """https://docs.github.com/en/rest/repos/contents#get-repository-content"""
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    if ref:
        api_url += f"?ref={ref}"

    python_files = []
    api_results = requests.get(api_url).json()

    for result in api_results:
        if result["type"] == "file" and result["name"].endswith(".py"):
            python_files.append(result)

    return python_files
