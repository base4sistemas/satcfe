# -*- coding: utf-8 -*-
#
# satcfe/tests/test_cancelarultimavenda.py
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

from satcfe.entidades import CFeCancelamento
from satcfe.entidades import Destinatario
from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaCancelarUltimaVenda
from satcfe.util import as_datetime
from satcfe.util import str_to_base64


def test_respostas_de_sucesso(datadir):
    with open(datadir.join('respostas-de-sucesso.txt'), 'r') as f, \
         open(datadir.join('cfecanc-autorizado.xml'), 'r') as fxml:
        r_sucessos = f.read().splitlines()
        cfecanc_autorizado = fxml.read()

    _CFeCanc = ET.fromstring(cfecanc_autorizado)
    _infCFe = _CFeCanc.find('./infCFe')
    chave_consulta = _infCFe.attrib['Id']
    assinatura_qrcode = _infCFe.findtext('./ide/assinaturaQRCODE')

    resposta = RespostaCancelarUltimaVenda.analisar(r_sucessos[0])
    assert resposta.numeroSessao == 123456
    assert resposta.EEEEE == '07000'
    assert resposta.CCCC == '0000'
    assert resposta.arquivoCFeBase64 == str_to_base64(cfecanc_autorizado)
    assert resposta.timeStamp == as_datetime('20150911175921')
    assert resposta.chaveConsulta == chave_consulta
    assert resposta.valorTotalCFe == Decimal('2.00')
    assert resposta.assinaturaQRCODE == assinatura_qrcode


def test_respostas_de_falha(datadir):
    with open(datadir.join('respostas-de-falha.txt'), 'r') as f:
        respostas = f.read().splitlines()
    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaCancelarUltimaVenda.analisar(retorno)


def test_respostas_invalidas(datadir):
    with open(datadir.join('respostas-invalidas.txt'), 'r') as f:
        r_invalidas = f.read().splitlines()
    for retorno in r_invalidas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaCancelarUltimaVenda.analisar(retorno)


@pytest.mark.skipif(
        pytest.config.getoption('--skip-cancelarultimavenda') or
        pytest.config.getoption('--skip-funcoes-sat'),
        reason='Funcao `CancelarUltimaVenda` explicitamente ignorada')
def test_funcao_cancelarultimavenda(clientesatlocal, cfevenda):
    # realiza uma venda para cancelar em seguida
    rvenda = clientesatlocal.enviar_dados_venda(cfevenda)

    cfecanc = CFeCancelamento(
            chCanc=rvenda.chaveConsulta,
            CNPJ=pytest.config.getoption('--cnpj-ac'),
            signAC=pytest.config.getoption('--assinatura-ac'),
            numeroCaixa=pytest.config.getoption('--numero-caixa'),
            destinatario=Destinatario(
                    CPF='11122233396',
                    xNome=u'João de Teste'))

    rcanc = clientesatlocal.cancelar_ultima_venda(cfecanc.chCanc, cfecanc)
    assert rcanc.EEEEE == '07000'
    assert rcanc.valorTotalCFe == Decimal('5.75')
