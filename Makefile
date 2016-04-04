lint:
	find bin pry tests | xargs flake8

test:
	nosetests
