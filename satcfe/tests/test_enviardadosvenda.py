# -*- coding: utf-8 -*-
#
# satcfe/tests/resposta/test_enviardadosvenda.py
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
import xml.etree.ElementTree as ET

from decimal import Decimal

import pytest

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaEnviarDadosVenda
from satcfe.util import as_datetime
from satcfe.util import str_to_base64


def test_respostas_de_sucesso(datadir):
    with open(datadir.join('respostas-de-sucesso.txt'), 'r') as fresp, \
         open(datadir.join('cfe-autorizado.xml'), 'r') as fxml:
        r_sucessos = fresp.read().splitlines()
        cfe_autorizado = fxml.read()

    _CFe = ET.fromstring(cfe_autorizado)
    _infCFe = _CFe.find('./infCFe')
    chave_consulta = _infCFe.attrib['Id']
    assinatura_qrcode = _infCFe.findtext('./ide/assinaturaQRCODE')

    resposta = RespostaEnviarDadosVenda.analisar(r_sucessos[0])
    assert resposta.numeroSessao == 123456
    assert resposta.EEEEE == '06000'
    assert resposta.CCCC == '0000'
    assert resposta.arquivoCFeSAT == str_to_base64(cfe_autorizado)
    assert resposta.timeStamp == as_datetime('20150718154423')
    assert resposta.chaveConsulta == chave_consulta
    assert resposta.valorTotalCFe == Decimal('2.00')
    assert resposta.assinaturaQRCODE == assinatura_qrcode


def test_respostas_de_falha(datadir):
    with open(datadir.join('respostas-de-falha.txt'), 'r') as f:
        respostas = f.read().splitlines()
    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaEnviarDadosVenda.analisar(retorno)


def test_respostas_invalidas(datadir):
    with open(datadir.join('respostas-invalidas.txt'), 'r') as f:
        respostas = f.read().splitlines()
    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaEnviarDadosVenda.analisar(retorno)


@pytest.mark.skipif(
        pytest.config.getoption('--skip-enviardadosvenda') or
        pytest.config.getoption('--skip-funcoes-sat'),
        reason='Funcao `EnviarDadosVenda` explicitamente ignorada')
def test_funcao_enviardadosvenda(clientesatlocal, cfevenda):
    resposta = clientesatlocal.enviar_dados_venda(cfevenda)
    assert resposta.EEEEE == '06000'
    assert resposta.valorTotalCFe == Decimal('5.75')
    assert len(resposta.chaveConsulta) == 47
    assert resposta.chaveConsulta.startswith('CFe')
