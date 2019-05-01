# -*- coding: utf-8 -*-
#
# satcfe/tests/entidades/test_cfecanc.py
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

from satcomum import constantes
from satcfe.entidades import CFeCancelamento


def test_simples_minimo():
    xml_esperado = (
            '<CFeCanc>'
            '<infCFe chCanc="CFe01234567890123456789012345678901234567890123">'
            '<ide>'
            '<CNPJ>08427847000169</CNPJ>'
            '<signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>'
            '<numeroCaixa>001</numeroCaixa>'
            '</ide>'
            '<emit />'
            '<dest />'
            '<total />'
            '</infCFe>'
            '</CFeCanc>'
        )
    cfecanc = CFeCancelamento(
            chCanc='CFe01234567890123456789012345678901234567890123',
            CNPJ='08427847000169',
            signAC=constantes.ASSINATURA_AC_TESTE,
            numeroCaixa=1)
    assert ET.tostring(cfecanc._xml(), encoding='unicode') == xml_esperado
