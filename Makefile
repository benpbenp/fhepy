lint:
	find . -iname "*.py" | xargs pylint

test:
	py.test
