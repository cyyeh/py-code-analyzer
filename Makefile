format:
	pipenv run black py_code_analyzer && \
	pipenv run isort py_code_analyzer && \
	pipenv run mypy

test:
	pipenv run pytest --cov --cov-fail-under=100
