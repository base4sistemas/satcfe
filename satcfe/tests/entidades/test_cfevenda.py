# -*- coding: utf-8 -*-
#
# satcfe/tests/entidades/test_cfevenda.py
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
from satcfe.entidades import CFeVenda
from satcfe.entidades import Emitente


def test_simples_minimo():
    xml_esperado = (
            '<CFe>'
            '<infCFe versaoDadosEnt="0.07">'
            '<ide>'
            '<CNPJ>08427847000169</CNPJ>'
            '<signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>'
            '<numeroCaixa>001</numeroCaixa>'
            '</ide>'
            '<emit>'
            '<CNPJ>61099008000141</CNPJ>'
            '<IE>111111111111</IE>'
            '<IM>12345</IM>'
            '<cRegTribISSQN>3</cRegTribISSQN>'
            '<indRatISSQN>N</indRatISSQN>'
            '</emit>'
            '<dest />'
            '<total /><pgto />'
            '</infCFe>'
            '</CFe>'
        )
    cfe = CFeVenda(
            CNPJ='08427847000169',
            signAC=constantes.ASSINATURA_AC_TESTE,
            numeroCaixa=1,
            emitente=Emitente(
                    CNPJ='61099008000141',
                    IE='111111111111',
                    IM='12345',
                    cRegTribISSQN=constantes.C15_SOCIEDADE_PROFISSIONAIS,
                    indRatISSQN=constantes.C16_NAO_RATEADO))
    assert ET.tostring(cfe._xml(), encoding='unicode') == xml_esperado
