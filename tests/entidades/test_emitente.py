# -*- coding: utf-8 -*-
#
# tests/entidades/test_emitente.py
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

import pytest
import cerberus

from satcomum import constantes

from satcfe.entidades import Emitente


def test_simples_minimo():
    """XML esperado:

    .. sourcecode:: xml

        <emit>
            <CNPJ>08427847000169</CNPJ>
            <IE>111222333444</IE>
            <indRatISSQN>S</indRatISSQN>
        </emit>

    """
    emit = Emitente(
            CNPJ='08427847000169',
            IE='111222333444',
            indRatISSQN=constantes.C16_RATEADO)

    el = emit._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'emit'
    assert el.find('CNPJ').text == '08427847000169'
    assert el.find('IE').text == '111222333444'
    assert el.find('indRatISSQN').text == constantes.C16_RATEADO


def test_simples():
    """XML esperado:

    .. sourcecode:: xml

        <emit>
            <CNPJ>08427847000169</CNPJ>
            <IE>111222333444</IE>
            <IM>123456789012345</IM>
            <cRegTribISSQN>1</cRegTribISSQN>
            <indRatISSQN>S</indRatISSQN>
        </emit>

    """
    emit = Emitente(
            CNPJ='08427847000169',
            IE='111222333444',
            IM='123456789012345',
            cRegTribISSQN=constantes.C15_MICROEMPRESA_MUNICIPAL,
            indRatISSQN=constantes.C16_RATEADO)
    el = emit._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'emit'
    assert el.find('CNPJ').text == '08427847000169'
    assert el.find('IE').text == '111222333444'
    assert el.find('IM').text == '123456789012345'
    assert el.find('indRatISSQN').text == constantes.C16_RATEADO
    assert el.find('cRegTribISSQN').text == (
            constantes.C15_MICROEMPRESA_MUNICIPAL
        )


def test_emitente_todos_atributos_invalidos():
    emit = Emitente(
            CNPJ='08427847000160',
            IE='111765567567822333444',  # mais de 12 digitos
            cRegTribISSQN='0',
            indRatISSQN='X')

    with pytest.raises(cerberus.DocumentError):
        emit.validar()

    assert emit.__class__.__name__ in emit._erros
    erros = emit._erros[emit.__class__.__name__]

    assert 'CNPJ' in erros
    assert 'IE' in erros
    assert 'cRegTribISSQN' in erros
    assert 'indRatISSQN' in erros
