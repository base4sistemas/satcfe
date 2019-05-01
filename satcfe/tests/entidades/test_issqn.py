# -*- coding: utf-8 -*-
#
# satcfe/tests/entidades/test_issqn.py
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

from satcfe.entidades import ISSQN


def test_simples_minimo():
    xml_esperado = (
            '<ISSQN>'
            '<vDeducISSQN>10.00</vDeducISSQN>'
            '<vAliq>7.00</vAliq>'
            '<cNatOp>01</cNatOp>'
            '<indIncFisc>2</indIncFisc>'
            '</ISSQN>'
        )
    issqn = ISSQN(
            vDeducISSQN=Decimal('10.00'),
            vAliq=Decimal('7.00'),
            cNatOp='01',
            indIncFisc='2')
    assert ET.tostring(issqn._xml(), encoding='unicode') == xml_esperado


def test_simples():
    xml_esperado = (
            '<ISSQN>'
            '<vDeducISSQN>10.00</vDeducISSQN>'
            '<vAliq>7.00</vAliq>'
            '<cMunFG>3511102</cMunFG>'
            '<cListServ>01.01</cListServ>'
            '<cServTribMun>01234567890123456789</cServTribMun>'
            '<cNatOp>01</cNatOp>'
            '<indIncFisc>2</indIncFisc>'
            '</ISSQN>'
        )
    issqn = ISSQN(
            vDeducISSQN=Decimal('10.00'),
            vAliq=Decimal('7.00'),
            cNatOp='01',
            indIncFisc='2',
            cMunFG='3511102',
            cListServ='01.01',
            cServTribMun='01234567890123456789')
    assert ET.tostring(issqn._xml(), encoding='unicode') == xml_esperado
