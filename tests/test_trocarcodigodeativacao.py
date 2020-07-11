# -*- coding: utf-8 -*-
#
# tests/test_trocarcodigodeativacao.py
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

from satcomum import constantes

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaSAT


def test_respostas_de_sucesso(datadir):
    arquivo = text(datadir.join('respostas-de-sucesso.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        resposta = RespostaSAT.trocar_codigo_de_ativacao(retorno)
        assert resposta.EEEEE == '18000'  # único código de sucesso possível


def test_respostas_de_falha(datadir):
    arquivo = text(datadir.join('respostas-de-falha.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaSAT.trocar_codigo_de_ativacao(retorno)


def test_respostas_invalidas(datadir):
    arquivo = text(datadir.join('respostas-invalidas.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaSAT.trocar_codigo_de_ativacao(retorno)


@pytest.mark.acessa_sat
@pytest.mark.invoca_trocarcodigodeativacao
def test_trocarcodigodeativacao_regular(request, clientesatlocal):
    # Este teste baseia-se na resposta da biblioteca SAT de simulação (mockup)
    # que é usada nos testes do projeto SATHub:
    # https://github.com/base4sistemas/sathub
    #
    novo_codigo = 's3cr370'

    if clientesatlocal.codigo_ativacao == novo_codigo:
        # garante que o novo código de ativação não seja igual ao atual
        novo_codigo = 'd15cr370'

    resposta = clientesatlocal.trocar_codigo_de_ativacao(
            novo_codigo,
            opcao=constantes.CODIGO_ATIVACAO_REGULAR)

    assert resposta.EEEEE == '18000'
    assert resposta.mensagem == 'Código de ativação alterado com sucesso'

    # ao alterar o código de ativação, o novo código deve ter sido alterado
    # também no cliente SAT, para que as chamadas subsequentes à funções SAT
    # tenham sucesso...
    assert clientesatlocal.codigo_ativacao == novo_codigo


@pytest.mark.acessa_sat
@pytest.mark.invoca_trocarcodigodeativacao
def test_trocarcodigodeativacao_emergencia(request, clientesatlocal):
    # Este teste baseia-se na resposta da biblioteca SAT de simulação (mockup)
    # que é usada nos testes do projeto SATHub:
    # https://github.com/base4sistemas/sathub
    #
    novo_codigo = 's3cr370'
    resposta = clientesatlocal.trocar_codigo_de_ativacao(
            novo_codigo,
            opcao=constantes.CODIGO_ATIVACAO_EMERGENCIA,
            codigo_emergencia='35c0nd1d0')
    assert resposta.EEEEE == '18000'
    assert resposta.mensagem == 'Código de ativação alterado com sucesso'


@pytest.mark.acessa_sat
@pytest.mark.invoca_trocarcodigodeativacao
def test_trocarcodigodeativacao_novo_codigo_invalido(request, clientesatlocal):
    # Este teste baseia-se na resposta da biblioteca SAT de simulação (mockup)
    # que é usada nos testes do projeto SATHub:
    # https://github.com/base4sistemas/sathub
    #
    with pytest.raises(ValueError):
        clientesatlocal.trocar_codigo_de_ativacao('')


@pytest.mark.acessa_sat
@pytest.mark.invoca_trocarcodigodeativacao
def test_trocarcodigodeativacao_opcao_invalida(request, clientesatlocal):
    # Este teste baseia-se na resposta da biblioteca SAT de simulação (mockup)
    # que é usada nos testes do projeto SATHub:
    # https://github.com/base4sistemas/sathub
    #
    with pytest.raises(ValueError):
        clientesatlocal.trocar_codigo_de_ativacao('s3cr370', opcao=9)


@pytest.mark.acessa_sat
@pytest.mark.invoca_trocarcodigodeativacao
def test_trocarcodigodeativacao_com_codigo_emergia_invalido(
        request,
        clientesatlocal):
    # Este teste baseia-se na resposta da biblioteca SAT de simulação (mockup)
    # que é usada nos testes do projeto SATHub:
    # https://github.com/base4sistemas/sathub
    #
    novo_codigo = 's3cr370'
    with pytest.raises(ValueError):
        # (!) note que o parâmetro 'codigo_emergencia' não é informado
        clientesatlocal.trocar_codigo_de_ativacao(
                novo_codigo,
                opcao=constantes.CODIGO_ATIVACAO_EMERGENCIA)
