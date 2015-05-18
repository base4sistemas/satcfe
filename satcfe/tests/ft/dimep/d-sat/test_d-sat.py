# -*- coding: utf-8 -*-
#
# satcfe/test/ft/dimep/d-sat/test_d-sat.py
#
# Copyright 2015 Base4 Sistemas Ltda ME
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

import os
import sys

import pytest

from satcomum.constantes import WINDOWS_STDCALL


# assume apenas plataforma windows, por enquanto
pytestmark = pytest.mark.skipif(
        sys.platform != 'win32',
        reason='requires Microsoft Windows')

# os seguintes atributos que serão lidos pelas fixtures (via request.module)
convencao = WINDOWS_STDCALL
caminho_dll = os.path.join(os.path.abspath(os.path.dirname(__file__)),
        'kit', 'windows', 'dllsat.dll')


def test_consultar_sat(clientesatlocal):
    resposta = clientesatlocal.consultar_sat()
    assert resposta.EEEEE == '08000', _assert_msg(resposta, 'ConsultarSAT')


def test_consultar_status_operacional(clientesatlocal):
    resposta = clientesatlocal.consultar_status_operacional()
    assert resposta.EEEEE == '10000', \
            _assert_msg(resposta, 'ConsultarStatusOperacional')


def test_extrair_logs(clientesatlocal):
    resposta = clientesatlocal.extrair_logs()
    assert resposta.EEEEE == '15000', _assert_msg(resposta, 'ExtrairLogs')


def test_teste_fim_a_fim(cfevenda, clientesatlocal):
    resposta = clientesatlocal.teste_fim_a_fim(cfevenda)
    assert resposta.EEEEE == '09000', _assert_msg(resposta, 'TesteFimAFim')


def test_enviar_dados_venda(cfevenda, clientesatlocal):
    resposta = clientesatlocal.enviar_dados_venda(cfevenda)
    assert resposta.EEEEE == '06000', _assert_msg(resposta, 'EnviarDadosVenda')


def test_cancelar_ultima_venda(cfevenda, cfecanc, clientesatlocal):
    resposta_venda = clientesatlocal.enviar_dados_venda(cfevenda)
    assert resposta_venda.EEEEE == '06000', \
            _assert_msg(resposta_venda, 'EnviarDadosVenda')

    cfecanc.chCanc=resposta_venda.chaveConsulta
    resposta_canc = clientesatlocal.cancelar_ultima_venda(canc)
    assert resposta_canc.EEEEE == '07000', \
            _assert_msg(resposta_canc, 'CancelarUltimaVenda')


def _assert_msg(resposta, funcao):
    return 'Resposta "{}" '\
            'numeroSessao={}, EEEEE={}, mensagem={}'.format(
                    funcao,
                    resposta.numeroSessao,
                    resposta.EEEEE,
                    resposta.mensagem)
