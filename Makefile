run:
	pipenv run python app.py

format:
	pipenv run black py_code_analyzer && \
	pipenv run isort py_code_analyzer && \
	pipenv run flake8 py_code_analyzer && \
	pipenv run mypy py_code_analyzer

test:
	pipenv run pytest --cov
