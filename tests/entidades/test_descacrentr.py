# -*- coding: utf-8 -*-
#
# tests/entidades/test_descacrentr.py
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

from satcfe.entidades import DescAcrEntr


def test_simples_minimo():
    """XML esperado:

    .. sourcecode:: xml

        <DescAcrEntr />

    """
    grupo = DescAcrEntr()
    el = grupo._xml()  # xml.etree.ElementTree.Element
    assert el is not None
    assert el.tag == 'DescAcrEntr'
    assert len(list(el)) == 0


def test_acrescimo_no_subtotal():
    """XML esperado:

    .. sourcecode:: xml

        <DescAcrEntr>
            <vAcresSubtot>0.02</vAcresSubtot>
        </DescAcrEntr>

    """
    grupo = DescAcrEntr(vAcresSubtot=Decimal('0.02'))
    el = grupo._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'DescAcrEntr'
    assert el.find('vAcresSubtot').text == '0.02'


def test_desconto_no_subtotal():
    """XML esperado:

    .. sourcecode:: xml

        <DescAcrEntr>
            <vDescSubtot>0.01</vDescSubtot>
        </DescAcrEntr>

    """
    grupo = DescAcrEntr(vDescSubtot=Decimal('0.01'))
    el = grupo._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'DescAcrEntr'
    assert el.find('vDescSubtot').text == '0.01'


def test_atributos_mutuamente_exclusivos():
    grupo = DescAcrEntr(
            vDescSubtot=Decimal('0.01'),
            vAcresSubtot=Decimal('0.02'))
    with pytest.raises(cerberus.DocumentError):
        grupo._xml()
