lint:
	find bin call_graph tests | xargs flake8

test:
	nosetests
