run:
	./ops/retrieve_secrets.sh
	pipenv run python -m manage runserver

migrate:
	pipenv run python -m manage makemigrations
	pipenv run python -m manage migrate

test:
	# Ref: https://stackoverflow.com/a/42862546/8749888 -- config for running in parallel
	pipenv run python -m coverage run --concurrency=multiprocessing -m manage test --noinput --verbosity 2 --parallel
	pipenv run python -m coverage combine
	pipenv run python -m coverage report --show-missing --fail-under=90

format:
	pipenv run isort .
	pipenv run black .

lint:
	pipenv run pylint ./luvio_api --fail-under=9
	pipenv run mypy luvio_api/