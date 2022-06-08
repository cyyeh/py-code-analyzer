"""CodeFetcher deals with every detail of
how to get all python files in the given directory
"""
import requests


def construct_fetch_repo_content_api_url(owner, repo, tree_sha, recursive):
    import os

    # to increase api rate limiting
    # https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting
    USER = os.environ.get("USER", "")
    PERSONAL_ACCESS_TOKEN = os.environ.get("PERSONAL_ACCESS_TOKEN", "")

    api_url = f"api.github.com/repos/{owner}/{repo}/git/trees/{tree_sha}"
    if USER and PERSONAL_ACCESS_TOKEN:
        api_url = f"{USER}:{PERSONAL_ACCESS_TOKEN}@{api_url}"
    if recursive:
        api_url += "?recursive=1"

    return "https://" + api_url


class CodeFetcher:
    @classmethod
    def get_python_files(
        cls,
        owner: str,
        repo: str,
        tree_sha: str,
        recursive: bool = True,
    ):
        """https://docs.github.com/en/rest/git/trees#get-a-tree"""
        # TODO: deal with truncated api results

        api_url = construct_fetch_repo_content_api_url(owner, repo, tree_sha, recursive)

        response = requests.get(
            api_url, headers={"Accept": "application/vnd.github.v3+json"}
        )

        api_results = response.json()
        if response.status_code == requests.codes.ok:
            python_files = [
                result
                for result in api_results["tree"]
                if type(result) is dict
                and result["type"] == "blob"
                and result["path"].endswith(".py")
            ]
            return python_files
        else:
            print(api_results)

        return []
