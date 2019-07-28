test:
	pip install -r tests/test_requirements.txt && pip install -e . && python3 -m pytest -v -W ignore::DeprecationWarning