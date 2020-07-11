# -*- coding: utf-8 -*-
#
# tests/test_consultarstatusoperacional.py
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
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from io import open

from builtins import str as text

import pytest

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaConsultarStatusOperacional
from satcfe.resposta.consultarstatusoperacional import DESBLOQUEADO
from satcfe.util import as_date
from satcfe.util import as_datetime


def test_resposta_consultarstatusoperacional(datadir):
    arquivo = text(datadir.join('respostas-de-sucesso.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        r_sucessos = f.read().splitlines()

    resposta = RespostaConsultarStatusOperacional.analisar(r_sucessos[0])
    assert resposta.numeroSessao == 61407
    assert resposta.EEEEE == '10000'
    assert resposta.mensagem == 'Resposta com sucesso'
    assert resposta.cod == ''
    assert resposta.mensagemSEFAZ == ''
    assert resposta.NSERIE == '900004019'
    assert resposta.TIPO_LAN == 'DHCP'
    assert resposta.LAN_IP == '10.0.0.108'
    assert resposta.LAN_MAC == '30:40:03:19:19:40'
    assert resposta.LAN_MASK == '255.255.255.0'
    assert resposta.LAN_GW == '10.0.0.1'
    assert resposta.LAN_DNS_1 == '10.0.0.1'
    assert resposta.LAN_DNS_2 == '10.0.0.1'
    assert resposta.STATUS_LAN == 'CONECTADO'
    assert resposta.NIVEL_BATERIA == 'ALTO'
    assert resposta.MT_TOTAL == '4 GB'
    assert resposta.MT_USADA == '260 MB'
    assert resposta.DH_ATUAL == as_datetime('20150912113321')
    assert resposta.VER_SB == '01.00.00'
    assert resposta.VER_LAYOUT == '00.06'
    assert resposta.ULTIMO_CF_E_SAT == '35150908723218000186599000040190000723645630'  # noqa: E501
    assert resposta.LISTA_INICIAL == '00000000000000000000000000000000000000000000'  # noqa: E501
    assert resposta.LISTA_FINAL == '00000000000000000000000000000000000000000000'  # noqa: E501
    assert resposta.DH_CFE == as_datetime('20150912104828')
    assert resposta.DH_ULTIMA == as_datetime('20150912113039')
    assert resposta.CERT_EMISSAO == as_date('20150708')
    assert resposta.CERT_VENCIMENTO == as_date('20200708')
    assert resposta.ESTADO_OPERACAO == 0

    resposta = RespostaConsultarStatusOperacional.analisar(r_sucessos[1])
    # Resposta de um equipamento SAT que ainda não transmitiu nenhum CF-e,
    # conforme ocorrência https://github.com/base4sistemas/sathub/issues/1
    # Note que os campos 16 (ULTIMO_CF_E_SAT), 17 (LISTA_INICIAL),
    # 18 (LISTA_FINAL) e 19 (DH_CFE) estão vazios.
    assert resposta.EEEEE == '10000'
    assert resposta.ULTIMO_CF_E_SAT == ''
    assert resposta.LISTA_INICIAL == ''
    assert resposta.LISTA_FINAL == ''
    assert resposta.DH_CFE is None

    # demais respostas de sucesso, se houverem
    for retorno in r_sucessos[2:]:
        resposta = RespostaConsultarStatusOperacional.analisar(retorno)
        assert resposta.EEEEE == '10000'


def test_respostas_de_falha(datadir):
    arquivo = text(datadir.join('respostas-de-falha.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()
    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaConsultarStatusOperacional.analisar(retorno)


def test_respostas_invalidas(datadir):
    arquivo = text(datadir.join('respostas-invalidas.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()
    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaConsultarStatusOperacional.analisar(retorno)


@pytest.mark.acessa_sat
@pytest.mark.invoca_consultarstatusoperacional
def test_funcao_consultarstatusoperacional(clientesatlocal):
    resposta = clientesatlocal.consultar_status_operacional()
    assert resposta.EEEEE == '10000'
    assert resposta.TIPO_LAN == 'DHCP'
    assert resposta.STATUS_LAN == 'CONECTADO'
    assert resposta.NIVEL_BATERIA == 'ALTO'
    assert resposta.ESTADO_OPERACAO == DESBLOQUEADO
