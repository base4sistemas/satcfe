# -*- coding: utf-8 -*-
#
# satcfe/tests/test_extrairlogs.py
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
from satcfe.resposta import RespostaExtrairLogs


def test_respostas_de_sucesso(datadir):
    with open(datadir.join('respostas-de-sucesso.txt'), 'r') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        resposta = RespostaExtrairLogs.analisar(retorno)
        assert resposta.EEEEE == '15000'  # único código que representa sucesso
        assert len(resposta.arquivoLog) > 0


def test_respostas_de_falha(datadir):
    with open(datadir.join('respostas-de-falha.txt'), 'r') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaExtrairLogs.analisar(retorno)


def test_respostas_invalidas(datadir):
    with open(datadir.join('respostas-invalidas.txt'), 'r') as f:
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
    assert destino.read() == resposta.conteudo()


@pytest.mark.acessa_sat
@pytest.mark.invoca_extrairlogs
def test_salvar_sem_destino_especifico(request, tmpdir, clientesatlocal):
    resposta = clientesatlocal.extrair_logs()
    assert resposta.EEEEE == '15000'
    assert len(resposta.arquivoLog) > 0

    destino = resposta.salvar(dir=tmpdir.strpath)
    with open(destino, 'r') as f:
        conteudo = f.read()

    assert conteudo == resposta.conteudo()
