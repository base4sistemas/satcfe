.PHONY: main clean test testfnall

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

testallfn: | clean
	@python setup.py test -a "--acessa-sat \
		--invoca-ativarsat \
		--invoca-comunicarcertificadoicpbrasil \
		--invoca-enviardadosvenda \
		--invoca-cancelarultimavenda \
		--invoca-consultarsat \
		--invoca-testefimafim \
		--invoca-consultarstatusoperacional \
		--invoca-consultarnumerosessao \
		--invoca-configurarinterfacederede \
		--invoca-associarassinatura \
		--invoca-atualizarsoftwaresat \
		--invoca-extrairlogs \
		--invoca-bloquearsat \
		--invoca-desbloquearsat \
		--invoca-trocarcodigodeativacao "

