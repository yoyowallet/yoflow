build: clean virtualenv database

clean:
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*,cover" -delete

clean_migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete

virtualenv:
	pip install -r requirements.txt

database:
	createdb yoflow
	./manage.py migrate

static_analysis: pep8 xenon

pep8:
	@echo "Running flake8 over codebase"
	flake8 --ignore=E501,W391,F999 --exclude=migrations yoflow/

xenon:
	@echo "Running xenon over codebase"
	xenon --max-absolute B --max-modules B --max-average A --exclude test_*.py yoflow/\

test: static_analysis
	tox $(pytest_args)

.PHONY: clean clean_migrations virtualenv database static_analysis pep8 xenon test