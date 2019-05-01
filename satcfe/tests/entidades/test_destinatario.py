# -*- coding: utf-8 -*-
#
# satcfe/tests/entidades/test_destinatario.py
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

import pytest
import cerberus

from satcfe.entidades import Destinatario


def test_sem_destinario():
    dest = Destinatario()
    assert ET.tostring(dest._xml(), encoding='unicode') == '<dest />'


def test_simples_minimo():
    xml_esperado = (
            '<dest>'
            '<CNPJ>08427847000169</CNPJ>'
            '</dest>'
        )
    dest = Destinatario(CNPJ='08427847000169')
    assert ET.tostring(dest._xml(), encoding='unicode') == xml_esperado


def test_simples():
    xml_esperado = (
            '<dest>'
            '<CPF>11122233396</CPF>'
            '<xNome>Fulano Beltrano</xNome>'
            '</dest>'
        )
    dest = Destinatario(CPF='11122233396', xNome='Fulano Beltrano')
    assert ET.tostring(dest._xml(), encoding='unicode') == xml_esperado


def test_cnpj_e_cpf_sao_mutuamente_exclusivos():
    # note que ambos, CNPJ e CPF, são válidos...
    dest = Destinatario(
            CNPJ='08427847000169',
            CPF='11122233396')

    with pytest.raises(cerberus.DocumentError):
        dest._xml()


def test_cnpj_invalido():
    dest = Destinatario(CNPJ='08427847000160')
    with pytest.raises(cerberus.DocumentError):
        dest._xml()

    assert dest.__class__.__name__ in dest._erros
    assert 'CNPJ' in dest._erros[dest.__class__.__name__]


def test_cpf_invalido():
    dest = Destinatario(CPF='11122233390')
    with pytest.raises(cerberus.DocumentError):
        dest._xml()

    assert dest.__class__.__name__ in dest._erros
    assert 'CPF' in dest._erros[dest.__class__.__name__]


def test_destinatario_para_cancelamento():
    # no XML de cancelamento, o nome deverá ser ignorado
    dest = Destinatario(CPF='11122233396', xNome=u'Fulano Beltrano')
    assert ET.tostring(dest._xml(cancelamento=True), encoding='unicode') == (
            '<dest><CPF>11122233396</CPF></dest>'
        )
