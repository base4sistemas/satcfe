# -*- coding: utf-8 -*-
#
# satcfe/tests/entidades/test_detalhamento.py
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

from satcfe.entidades import Detalhamento
from satcfe.entidades import ProdutoServico
from satcfe.entidades import Imposto
from satcfe.entidades import PISSN
from satcfe.entidades import COFINSSN
from satcfe.entidades import ICMSSN102


def test_simples():
    xml_esperado = (
            '<det nItem="1">'
            '<prod>'
            '<cProd>123456</cProd>'
            '<xProd>BORRACHA STAEDTLER</xProd>'
            '<CFOP>5102</CFOP>'
            '<uCom>UN</uCom>'
            '<qCom>1.0000</qCom>'
            '<vUnCom>5.75</vUnCom>'
            '<indRegra>A</indRegra>'
            '</prod>'
            '<imposto>'
            '<ICMS>'
            '<ICMSSN102>'
            '<Orig>2</Orig>'
            '<CSOSN>500</CSOSN>'
            '</ICMSSN102>'
            '</ICMS>'
            '<PIS>'
            '<PISSN>'
            '<CST>49</CST>'
            '</PISSN>'
            '</PIS>'
            '<COFINS>'
            '<COFINSSN>'
            '<CST>49</CST>'
            '</COFINSSN>'
            '</COFINS>'
            '</imposto>'
            '<infAdProd>Teste</infAdProd>'
            '</det>'
        )
    det = Detalhamento(
            produto=ProdutoServico(
                    cProd='123456',
                    xProd='BORRACHA STAEDTLER',
                    CFOP='5102',
                    uCom='UN',
                    qCom=Decimal('1.0000'),
                    vUnCom=Decimal('5.75'),
                    indRegra='A'),
            imposto=Imposto(
                    pis=PISSN(CST='49'),
                    cofins=COFINSSN(CST='49'),
                    icms=ICMSSN102(Orig='2', CSOSN='500')),
            infAdProd='Teste')
    assert ET.tostring(det._xml(nItem=1), encoding='unicode') == xml_esperado
