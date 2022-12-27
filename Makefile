run:
	pipenv run python -m manage runserver

migrate:
	pipenv run python -m manage makemigrations
	pipenv run python -m manage migrate

test:
	# Ref: https://stackoverflow.com/a/42862546/8749888 -- config for running in parallel
	pipenv run python -m coverage run -m manage test --noinput --verbosity 2
	pipenv run python -m coverage report

format:
	pipenv run isort .
	pipenv run black .

lint:
	pipenv run pylint ./luvio_api --fail-under=9
	pipenv run mypy luvio_api/