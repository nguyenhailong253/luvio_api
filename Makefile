run:
	pipenv run python -m manage runserver

migrate:
	pipenv run python -m manage makemigrations
	pipenv run python -m manage migrate

test:
	pipenv run python -m manage test --noinput --verbosity 2

format:
	pipenv run isort .
	