.PHONY: main clean test

main:
	@echo "Makefile do projeto SATCFe para Python"

clean:
	@find . -name '__pycache__' -delete -print \
		-o \
		-name '*.pyc' -delete -print

test: | clean
	@python setup.py test
