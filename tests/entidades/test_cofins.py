# -*- coding: utf-8 -*-
#
# tests/entidades/test_cofins.py
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

from satcfe.entidades import COFINSAliq
from satcfe.entidades import COFINSQtde
from satcfe.entidades import COFINSNT
from satcfe.entidades import COFINSSN
from satcfe.entidades import COFINSOutr
from satcfe.entidades import COFINSST


def test_COFINSAliq():
    """XML esperado:

    .. sourcecode:: xml

        <COFINSAliq>
            <CST>01</CST>
            <vBC>1.00</vBC>
            <pCOFINS>0.0065</pCOFINS>
        </COFINSAliq>

    """
    cofins = COFINSAliq(
            CST='01',
            vBC=Decimal('1.00'),
            pCOFINS=Decimal('0.0065'))

    el = cofins._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'COFINSAliq'
    assert el.find('CST').text == '01'
    assert el.find('vBC').text == '1.00'
    assert el.find('pCOFINS').text == '0.0065'


def test_COFINSQtde():
    """XML esperado:

    .. sourcecode:: xml

        <COFINSQtde>
            <CST>03</CST>
            <qBCProd>100.0000</qBCProd>
            <vAliqProd>0.6500</vAliqProd>
        </COFINSQtde>

    """
    cofins = COFINSQtde(
            CST='03',
            qBCProd=Decimal('100.0000'),
            vAliqProd=Decimal('0.6500'))

    el = cofins._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'COFINSQtde'
    assert el.find('CST').text == '03'
    assert el.find('qBCProd').text == '100.0000'
    assert el.find('vAliqProd').text == '0.6500'


def test_COFINSNT():
    """XML esperado:

    .. sourcecode:: xml

        <COFINSNT>
            <CST>04</CST>
        </COFINSNT>

    """
    cofins = COFINSNT(CST='04')
    el = cofins._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'COFINSNT'
    assert el.find('CST').text == '04'


def test_COFINSSN():
    """XML esperado:

    .. sourcecode:: xml

        <COFINSSN>
            <CST>49</CST>
        </COFINSSN>

    """
    cofins = COFINSSN(CST='49')
    el = cofins._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'COFINSSN'
    assert el.find('CST').text == '49'


def test_COFINSOutr_simples_vBC():
    """XML esperado:

    .. sourcecode:: xml

        <COFINSOutr>
            <CST>99</CST>
            <vBC>1.00</vBC>
            <pCOFINS>0.0065</pCOFINS>
        </COFINSOutr>

    """
    cofins = COFINSOutr(
            CST='99',
            vBC=Decimal('1.00'),
            pCOFINS=Decimal('0.0065'))
    el = cofins._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'COFINSOutr'
    assert el.find('CST').text == '99'
    assert el.find('vBC').text == '1.00'
    assert el.find('pCOFINS').text == '0.0065'


def test_COFINSOutr_simples_qBCProd():
    """XML esperado:

    .. sourcecode:: xml

        <COFINSOutr>
            <CST>99</CST>
            <qBCProd>100.0000</qBCProd>
            <vAliqProd>0.6500</vAliqProd>
        </COFINSOutr>

    """
    cofins = COFINSOutr(
            CST='99',
            qBCProd=Decimal('100.0000'),
            vAliqProd=Decimal('0.6500'))
    el = cofins._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'COFINSOutr'
    assert el.find('CST').text == '99'
    assert el.find('qBCProd').text == '100.0000'
    assert el.find('vAliqProd').text == '0.6500'


def test_COFINSOutr_vBC_sem_pCOFINS():
    # atributo vBC depende de pCOFINS que não foi informado
    cofins = COFINSOutr(CST='99', vBC=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        cofins._xml()


def test_COFINSOutr_qBCProd_sem_vAliqProd():
    # atributo qBCProd depende de vAliqProd que não foi informado
    cofins = COFINSOutr(CST='99', qBCProd=Decimal('100.0000'))
    with pytest.raises(cerberus.DocumentError):
        cofins._xml()


def test_COFINSOutr_sem_vBC_nem_qBCProd():
    # deve falhar pois vBC nem qBCProd foram informados
    cofins = COFINSOutr(CST='99')
    with pytest.raises(cerberus.DocumentError):
        cofins._xml()


def test_COFINSOutr_vBC_e_qBCProd_sao_mutuamente_exclusivos():
    # deve falhar pois apenas um ou outro grupo pode ser informado: ou
    # informa-se vBC e pCOFINS ou informa-se qBCProd e vAliqProd
    cofins = COFINSOutr(
            CST='99',
            vBC=Decimal('1.00'),
            pCOFINS=Decimal('1.00'),
            qBCProd=Decimal('1.00'),
            vAliqProd=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        cofins._xml()


def test_COFINSOutr_pCOFINS_sem_vBC():
    # o atributo pCOFINS requer que vBC tenha sido informado
    cofins = COFINSOutr(CST='99', pCOFINS=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        cofins._xml()


def test_COFINSOutr_vAliqProd_sem_qBCProd():
    # o atributo vAliqProd requer que qBCProd tenha sido informado
    cofins = COFINSOutr(CST='99', vAliqProd=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        cofins._xml()


def test_COFINSST_simples_vBC():
    """XML esperado:

    .. sourcecode:: xml

        <COFINSST>
            <vBC>1.00</vBC>
            <pCOFINS>0.0065</pCOFINS>
        </COFINSST>

    """
    cofins = COFINSST(vBC=Decimal('1.00'), pCOFINS=Decimal('0.0065'))
    el = cofins._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'COFINSST'
    assert el.find('CST') is None
    assert el.find('vBC').text == '1.00'
    assert el.find('pCOFINS').text == '0.0065'


def test_COFINSST_simples_qBCProd():
    """XML esperado:

    .. sourcecode:: xml

        <COFINSST>
            <qBCProd>100.0000</qBCProd>
            <vAliqProd>0.6500</vAliqProd>
        </COFINSST>

    """
    cofins = COFINSST(
            qBCProd=Decimal('100.0000'),
            vAliqProd=Decimal('0.6500'))
    el = cofins._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'COFINSST'
    assert el.find('CST') is None
    assert el.find('qBCProd').text == '100.0000'
    assert el.find('vAliqProd').text == '0.6500'


def test_COFINSST_vBC_sem_pCOFINS():
    # atributo vBC depende de pCOFINS que não foi informado
    cofins = COFINSST(vBC=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        cofins._xml()


def test_COFINSST_qBCProd_sem_vAliqProd():
    # atributo qBCProd depende de vAliqProd que não foi informado
    cofins = COFINSST(qBCProd=Decimal('100.0000'))
    with pytest.raises(cerberus.DocumentError):
        cofins._xml()


def test_COFINSST_sem_vBC_nem_qBCProd():
    # deve falhar pois vBC nem qBCProd foram informados
    cofins = COFINSST()
    with pytest.raises(cerberus.DocumentError):
        cofins._xml()


def test_COFINSST_vBC_e_qBCProd_sao_mutuamente_exclusivos():
    # deve falhar pois apenas um ou outro grupo pode ser informado: ou
    # informa-se vBC e pCOFINS ou informa-se qBCProd e vAliqProd
    cofins = COFINSST(
            vBC=Decimal('1.00'),
            pCOFINS=Decimal('1.00'),
            qBCProd=Decimal('1.00'),
            vAliqProd=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        cofins._xml()


def test_COFINSST_pCOFINS_sem_vBC():
    # o atributo pCOFINS requer que vBC tenha sido informado
    cofins = COFINSST(pCOFINS=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        cofins._xml()


def test_COFINSST_vAliqProd_sem_qBCProd():
    # o atributo vAliqProd requer que qBCProd tenha sido informado
    cofins = COFINSST(vAliqProd=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        cofins._xml()
