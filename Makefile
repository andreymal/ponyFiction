.PHONY: clean-pyc clean-build clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf '*.egg-info'

clean-pyc:
	find ponyFiction -name '*.py[cod]' -type f -delete
	find ponyFiction -name '__pycache__' -type d -delete

release: clean
	python3 setup.py sdist upload
	python3 setup.py bdist_wheel upload

dist: clean
	python3 setup.py sdist
	python3 setup.py bdist_wheel
	ls -l dist

install: clean
	python3 setup.py install