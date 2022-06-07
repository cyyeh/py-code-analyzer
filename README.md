---
title: Py Code Analyzer
emoji: 📈
colorFrom: red
colorTo: yellow
sdk: streamlit
sdk_version: 1.9.0
app_file: app.py
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces#reference

# Python Code Analyzer

## Motivation

The main purpose of the app is to allow Python developers navigate Python code base much easier by showing dependencies
among files included in the directory with better visualization.

## Setup

- Python version: 3.8
- `pipenv install`
- `cp .env.example .env`: fill in your GitHub username and personal access token if you need to increase [GitHub API requests rate limiting](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- `make run`
- Also refer to References to understand settings behind the project

## Thoughts on solving the problem

1. Build a prototype without UI interface to show dependencies among files included in the directory(output) given user's
input to one GitHub public repo's URL(input)
2. Build a `streamlit` app to show results using some network visualization tools

## Used technologies

- `networkx`: network analysis
- `pyvis`: network visualization
- `streamlit`: web app

## TODOs

- [x] Build a prototype
  - [x] Finish `generate_imports_graph` implementation
  - [x] Fetch python files given public GitHub repo url(owner, repo, path, ref)
  - [x] Use `ast` to parse imports among given python files
  - [x] Generate a basic `networkx` graph given python imports
  - [x] Visualize a basic `networkx` graph using `pyvis`
- [x] Build a `streamlit` app
- [ ] Performance optimization
  - [x] `requests` to `aiohttp`: reduce latency 8-10x in my laptop(MacBook Pro)
## References

- [How to set up a perfect Python project](https://sourcery.ai/blog/python-best-practices/)
- [Benchmark of popular graph/network packages](https://www.timlrx.com/blog/benchmark-of-popular-graph-network-packages)