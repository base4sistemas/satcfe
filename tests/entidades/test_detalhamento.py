# -*- coding: utf-8 -*-
#
# tests/entidades/test_detalhamento.py
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

from satcomum import constantes

from satcfe.entidades import Detalhamento
from satcfe.entidades import ProdutoServico
from satcfe.entidades import Imposto
from satcfe.entidades import PISSN
from satcfe.entidades import COFINSSN
from satcfe.entidades import ICMSSN102


def test_simples():
    """XML esperado:

    .. sourcecode:: xml

        <det nItem="1">
            <prod>
                <cProd>123456</cProd>
                <xProd>BORRACHA STAEDTLER</xProd>
                <CFOP>5102</CFOP>
                <uCom>UN</uCom>
                <qCom>1.0000</qCom>
                <vUnCom>5.75</vUnCom>
                <indRegra>A</indRegra>
            </prod>
            <imposto>
                <ICMS>
                    <ICMSSN102>
                        <Orig>2</Orig>
                        <CSOSN>500</CSOSN>
                    </ICMSSN102>
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
            <infAdProd>Teste</infAdProd>
        </det>

    """
    det = Detalhamento(
            produto=ProdutoServico(
                    cProd='123456',
                    xProd='BORRACHA STAEDTLER',
                    CFOP='5102',
                    uCom='UN',
                    qCom=Decimal('1.0000'),
                    vUnCom=Decimal('5.75'),
                    indRegra=constantes.I11_ARREDONDAMENTO),
            imposto=Imposto(
                    pis=PISSN(CST='49'),
                    cofins=COFINSSN(CST='49'),
                    icms=ICMSSN102(Orig='2', CSOSN='500')),
            infAdProd='Teste')

    el = det._xml(nItem=1)  # xml.etree.ElementTree.Element
    assert el.tag == 'det'

    assert el.attrib['nItem'] == '1'
    assert el.find('infAdProd').text == 'Teste'

    prod = el.find('prod')
    assert prod.find('cProd').text == '123456'
    assert prod.find('xProd').text == 'BORRACHA STAEDTLER'
    assert prod.find('CFOP').text == '5102'
    assert prod.find('uCom').text == 'UN'
    assert prod.find('qCom').text == '1.0000'
    assert prod.find('vUnCom').text == '5.75'
    assert prod.find('indRegra').text == constantes.I11_ARREDONDAMENTO

    imposto = el.find('imposto')

    el_ICMS = imposto.find('ICMS')
    el_ICMSSN102 = el_ICMS.find('ICMSSN102')
    assert el_ICMSSN102.find('Orig').text == '2'
    assert el_ICMSSN102.find('CSOSN').text == '500'

    el_PIS = imposto.find('PIS')
    el_PISSN = el_PIS.find('PISSN')
    assert el_PISSN.find('CST').text == '49'

    el_COFINS = imposto.find('COFINS')
    el_COFINSSN = el_COFINS.find('COFINSSN')
    assert el_COFINSSN.find('CST').text == '49'
