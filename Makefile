#
#  Makefile
#
#  Copyright 2019 Base4 Sistemas Ltda ME
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

.PHONY: main clean mockuplib test testall
.ONESHELL:

main:
	@echo "Makefile do projeto SATCFe para Python"

clean:
	find . -type d -name '__pycache__' -exec rm -rv {} +
	find . -type d -name '.cache' -exec rm -rv {} +
	find . -type d -name '.pytest_cache' -exec rm -rv {} +
	find . -type d -name 'satcfe.egg-info' -exec rm -rv {} +
	find . -name '*.pyc' -delete -print
	find . -name 'mockupsat.o' -delete -print
	find . -name 'libmockupsat.so' -delete -print

mockuplib: clean
	cd satcfe/tests/mockup/
	gcc -c -Wall -Werror -fpic mockupsat.c
	gcc -shared -o libmockupsat.so mockupsat.o

test: clean
	pipenv run python setup.py test

testall: clean mockuplib
	pipenv run python setup.py test -a "--acessa-sat \
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
