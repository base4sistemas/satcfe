# -*- coding: utf-8 -*-
#
# tests/entidades/test_meiopagamento.py
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

from decimal import Decimal

from satcomum import constantes

from satcfe.entidades import MeioPagamento


def test_simples():
    """XML esperado:

    .. sourcecode:: xml

        <MP>
            <cMP>01</cMP>
            <vMP>10.00</vMP>
        </MP>

    """
    mp = MeioPagamento(cMP=constantes.WA03_DINHEIRO, vMP=Decimal('10.00'))
    el = mp._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'MP'
    assert el.find('cMP').text == constantes.WA03_DINHEIRO
    assert el.find('vMP').text == '10.00'


def test_simples_com_adm_cartao():
    """XML esperado:

    .. sourcecode:: xml

        <MP>
            <cMP>01</cMP>
            <vMP>10.00</vMP>
            <cAdmC>999</cAdmC>
        </MP>

    """
    mp = MeioPagamento(
            cMP=constantes.WA03_CARTAO_CREDITO,
            vMP=Decimal('10.00'),
            cAdmC='999')

    el = mp._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'MP'
    assert el.find('cMP').text == constantes.WA03_CARTAO_CREDITO
    assert el.find('vMP').text == '10.00'
    assert el.find('cAdmC').text == '999'
