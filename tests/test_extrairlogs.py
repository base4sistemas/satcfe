# -*- coding: utf-8 -*-
#
# tests/test_extrairlogs.py
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
from satcfe.resposta import RespostaExtrairLogs


def test_respostas_de_sucesso(datadir):
    arquivo = text(datadir.join('respostas-de-sucesso.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        resposta = RespostaExtrairLogs.analisar(retorno)
        assert resposta.EEEEE == '15000'  # único código que representa sucesso
        assert len(resposta.arquivoLog) > 0


def test_respostas_de_falha(datadir):
    arquivo = text(datadir.join('respostas-de-falha.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaExtrairLogs.analisar(retorno)


def test_respostas_invalidas(datadir):
    arquivo = text(datadir.join('respostas-invalidas.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaExtrairLogs.analisar(retorno)


@pytest.mark.acessa_sat
@pytest.mark.invoca_extrairlogs
def test_extrairlogs(request, clientesatlocal):
    resposta = clientesatlocal.extrair_logs()
    assert resposta.EEEEE == '15000'
    assert len(resposta.arquivoLog) > 0


@pytest.mark.acessa_sat
@pytest.mark.invoca_extrairlogs
def test_salvar_com_destino_especifico(request, tmpdir, clientesatlocal):
    resposta = clientesatlocal.extrair_logs()
    assert resposta.EEEEE == '15000'
    assert len(resposta.arquivoLog) > 0

    destino = tmpdir.join('arquivo-log.txt')
    resposta.salvar(destino=destino.strpath)

    arquivo_salvo = destino.strpath
    with open(arquivo_salvo, 'r', encoding='utf-8') as f:
        conteudo_salvo = f.read()

    assert conteudo_salvo == resposta.conteudo()


@pytest.mark.acessa_sat
@pytest.mark.invoca_extrairlogs
def test_salvar_sem_destino_especifico(request, tmpdir, clientesatlocal):
    resposta = clientesatlocal.extrair_logs()
    assert resposta.EEEEE == '15000'
    assert len(resposta.arquivoLog) > 0

    destino = resposta.salvar(dir=tmpdir.strpath)
    with open(destino, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    assert conteudo == resposta.conteudo()
