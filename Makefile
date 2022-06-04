run:
	pipenv run python app.py

format:
	pipenv run black py_code_analyzer && \
	pipenv run isort py_code_analyzer && \
	pipenv run flake8 && \
	pipenv run mypy

test:
	pipenv run pytest --cov
