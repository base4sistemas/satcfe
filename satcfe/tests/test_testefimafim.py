# -*- coding: utf-8 -*-
#
# satcfe/tests/resposta/test_testefimafim.py
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

import pytest

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaTesteFimAFim
from satcfe.util import as_datetime
from satcfe.util import str_to_base64


def test_resposta_testefimafim(datadir):
    with open(datadir.join('respostas-de-sucesso.txt'), 'r') as fresp, \
         open(datadir.join('cfe-teste-assinado.xml'), 'r') as fxml:
        r_sucessos = fresp.read().splitlines()
        cfe_teste = fxml.read()

    _CFe = ET.fromstring(cfe_teste)
    _infCFe = _CFe.find('./infCFe')
    chave_consulta = _infCFe.attrib['Id']

    resposta = RespostaTesteFimAFim.analisar(r_sucessos[0])
    assert resposta.numeroSessao == 31545
    assert resposta.EEEEE == '09000'
    assert resposta.arquivoCFeBase64 == str_to_base64(cfe_teste)
    assert resposta.timeStamp == as_datetime('20150912101513')
    assert resposta.numDocFiscal == 0
    assert resposta.chaveConsulta == chave_consulta


def test_respostas_de_falha(datadir):
    with open(datadir.join('respostas-de-falha.txt'), 'r') as f:
        respostas = f.read().splitlines()
    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaTesteFimAFim.analisar(retorno)


def test_respostas_invalidas(datadir):
    with open(datadir.join('respostas-invalidas.txt'), 'r') as f:
        respostas = f.read().splitlines()
    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaTesteFimAFim.analisar(retorno)


@pytest.mark.skipif(
        pytest.config.getoption('--skip-testefimafim', default=True) or
        pytest.config.getoption('--skip-funcoes-sat', default=True),
        reason='Funcao `TesteFimAFim` explicitamente ignorada')
def test_funcao_testefimafim(clientesatlocal, cfevenda):
    resposta = clientesatlocal.teste_fim_a_fim(cfevenda)
    assert resposta.EEEEE == '09000'
    assert resposta.numDocFiscal == 0
    assert len(resposta.chaveConsulta) == 47
    assert resposta.chaveConsulta.startswith('CFe')
