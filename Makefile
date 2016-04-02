lint:
	find call_graph tests -name '*.py' | xargs flake8
