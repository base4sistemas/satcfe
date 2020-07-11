# -*- coding: utf-8 -*-
#
# tests/test_consultarnumerosessao.py
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
        '04000': 'AtivarSAT',
        '04006': 'AtivarSAT',
        '05000': 'ComunicarCertificadoICPBRASIL',
        '08000': 'ConsultarSAT',
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
@pytest.mark.invoca_consultarnumerosessao
def test_funcao_consultarnumerosessao(clientesatlocal):
    # Este teste baseia-se na resposta da biblioteca SAT de simulação (mockup)
    # que é usada nos testes do projeto SATHub. Nesta biblioteca, a função
    # ConsultarNumeroSessao sempre indica que o número de sessão consultado
    # não existe.
    #
    # Detalhes em: https://github.com/base4sistemas/sathub
    #
    with pytest.raises(ExcecaoRespostaSAT) as exsat:
        clientesatlocal.consultar_numero_sessao(123456)

    assert hasattr(exsat.value, 'resposta')

    resposta = exsat.value.resposta
    assert resposta.EEEEE == '11003'
    assert resposta.mensagem == 'Sessão não existe'
