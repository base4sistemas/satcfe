# -*- coding: utf-8 -*-
#
# tests/test_configurarinterfacederede.py
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
from satcfe.resposta import RespostaSAT


def test_respostas_sucesso(datadir):
    arquivo = text(datadir.join('respostas-de-sucesso.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        resposta = RespostaSAT.configurar_interface_de_rede(retorno)
        assert resposta.EEEEE == '12000'  # único código que reprenta sucesso


def test_respostas_de_falha(datadir):
    arquivo = text(datadir.join('respostas-de-falha.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaSAT.configurar_interface_de_rede(retorno)


def test_respostas_invalidas(datadir):
    arquivo = text(datadir.join('respostas-invalidas.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaSAT.configurar_interface_de_rede(retorno)


@pytest.mark.acessa_sat
@pytest.mark.invoca_configurarinterfacederede
def test_funcao_configurarinterfacederede_minimo(clientesatlocal, rede_minimo):
    # Este teste baseia-se na resposta da biblioteca SAT de simulação (mockup)
    # que é usada nos testes do projeto SATHub. Sempre configura com sucesso.
    #
    # Detalhes em: https://github.com/base4sistemas/sathub
    #
    resposta = clientesatlocal.configurar_interface_de_rede(rede_minimo)
    assert resposta.EEEEE == '12000'
    assert resposta.mensagem.lower() == 'rede configurada com sucesso'


@pytest.mark.acessa_sat
@pytest.mark.invoca_configurarinterfacederede
def test_funcao_configurarinterfacederede_completo(
        clientesatlocal,
        rede_completo):
    # Este teste baseia-se na resposta da biblioteca SAT de simulação (mockup)
    # que é usada nos testes do projeto SATHub. Sempre configura com sucesso.
    #
    # Detalhes em: https://github.com/base4sistemas/sathub
    #
    resposta = clientesatlocal.configurar_interface_de_rede(rede_completo)
    assert resposta.EEEEE == '12000'
    assert resposta.mensagem.lower() == 'rede configurada com sucesso'


@pytest.mark.acessa_sat
@pytest.mark.invoca_configurarinterfacederede
def test_emite_warning_argumentos_extras_ignorados(
        clientesatlocal,
        rede_minimo):
    documento = rede_minimo.documento()
    with pytest.warns(UserWarning) as rec:
        resposta = clientesatlocal.configurar_interface_de_rede(
                documento,
                'argumentos',
                'extras',
                'informados',
                argumentos=1,
                extras=2,
                informados=3)

    assert len(rec) == 1
    assert rec[0].message.args[0].startswith('O documento foi informado')
    assert resposta.EEEEE == '12000'


@pytest.mark.acessa_sat
@pytest.mark.invoca_configurarinterfacederede
def test_argumento_nao_str_sem_metodo_documento(clientesatlocal):
    # se o argumento 'configuracao' não for str, então deverá ser um objeto
    # que possua um método chamado "documento()" capaz de gerar o conteúdo do
    # XML de configuração que será enviado ao equipamento SAT
    class _Quack(object):
        pass

    with pytest.raises(ValueError):
        clientesatlocal.configurar_interface_de_rede(_Quack())
