# -*- coding: utf-8 -*-
#
# tests/entidades/test_cfecanc.py
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
from satcfe.entidades import CFeCancelamento


def test_simples_minimo():
    """XML esperado:

    .. sourcecode:: xml

        <CFeCanc>
            <infCFe chCanc="CFe01234567890123456789012345678901234567890123">
                <ide>
                    <CNPJ>08427847000169</CNPJ>
                    <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
                    <numeroCaixa>001</numeroCaixa>
                </ide>
                <emit />
                <dest />
                <total />
            </infCFe>
        </CFeCanc>

    """  # noqa: E501

    cfecanc = CFeCancelamento(
            chCanc='CFe01234567890123456789012345678901234567890123',
            CNPJ='08427847000169',
            signAC=constantes.ASSINATURA_AC_TESTE,
            numeroCaixa=1)

    el = cfecanc._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'CFeCanc'

    infCFe = el.find('infCFe')
    assert infCFe.attrib['chCanc'] == (
            'CFe01234567890123456789012345678901234567890123'
        )

    ide = infCFe.find('ide')
    assert ide.find('CNPJ').text == '08427847000169'
    assert ide.find('numeroCaixa').text == '001'
    assert ide.find('signAC').text == (
            'SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT'
        )

    emit = infCFe.find('emit')
    assert emit is not None
    assert len(list(emit)) == 0

    dest = infCFe.find('dest')
    assert dest is not None
    assert len(list(dest)) == 0

    total = infCFe.find('total')
    assert total is not None
    assert len(list(total)) == 0
