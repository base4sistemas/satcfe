# -*- coding: utf-8 -*-
#
# satcfe/tests/entidades/test_descacrentr.py
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

import cerberus
import pytest

from satcfe.entidades import DescAcrEntr


def test_simples_minimo():
    grupo = DescAcrEntr()
    assert ET.tostring(grupo._xml(), encoding='unicode') == '<DescAcrEntr />'


def test_acrescimo_no_subtotal():
    xml_esperado = (
            '<DescAcrEntr>'
            '<vAcresSubtot>0.02</vAcresSubtot>'
            '</DescAcrEntr>'
        )
    grupo = DescAcrEntr(vAcresSubtot=Decimal('0.02'))
    assert ET.tostring(grupo._xml(), encoding='unicode') == xml_esperado


def test_desconto_no_subtotal():
    xml_esperado = (
            '<DescAcrEntr>'
            '<vDescSubtot>0.01</vDescSubtot>'
            '</DescAcrEntr>'
        )
    grupo = DescAcrEntr(vDescSubtot=Decimal('0.01'))
    assert ET.tostring(grupo._xml(), encoding='unicode') == xml_esperado


def test_atributos_mutuamente_exclusivos():
    grupo = DescAcrEntr(
            vDescSubtot=Decimal('0.01'),
            vAcresSubtot=Decimal('0.02'))
    with pytest.raises(cerberus.DocumentError):
        grupo._xml()
