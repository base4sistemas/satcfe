# -*- coding: utf-8 -*-
#
# satcfe/tests/entidades/test_localentrega.py
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

from satcfe.entidades import LocalEntrega


def test_simples_minimo():
    xml_esperado = (
            '<entrega>'
            '<xLgr>Rua Armando Gulim</xLgr>'
            '<nro>65</nro>'
            '<xBairro>Parque Glória III</xBairro>'
            '<xMun>Catanduva</xMun>'
            '<UF>SP</UF>'
            '</entrega>'
        )
    local = LocalEntrega(
            xLgr='Rua Armando Gulim',
            nro='65',
            xBairro='Parque Glória III',
            xMun='Catanduva',
            UF='SP')
    assert ET.tostring(local._xml(), encoding='unicode') == xml_esperado


def test_uf_invalida():
    local = LocalEntrega(
            xLgr='Rua Armando Gulim',
            nro='65',
            xBairro='Parque Glória III',
            xMun='Catanduva',
            UF='XX')

    with pytest.raises(cerberus.DocumentError):
        local._xml()

    assert local.__class__.__name__ in local._erros
    assert 'UF' in local._erros[local.__class__.__name__]
