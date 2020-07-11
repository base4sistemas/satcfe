# -*- coding: utf-8 -*-
#
# tests/entidades/test_imposto.py
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

import cerberus
import pytest

from satcfe.entidades import ICMS00
from satcfe.entidades import PISSN
from satcfe.entidades import COFINSSN
from satcfe.entidades import Imposto


def test_simples():
    """XML esperado:

    .. sourcecode:: xml

        <imposto>
            <vItem12741>0.10</vItem12741>
            <ICMS>
                <ICMS00>
                    <Orig>0</Orig>
                    <CST>00</CST>
                    <pICMS>18.00</pICMS>
                </ICMS00>
            </ICMS>
            <PIS>
                <PISSN>
                    <CST>49</CST>
                </PISSN>
            </PIS>
            <COFINS>
                <COFINSSN>
                    <CST>49</CST>
                </COFINSSN>
            </COFINS>
        </imposto>

    """
    imposto = Imposto(
            vItem12741=Decimal('0.10'),
            icms=ICMS00(Orig='0', CST='00', pICMS=Decimal('18.00')),
            pis=PISSN(CST='49'),
            cofins=COFINSSN(CST='49'))
    el = imposto._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'imposto'
    assert el.find('vItem12741').text == '0.10'

    el_ICMS = el.find('ICMS')
    el_ICMS00 = el_ICMS.find('ICMS00')
    assert el_ICMS00.find('Orig').text == '0'
    assert el_ICMS00.find('CST').text == '00'
    assert el_ICMS00.find('pICMS').text == '18.00'

    el_PIS = el.find('PIS')
    el_PISSN = el_PIS.find('PISSN')
    assert el_PISSN.find('CST').text == '49'

    el_COFINS = el.find('COFINS')
    el_COFINSSN = el_COFINS.find('COFINSSN')
    assert el_COFINSSN.find('CST').text == '49'


def test_sem_pis():
    imposto = Imposto(cofins=COFINSSN(CST='49'))
    with pytest.raises(cerberus.DocumentError):
        imposto._xml()


def test_sem_cofins():
    imposto = Imposto(pis=PISSN(CST='49'))
    with pytest.raises(cerberus.DocumentError):
        imposto._xml()
