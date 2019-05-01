# -*- coding: utf-8 -*-
#
# satcfe/tests/entidades/test_meiopagamento.py
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
import xml.etree.ElementTree as ET

from decimal import Decimal

from satcfe.entidades import MeioPagamento


def test_simples():
    xml_esperado = (
            '<MP>'
            '<cMP>01</cMP>'
            '<vMP>10.00</vMP>'
            '</MP>'
        )
    mp = MeioPagamento(cMP='01', vMP=Decimal('10.00'))
    assert ET.tostring(mp._xml(), encoding='unicode') == xml_esperado


def test_simples_com_adm_cartao():
    xml_esperado = (
            '<MP>'
            '<cMP>01</cMP>'
            '<vMP>10.00</vMP>'
            '<cAdmC>999</cAdmC>'
            '</MP>'
        )
    mp = MeioPagamento(cMP='01', vMP=Decimal('10.00'), cAdmC='999')
    assert ET.tostring(mp._xml(), encoding='unicode') == xml_esperado
