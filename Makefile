lint:
	find . -iname "*.py" | xargs pylint

test:
	py.test

fix:
	autopep8 --in-place -r . && isort -rc .
