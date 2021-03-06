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

- `pipenv install -r requirements.txt --python=3.8`
- `cp .env.example .env`: fill in your GitHub username and personal access token if you need to increase [GitHub API requests rate limiting](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- `make run`

## Used technologies

- `networkx`: network analysis
- `pyvis`: network visualization
- `aiohttp`: asynchronous HTTP client
- `pybase64`: faster base64 encoding/decoding
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
  - [x] `requests` to `aiohttp`
  - [x] change fetching GitHub repository content api from preventing querying multiple times
  - [ ] ...
- [ ] Network analysis
- [ ] Enhance network visualization UI
## References

- [How to set up a perfect Python project](https://sourcery.ai/blog/python-best-practices/)
- [Benchmark of popular graph/network packages](https://www.timlrx.com/blog/benchmark-of-popular-graph-network-packages)
- [Asynchronous HTTP Requests in Python with aiohttp and asyncio](https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp)