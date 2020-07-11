# -*- coding: utf-8 -*-
#
# tests/entidades/test_destinatario.py
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

from satcfe.entidades import Destinatario


def test_sem_destinario():
    """XML esperado:

    .. sourcecode:: xml

        <dest />

    """
    dest = Destinatario()
    el = dest._xml()  # xml.etree.ElementTree.Element
    assert el is not None
    assert el.tag == 'dest'
    assert len(list(el)) == 0


def test_simples_minimo():
    """XML esperado:

    .. sourcecode:: xml

        <dest>
            <CNPJ>08427847000169</CNPJ>
        </dest>

    """
    dest = Destinatario(CNPJ='08427847000169')
    el = dest._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'dest'
    assert el.find('CNPJ').text == '08427847000169'


def test_simples():
    """XML esperado:

    .. sourcecode:: xml

        <dest>
            <CPF>11122233396</CPF>
            <xNome>Fulano Beltrano</xNome>
        </dest>

    """
    dest = Destinatario(CPF='11122233396', xNome='Fulano Beltrano')
    el = dest._xml()  # xml.etree.ElementTree.Element
    assert el.tag == 'dest'
    assert el.find('CPF').text == '11122233396'
    assert el.find('xNome').text == 'Fulano Beltrano'


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
    """No XML de cancelamento, o nome deverá ser ignorado. XML esperado:

    .. sourcecode:: xml

        <dest>
            <CPF>11122233396</CPF>
        </dest>

    """
    dest = Destinatario(CPF='11122233396', xNome='Fulano Beltrano')
    el = dest._xml(cancelamento=True)  # xml.etree.ElementTree.Element
    assert el.tag == 'dest'
    assert el.find('xNome') is None
    assert el.find('CPF').text == '11122233396'
