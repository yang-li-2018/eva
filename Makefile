all:
	@python3 setup.py build
release:
	@python3 setup.py sdist
clean:
	@rm -rf build/ dist/ pyeva.egg-info/
