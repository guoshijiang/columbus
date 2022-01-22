.DEFAULT_GOAL := help

all: help


format:
	black -l 82  --skip-magic-trailing-comma --target-version py39 .
	find . -name "*.py" -exec isort --py 39 --force-grid-wrap --multi-line VERTICAL_PREFIX_FROM_MODULE_IMPORT {} +

format_models:
	find . | grep models | grep -v pyc | xargs black -l 50

check::
	python manage.py check
