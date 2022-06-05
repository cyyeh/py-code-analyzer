"""CodeFetcher deals with every detail of
how to get all python files in the given directory
"""
import os

import requests

# to increase api rate limiting
# https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting
USER = os.environ.get("USER", "")
PERSONAL_ACCESS_TOKEN = os.environ.get("PERSONAL_ACCESS_TOKEN", "")


class CodeFetcher:
    @classmethod
    def get_python_files(
        cls,
        owner: str,
        repo: str,
        path: str = "",
        ref: str = "",
        recursive: bool = True,
    ):
        """https://docs.github.com/en/rest/repos/contents#get-repository-content"""

        api_url = (
            f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
            if not USER or not PERSONAL_ACCESS_TOKEN
            else f"https://{USER}:{PERSONAL_ACCESS_TOKEN}@api.github.com/repos/{owner}/{repo}/contents/{path}"
        )
        if ref:
            api_url += f"?ref={ref}"

        python_files = []
        api_results = requests.get(
            api_url, headers={"Accept": "application/vnd.github.v3+json"}
        ).json()

        for result in api_results:
            if type(result) is dict:
                if result["type"] == "file" and result["name"].endswith(".py"):
                    python_files.append(result)
                elif (
                    recursive
                    and result["type"] == "dir"
                    and not result["name"].startswith(".")
                ):
                    python_files += cls.get_python_files(
                        owner, repo, path=result["path"], recursive=recursive
                    )

        return python_files
