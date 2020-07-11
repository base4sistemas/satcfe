# -*- coding: utf-8 -*-
#
# tests/test_cancelarultimavenda.py
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

import xml.etree.ElementTree as ET

from io import open

from builtins import str as text

from decimal import Decimal

import pytest

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaCancelarUltimaVenda
from satcfe.util import as_datetime
from satcfe.util import str_to_base64


def test_respostas_de_sucesso(datadir):
    arquivo_sucesso = text(datadir.join('respostas-de-sucesso.txt'))
    arquivo_cfecanc = text(datadir.join('cfecanc-autorizado.xml'))
    with open(arquivo_sucesso, 'r', encoding='utf-8') as f, \
            open(arquivo_cfecanc, 'r', encoding='utf-8') as fxml:
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

    # Evidente que esta não é a melhor maneira de comparar strings XML, mas é
    # tudo o que é necessário, ou seja, o conteúdo XML apenas precisa ser
    # retornado pelo método xml() para que esteja tudo OK;
    assert resposta.xml()[:32] == '<?xml version="1.0"?>\n<CFeCanc>\n'

    # Aqui a mesma coisa, o método qrcode() só precisa resultar algo, já que o
    # foco não é testar a produção da messa de dados do QRCode;
    assert resposta.qrcode()[:9] == '351509087'


def test_respostas_de_falha(datadir):
    arquivo = text(datadir.join('respostas-de-falha.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()
    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT) as exsat:
            RespostaCancelarUltimaVenda.analisar(retorno)

        assert hasattr(exsat.value, 'resposta')
        resposta = exsat.value.resposta

        with pytest.raises(ExcecaoRespostaSAT):
            # quando a resposta não for sucesso, xml() deve falhar
            resposta.xml()

        with pytest.raises(ExcecaoRespostaSAT):
            # quando a resposta não for sucesso, qrcode() deve falhar
            resposta.qrcode()


def test_respostas_invalidas(datadir):
    arquivo = text(datadir.join('respostas-invalidas.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        r_invalidas = f.read().splitlines()
    for retorno in r_invalidas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaCancelarUltimaVenda.analisar(retorno)


@pytest.mark.acessa_sat
@pytest.mark.invoca_enviardadosvenda
@pytest.mark.invoca_cancelarultimavenda
def test_funcao_cancelarultimavenda(
        clientesatlocal,
        cfevenda,
        cfecancelamento):
    # realiza uma venda para cancelar em seguida
    resp_venda = clientesatlocal.enviar_dados_venda(cfevenda)
    cfecancelamento.chCanc = resp_venda.chaveConsulta

    resp_canc = clientesatlocal.cancelar_ultima_venda(
            resp_venda.chaveConsulta,
            cfecancelamento)

    assert resp_canc.EEEEE == '07000'
    assert resp_canc.valorTotalCFe == Decimal('4.73')


@pytest.mark.acessa_sat
@pytest.mark.invoca_enviardadosvenda
@pytest.mark.invoca_cancelarultimavenda
def test_emite_warning_argumentos_extras_ignorados(
        clientesatlocal,
        cfevenda,
        cfecancelamento):
    resp_venda = clientesatlocal.enviar_dados_venda(cfevenda)
    cfecancelamento.chCanc = resp_venda.chaveConsulta
    conteudo_cfecanc = cfecancelamento.documento()

    with pytest.warns(UserWarning) as rec:
        resp_canc = clientesatlocal.cancelar_ultima_venda(
                conteudo_cfecanc,
                'argumentos',
                'extras',
                'informados',
                argumentos=1,
                extras=2,
                informados=3)

        assert len(rec) == 1
        assert rec[0].message.args[0].startswith('O documento foi informado')
        assert resp_canc.EEEEE == '07000'


@pytest.mark.acessa_sat
@pytest.mark.invoca_cancelarultimavenda
def test_argumento_nao_str_sem_metodo_documento(clientesatlocal):
    # se o argumento dados_cancelamento não for str, então deverá ser um objeto
    # que possua um método chamado "documento()" capaz de gerar o CF-e de
    # cancelamento que será enviado ao equipamento SAT
    class _NoQuack(object):
        pass

    with pytest.raises(ValueError):
        clientesatlocal.cancelar_ultima_venda('CFe35...', _NoQuack())
