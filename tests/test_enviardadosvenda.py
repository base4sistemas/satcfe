# -*- coding: utf-8 -*-
#
# tests/test_enviardadosvenda.py
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

from decimal import Decimal
from io import open

from builtins import str as text

import pytest

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaEnviarDadosVenda
from satcfe.util import as_datetime
from satcfe.util import str_to_base64


def test_respostas_de_sucesso(datadir):
    arquivo_sucesso = text(datadir.join('respostas-de-sucesso.txt'))
    arquivo_cfesat = text(datadir.join('cfe-autorizado.xml'))
    with open(arquivo_sucesso, 'r', encoding='utf-8') as fresp, \
            open(arquivo_cfesat, 'r', encoding='utf-8') as fxml:
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

    # Evidente que esta não é a melhor maneira de comparar strings XML, mas é
    # tudo o que é necessário, ou seja, o conteúdo XML apenas precisa ser
    # retornado pelo método xml() para que esteja tudo OK;
    assert resposta.xml()[:28] == '<?xml version="1.0"?>\n<CFe>\n'

    # Aqui a mesma coisa, o método qrcode() só precisa resultar algo, já que o
    # foco não é testar a produção da messa de dados do QRCode;
    assert resposta.qrcode()[:9] == '351507087'


def test_respostas_de_falha(datadir):
    arquivo = text(datadir.join('respostas-de-falha.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT) as exsat:
            RespostaEnviarDadosVenda.analisar(retorno)

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
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaEnviarDadosVenda.analisar(retorno)


@pytest.mark.acessa_sat
@pytest.mark.invoca_enviardadosvenda
def test_funcao_enviardadosvenda(clientesatlocal, cfevenda):
    resposta = clientesatlocal.enviar_dados_venda(cfevenda)
    assert resposta.EEEEE == '06000'
    assert resposta.valorTotalCFe == Decimal('4.73')
    assert len(resposta.chaveConsulta) == 47
    assert resposta.chaveConsulta.startswith('CFe')


@pytest.mark.acessa_sat
@pytest.mark.invoca_enviardadosvenda
def test_emite_warning_argumentos_extras_ignorados(
        clientesatlocal,
        cfevenda):
    conteudo_cfe = cfevenda.documento()  # resolve o documento (obtendo str)
    with pytest.warns(UserWarning) as rec:
        resposta = clientesatlocal.enviar_dados_venda(
                conteudo_cfe,
                'argumentos',
                'extras',
                'informados',
                argumentos=1,
                extras=2,
                informados=3)

    assert len(rec) == 1
    assert rec[0].message.args[0].startswith('O documento foi informado')
    assert resposta.EEEEE == '06000'


@pytest.mark.acessa_sat
@pytest.mark.invoca_enviardadosvenda
def test_argumento_nao_str_sem_metodo_documento(clientesatlocal):
    # se o argumento dados_venda não for str, então deverá ser um objeto
    # que possua um método chamado "documento()" capaz de gerar o CF-e de
    # venda que será enviado ao equipamento SAT
    class _Quack(object):
        pass

    with pytest.raises(ValueError):
        clientesatlocal.enviar_dados_venda(_Quack())
