run:
	pipenv run streamlit run app.py

format:
	pipenv run black py_code_analyzer app.py && \
	pipenv run isort py_code_analyzer app.py && \
	pipenv run flake8 py_code_analyzer app.py && \
	pipenv run mypy py_code_analyzer app.py

test:
	pipenv run pytest --cov
