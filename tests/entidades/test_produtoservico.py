# -*- coding: utf-8 -*-
#
# tests/entidades/test_produtoservico.py
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

import pytest
import cerberus

from satcomum import constantes

from satcfe.entidades import ProdutoServico


def test_simples():
    """XML esperado:

    .. sourcecode:: xml

        <prod>
            <cProd>123456</cProd>
            <xProd>BORRACHA STAEDTLER</xProd>
            <CFOP>5102</CFOP>
            <uCom>UN</uCom>
            <qCom>1.0000</qCom>
            <vUnCom>5.75</vUnCom>
            <indRegra>A</indRegra>
        </prod>

    """
    prod = ProdutoServico(
            cProd='123456',
            xProd='BORRACHA STAEDTLER',
            CFOP='5102',
            uCom='UN',
            qCom=Decimal('1.0000'),
            vUnCom=Decimal('5.75'),
            indRegra=constantes.I11_ARREDONDAMENTO)
    # apenas os atributos requeridos; note que, diferente da NF-e/NFC-e a
    # ER SAT indica que o atributo NCM não é obrigatório no CF-e;

    el = prod._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'prod'
    assert el.find('cProd').text == '123456'
    assert el.find('xProd').text == 'BORRACHA STAEDTLER'
    assert el.find('CFOP').text == '5102'
    assert el.find('uCom').text == 'UN'
    assert el.find('qCom').text == '1.0000'
    assert el.find('vUnCom').text == '5.75'
    assert el.find('indRegra').text == constantes.I11_ARREDONDAMENTO


def test_todos_os_atributos_informando_vDesc():
    """XML esperado:

    .. sourcecode:: xml

        <prod>
            <cProd>123456</cProd>
            <cEAN>4007817525074</cEAN>
            <xProd>BORRACHA STAEDTLER</xProd>
            <NCM>40169200</NCM>
            <CFOP>5102</CFOP>
            <uCom>UN</uCom>
            <qCom>1.0000</qCom>
            <vUnCom>5.75</vUnCom>
            <indRegra>A</indRegra>
            <vDesc>0.25</vDesc>
        </prod>

    """
    prod = ProdutoServico(
            cProd='123456',
            xProd='BORRACHA STAEDTLER',
            cEAN='4007817525074',
            NCM='40169200',
            CFOP='5102',
            uCom='UN',
            qCom=Decimal('1.0000'),
            vUnCom=Decimal('5.75'),
            indRegra=constantes.I11_ARREDONDAMENTO,
            vDesc=Decimal('0.25'))

    # todos os atributos (se vDesc for informado, então não informa vOutro)
    el = prod._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'prod'
    assert el.find('cProd').text == '123456'
    assert el.find('xProd').text == 'BORRACHA STAEDTLER'
    assert el.find('cEAN').text == '4007817525074'
    assert el.find('NCM').text == '40169200'
    assert el.find('CFOP').text == '5102'
    assert el.find('uCom').text == 'UN'
    assert el.find('qCom').text == '1.0000'
    assert el.find('vUnCom').text == '5.75'
    assert el.find('indRegra').text == constantes.I11_ARREDONDAMENTO
    assert el.find('vDesc').text == '0.25'
    assert el.find('vOutro') is None


def test_todos_os_atributos_informando_vOutro():
    """XML esperado:

    .. sourcecode:: xml

            '<prod>'
            '<cProd>123456</cProd>'
            '<cEAN>4007817525074</cEAN>'
            '<xProd>BORRACHA STAEDTLER</xProd>'
            '<NCM>40169200</NCM>'
            '<CFOP>5102</CFOP>'
            '<uCom>UN</uCom>'
            '<qCom>1.0000</qCom>'
            '<vUnCom>5.75</vUnCom>'
            '<indRegra>A</indRegra>'
            '<vOutro>0.25</vOutro>'
            '</prod>'
    """
    prod = ProdutoServico(
            cProd='123456',
            cEAN='4007817525074',
            xProd='BORRACHA STAEDTLER',
            NCM='40169200',
            CFOP='5102',
            uCom='UN',
            qCom=Decimal('1.0000'),
            vUnCom=Decimal('5.75'),
            indRegra=constantes.I11_ARREDONDAMENTO,
            vOutro=Decimal('0.25'))

    # todos os atributos (se vOutro for informado, então não informa vDesc)
    el = prod._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'prod'
    assert el.find('cProd').text == '123456'
    assert el.find('xProd').text == 'BORRACHA STAEDTLER'
    assert el.find('cEAN').text == '4007817525074'
    assert el.find('NCM').text == '40169200'
    assert el.find('CFOP').text == '5102'
    assert el.find('uCom').text == 'UN'
    assert el.find('qCom').text == '1.0000'
    assert el.find('vUnCom').text == '5.75'
    assert el.find('indRegra').text == constantes.I11_ARREDONDAMENTO
    assert el.find('vDesc') is None
    assert el.find('vOutro').text == '0.25'


def test_informando_vDesc_e_vOutro():
    # informando vDesc e vOutro, não deve validar
    prod = ProdutoServico(
            cProd='123456',
            xProd='BORRACHA STAEDTLER',
            CFOP='5102',
            uCom='UN',
            qCom=Decimal('1.0000'),
            vUnCom=Decimal('5.75'),
            indRegra='A',
            vDesc=Decimal('0.25'),
            vOutro=Decimal('0.25'))

    with pytest.raises(cerberus.DocumentError):
        prod._xml()
