# -*- coding: utf-8 -*-
#
# tests/test_consultarultimasessaofiscal.py
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
from satcfe.resposta import RespostaConsultarNumeroSessao


_RESPOSTAS_ESPERADAS = {
        # EEEEE, função SAT esperada
        '06000': 'EnviarDadosVenda',
        '07000': 'CancelarUltimaVenda',
    }


def test_respostas_de_sucesso(datadir):
    arquivo = text(datadir.join('respostas-de-sucesso.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        resp = RespostaConsultarNumeroSessao.analisar(retorno)
        assert resp.EEEEE in _RESPOSTAS_ESPERADAS
        assert resp.atributos.funcao == _RESPOSTAS_ESPERADAS[resp.EEEEE]
        assert resp.atributos.verbatim == retorno


def test_respostas_de_falha(datadir):
    arquivo = text(datadir.join('respostas-de-falha.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaConsultarNumeroSessao.analisar(retorno)


def test_respostas_invalidas(datadir):
    arquivo = text(datadir.join('respostas-invalidas.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaConsultarNumeroSessao.analisar(retorno)


@pytest.mark.acessa_sat
@pytest.mark.invoca_consultarultimasessaofiscal
def test_funcao_consultarultimasessaofiscal(clientesatlocal):
    # Este teste baseia-se na resposta da biblioteca SAT de simulação (mockup)
    # que é usada nos testes do projeto SATHub. Nesta biblioteca, a função
    # ConsultarUltimaSessaoFiscal sempre indica que não existe sessão fiscal.
    #
    with pytest.raises(ExcecaoRespostaSAT) as exsat:
        clientesatlocal.consultar_ultima_sessao_fiscal()

    assert hasattr(exsat.value, 'resposta')

    resposta = exsat.value.resposta
    assert resposta.EEEEE == '19003'
    assert resposta.mensagem == 'Não existe sessão fiscal'
