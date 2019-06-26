# -*- coding: utf-8 -*-
#
# satcfe/tests/test_atualizarsoftwaresat.py
#
# Copyright 2019 Base4 Sistemas Ltda ME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import pytest

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaSAT


def test_respostas_de_sucesso(datadir):
    with open(datadir.join('respostas-de-sucesso.txt'), 'r') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        resposta = RespostaSAT.atualizar_software_sat(retorno)
        assert resposta.EEEEE == '14000'  # único código que representa sucesso


def test_respostas_de_falha(datadir):
    with open(datadir.join('respostas-de-falha.txt'), 'r') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaSAT.atualizar_software_sat(retorno)


def test_respostas_invalidas(datadir):
    with open(datadir.join('respostas-invalidas.txt'), 'r') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaSAT.atualizar_software_sat(retorno)


@pytest.mark.acessa_sat
@pytest.mark.invoca_atualizarsoftwaresat
def test_funcao_ativarsat(request, clientesatlocal):
    # Este teste baseia-se na resposta da biblioteca SAT de simulação (mockup)
    # que é usada nos testes do projeto SATHub. Sempre atualiza com sucesso.
    #
    # Detalhes em: https://github.com/base4sistemas/sathub
    #
    resposta = clientesatlocal.atualizar_software_sat()
    assert resposta.EEEEE == '14000'