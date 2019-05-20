.PHONY: main clean test

main:
	@echo "Makefile do projeto SATCFe para Python"

clean:
	@find . -type d -name '__pycache__' -exec rm -rv {} +
	@find . -type d -name '.cache' -exec rm -rv {} +
	@find . -type d -name '.pytest_cache' -exec rm -rv {} +
	@find . -type d -name 'satcfe.egg-info' -exec rm -rv {} +
	@find . -name '*.pyc' -delete -print

test: | clean
	@python setup.py test
