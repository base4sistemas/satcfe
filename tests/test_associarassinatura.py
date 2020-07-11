# -*- coding: utf-8 -*-
#
# tests/test_associarassinatura.py
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
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from io import open

from builtins import str as text

import pytest

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaAssociarAssinatura


def test_respostas_de_sucesso(datadir):
    arquivo = text(datadir.join('respostas-de-sucesso.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        resposta = RespostaAssociarAssinatura.analisar(retorno)
        assert resposta.EEEEE == '13000'  # único código que representa sucesso


def test_respostas_de_falha(datadir):
    arquivo = text(datadir.join('respostas-de-falha.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaAssociarAssinatura.analisar(retorno)


def test_respostas_invalidas(datadir):
    arquivo = text(datadir.join('respostas-invalidas.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaAssociarAssinatura.analisar(retorno)


@pytest.mark.acessa_sat
@pytest.mark.invoca_associarassinatura
def test_funcao_associarassinatura(request, clientesatlocal):
    # Este teste baseia-se na resposta da biblioteca SAT de simulação (mockup)
    # que é usada nos testes do projeto SATHub. Sempre associa com sucesso.
    #
    # Detalhes em: https://github.com/base4sistemas/sathub
    #
    cnpj_ac = '1' * 14
    cnpj_estabelecimento = '2' * 14
    sequencia_cnpj = cnpj_ac + cnpj_estabelecimento
    assinatura_ac = 'Xyz...Hij=='

    resposta = clientesatlocal.associar_assinatura(
            sequencia_cnpj,
            assinatura_ac)
    assert resposta.EEEEE == '13000'
