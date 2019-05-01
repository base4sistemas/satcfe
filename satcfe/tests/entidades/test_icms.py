# -*- coding: utf-8 -*-
#
# satcfe/tests/entidades/test_icms.py
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

from satcfe.entidades import ICMS00
from satcfe.entidades import ICMS40
from satcfe.entidades import ICMSSN102
from satcfe.entidades import ICMSSN900


def test_ICMS00():
    xml_esperado = (
            '<ICMS00>'
            '<Orig>0</Orig>'
            '<CST>00</CST>'
            '<pICMS>18.00</pICMS>'
            '</ICMS00>'
        )
    icms = ICMS00(Orig='0', CST='00', pICMS=Decimal('18.00'))
    assert ET.tostring(icms._xml(), encoding='unicode') == xml_esperado


def test_ICMS40():
    xml_esperado = '<ICMS40><Orig>0</Orig><CST>60</CST></ICMS40>'
    icms = ICMS40(Orig='0', CST='60')
    assert ET.tostring(icms._xml(), encoding='unicode') == xml_esperado


def test_ICMSSN102():
    xml_esperado = '<ICMSSN102><Orig>0</Orig><CSOSN>500</CSOSN></ICMSSN102>'
    icms = ICMSSN102(Orig='0', CSOSN='500')
    assert ET.tostring(icms._xml(), encoding='unicode') == xml_esperado


def test_ICMSSN900():
    xml_esperado = (
            '<ICMSSN900>'
            '<Orig>0</Orig>'
            '<CSOSN>900</CSOSN>'
            '<pICMS>18.00</pICMS>'
            '</ICMSSN900>'
        )
    icms = ICMSSN900(Orig='0', CSOSN='900', pICMS=Decimal('18.00'))
    assert ET.tostring(icms._xml(), encoding='unicode') == xml_esperado
