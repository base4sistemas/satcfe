# -*- coding: utf-8 -*-
#
# satcfe/tests/entidades/test_pis.py
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

import pytest
import cerberus

from satcfe.entidades import PISAliq
from satcfe.entidades import PISQtde
from satcfe.entidades import PISNT
from satcfe.entidades import PISSN
from satcfe.entidades import PISOutr
from satcfe.entidades import PISST


def test_PISAliq():
    xml_esperado = (
            '<PISAliq>'
            '<CST>01</CST>'
            '<vBC>1.00</vBC>'
            '<pPIS>0.0065</pPIS>'
            '</PISAliq>'
        )
    pis = PISAliq(CST='01', vBC=Decimal('1.00'), pPIS=Decimal('0.0065'))
    assert ET.tostring(pis._xml(), encoding='unicode') == xml_esperado


def test_PISQtde():
    xml_esperado = (
            '<PISQtde>'
            '<CST>03</CST>'
            '<qBCProd>100.0000</qBCProd>'
            '<vAliqProd>0.6500</vAliqProd>'
            '</PISQtde>'
        )
    pis = PISQtde(
            CST='03',
            qBCProd=Decimal('100.0000'),
            vAliqProd=Decimal('0.6500'))
    assert ET.tostring(pis._xml(), encoding='unicode') == xml_esperado


def test_PISNT():
    xml_esperado = '<PISNT><CST>04</CST></PISNT>'
    pis = PISNT(CST='04')
    assert ET.tostring(pis._xml(), encoding='unicode') == xml_esperado


def test_PISSN():
    xml_esperado = '<PISSN><CST>49</CST></PISSN>'
    pis = PISSN(CST='49')
    assert ET.tostring(pis._xml(), encoding='unicode') == xml_esperado


def test_PISOutr_simples_vBC():
    xml_esperado = (
            '<PISOutr>'
            '<CST>99</CST>'
            '<vBC>1.00</vBC>'
            '<pPIS>0.0065</pPIS>'
            '</PISOutr>'
        )
    pis = PISOutr(CST='99', vBC=Decimal('1.00'), pPIS=Decimal('0.0065'))
    assert ET.tostring(pis._xml(), encoding='unicode') == xml_esperado


def test_PISOutr_simples_qBCProd():
    xml_esperado = (
            '<PISOutr>'
            '<CST>99</CST>'
            '<qBCProd>100.0000</qBCProd>'
            '<vAliqProd>0.6500</vAliqProd>'
            '</PISOutr>'
        )
    pis = PISOutr(
            CST='99',
            qBCProd=Decimal('100.0000'),
            vAliqProd=Decimal('0.6500'))
    assert ET.tostring(pis._xml(), encoding='unicode') == xml_esperado


def test_PISOutr_vBC_sem_pPIS():
    # atributo vBC depende de pPIS que não foi informado
    pis = PISOutr(CST='99', vBC=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        pis._xml()


def test_PISOutr_qBCProd_sem_vAliqProd():
    # atributo qBCProd depende de vAliqProd que não foi informado
    pis = PISOutr(CST='99', qBCProd=Decimal('100.0000'))
    with pytest.raises(cerberus.DocumentError):
        pis._xml()


def test_PISOutr_sem_vBC_nem_qBCProd():
    # deve falhar pois vBC nem qBCProd foram informados
    pis = PISOutr(CST='99')
    with pytest.raises(cerberus.DocumentError):
        pis._xml()


def test_PISOutr_vBC_e_qBCProd_sao_mutuamente_exclusivos():
    # deve falhar pois apenas um ou outro grupo pode ser informado: ou
    # informa-se vBC e pPIS ou informa-se qBCProd e vAliqProd
    pis = PISOutr(
            CST='99',
            vBC=Decimal('1.00'),
            pPIS=Decimal('1.00'),
            qBCProd=Decimal('1.00'),
            vAliqProd=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        pis._xml()


def test_PISOutr_pPIS_sem_vBC():
    # o atributo pPIS requer que vBC tenha sido informado
    pis = PISOutr(CST='99', pPIS=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        pis._xml()


def test_PISOutr_vAliqProd_sem_qBCProd():
    # o atributo vAliqProd requer que qBCProd tenha sido informado
    pis = PISOutr(CST='99', vAliqProd=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        pis._xml()


def test_PISST_simples_vBC():
    xml_esperado = (
            '<PISST>'
            '<vBC>1.00</vBC>'
            '<pPIS>0.0065</pPIS>'
            '</PISST>'
        )
    pis = PISST(vBC=Decimal('1.00'), pPIS=Decimal('0.0065'))
    assert ET.tostring(pis._xml(), encoding='unicode') == xml_esperado


def test_PISST_simples_qBCProd():
    xml_esperado = (
            '<PISST>'
            '<qBCProd>100.0000</qBCProd>'
            '<vAliqProd>0.6500</vAliqProd>'
            '</PISST>'
        )
    pis = PISST(
            qBCProd=Decimal('100.0000'),
            vAliqProd=Decimal('0.6500'))
    assert ET.tostring(pis._xml(), encoding='unicode') == xml_esperado


def test_PISST_vBC_sem_pPIS():
    # atributo vBC depende de pPIS que não foi informado
    pis = PISST(vBC=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        pis._xml()


def test_PISST_qBCProd_sem_vAliqProd():
    # atributo qBCProd depende de vAliqProd que não foi informado
    pis = PISST(qBCProd=Decimal('100.0000'))
    with pytest.raises(cerberus.DocumentError):
        pis._xml()


def test_PISST_sem_vBC_nem_qBCProd():
    # deve falhar pois vBC nem qBCProd foram informados
    pis = PISST()
    with pytest.raises(cerberus.DocumentError):
        pis._xml()


def test_PISST_vBC_e_qBCProd_sao_mutuamente_exclusivos():
    # deve falhar pois apenas um ou outro grupo pode ser informado: ou
    # informa-se vBC e pPIS ou informa-se qBCProd e vAliqProd
    pis = PISST(
            vBC=Decimal('1.00'),
            pPIS=Decimal('1.00'),
            qBCProd=Decimal('1.00'),
            vAliqProd=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        pis._xml()


def test_PISST_pPIS_sem_vBC():
    # o atributo pPIS requer que vBC tenha sido informado
    pis = PISST(pPIS=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        pis._xml()


def test_PISST_vAliqProd_sem_qBCProd():
    # o atributo vAliqProd requer que qBCProd tenha sido informado
    pis = PISST(vAliqProd=Decimal('1.00'))
    with pytest.raises(cerberus.DocumentError):
        pis._xml()
