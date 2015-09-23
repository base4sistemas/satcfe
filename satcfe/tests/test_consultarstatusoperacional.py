# -*- coding: utf-8 -*-
#
# satcfe/tests/resposta/test_consultarstatusoperacional.py
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

import base64

import pytest

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaConsultarStatusOperacional
from satcfe.util import as_date
from satcfe.util import as_datetime


RESP_SUCESSO = [
        u'061407|10000|Resposta com sucesso|||900004019|DHCP|'\
                '010.000.000.108|30:40:03:19:19:40|255.255.255.000|'\
                '010.000.000.001|010.000.000.001|010.000.000.001|'\
                'CONECTADO|ALTO|4 GB|260 MB|20150912113321|01.00.00|00.06|'\
                '35150908723218000186599000040190000723645630|'\
                '00000000000000000000000000000000000000000000|'\
                '00000000000000000000000000000000000000000000|'\
                '20150912104828|20150912113039|20150708|20200708|0',

        # Resposta de um equipamento SAT que ainda não transmitiu nenhum CF-e,
        # conforme ocorrência https://github.com/base4sistemas/sathub/issues/1
        # Note que os campos 16 (ULTIMO_CF_E_SAT), 17 (LISTA_INICIAL),
        # 18 (LISTA_FINAL) e 19 (DH_CFE) estão vazios.
        u'195195|10000|Resposta com Sucesso|||900003522|static\n|'\
                '192.168.000.100|00:07:25:15:14:cd|255.255.255.000|'\
                '192.168.000.001|192.168.000.001|000.000.000.000|'\
                'CONECTADO|ALTO|1870127104|1174929408|20150922165839|'
                '01.00.00|0.06|||||20150919233139|20150905|20200905|0'
    ]


RESP_FALHA = [
        u'123456|10001|Código de ativação inválido||',
        u'123456|10098|SAT em processamento. Tente novamente.||',
        u'123456|10099|Erro desconhecido||',
    ]


RESP_INVALIDAS = [
        u'Resposta sem nenhum separador',
        u'Numero inesperado de campos|a|b|c|d|e|f|g|h|i|j|k',
    ]


def test_resposta_consultarstatusoperacional():
    resposta = RespostaConsultarStatusOperacional.analisar(RESP_SUCESSO[0])
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
    assert resposta.ULTIMO_CF_E_SAT == '35150908723218000186599000040190000723645630'
    assert resposta.LISTA_INICIAL == '00000000000000000000000000000000000000000000'
    assert resposta.LISTA_FINAL == '00000000000000000000000000000000000000000000'
    assert resposta.DH_CFE == as_datetime('20150912104828')
    assert resposta.DH_ULTIMA == as_datetime('20150912113039')
    assert resposta.CERT_EMISSAO == as_date('20150708')
    assert resposta.CERT_VENCIMENTO == as_date('20200708')
    assert resposta.ESTADO_OPERACAO == 0

    for retorno in RESP_SUCESSO[1:]:
        resposta = RespostaConsultarStatusOperacional.analisar(retorno)
        assert resposta.EEEEE == '10000'

    for retorno in RESP_FALHA:
        with pytest.raises(ExcecaoRespostaSAT):
            resposta = RespostaConsultarStatusOperacional.analisar(retorno)

    for retorno in RESP_INVALIDAS:
        with pytest.raises(ErroRespostaSATInvalida):
            resposta = RespostaConsultarStatusOperacional.analisar(retorno)


@pytest.mark.skipif(
        pytest.config.getoption('--skip-consultarstatusoperacional') or
        pytest.config.getoption('--skip-funcoes-sat'),
        reason='Funcao `ConsultarStatusOperacional` explicitamente ignorada')
def test_funcao_consultarstatusoperacional(clientesatlocal):
    resposta = clientesatlocal.consultar_status_operacional()
    assert resposta.EEEEE == '10000'
