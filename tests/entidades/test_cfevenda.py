# -*- coding: utf-8 -*-
#
# tests/entidades/test_cfevenda.py
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

from satcomum import constantes
from satcfe.entidades import CFeVenda
from satcfe.entidades import Emitente


def test_simples_minimo():
    """XML esperado:

    .. sourcecode:: xml

        <CFe>
            <infCFe versaoDadosEnt="0.07">
                <ide>
                    <CNPJ>08427847000169</CNPJ>
                    <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
                    <numeroCaixa>001</numeroCaixa>
                </ide>
                <emit>
                    <CNPJ>61099008000141</CNPJ>
                    <IE>111111111111</IE>
                    <IM>12345</IM>
                    <cRegTribISSQN>3</cRegTribISSQN>
                    <indRatISSQN>N</indRatISSQN>
                </emit>
                <dest />
                <total />
                <pgto />
            </infCFe>
        </CFe>

    """  # noqa: E501

    cfe = CFeVenda(
            CNPJ='08427847000169',
            signAC=constantes.ASSINATURA_AC_TESTE,
            numeroCaixa=1,
            emitente=Emitente(
                    CNPJ='61099008000141',
                    IE='111111111111',
                    IM='12345',
                    cRegTribISSQN=constantes.C15_SOCIEDADE_PROFISSIONAIS,
                    indRatISSQN=constantes.C16_NAO_RATEADO))

    el = cfe._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'CFe'

    infCFe = el.find('infCFe')
    assert infCFe.attrib['versaoDadosEnt'] == '0.07'

    ide = infCFe.find('ide')
    assert ide.find('CNPJ').text == '08427847000169'
    assert ide.find('numeroCaixa').text == '001'
    assert ide.find('signAC').text == (
            'SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT'
        )

    emit = infCFe.find('emit')
    assert emit.find('CNPJ').text == '61099008000141'
    assert emit.find('IE').text == '111111111111'
    assert emit.find('IM').text == '12345'
    assert emit.find('indRatISSQN').text == constantes.C16_NAO_RATEADO
    assert emit.find('cRegTribISSQN').text == (
            constantes.C15_SOCIEDADE_PROFISSIONAIS
        )

    dest = infCFe.find('dest')
    assert dest is not None
    assert len(list(dest)) == 0

    total = infCFe.find('total')
    assert total is not None
    assert len(list(total)) == 0

    pgto = infCFe.find('pgto')
    assert pgto is not None
    assert len(list(pgto)) == 0
