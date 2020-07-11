# -*- coding: utf-8 -*-
#
# tests/test_rede.py
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

from satcomum import constantes
from satcfe.rede import ConfiguracaoRede


def test_configuracao_rede():
    """XML esperado:

    .. sourcecode:: xml

        <config>
            <tipoInter>ETHE</tipoInter>
            <tipoLan>DHCP</tipoLan>
        </config>

    """
    conf = ConfiguracaoRede(
            tipoInter=constantes.REDE_TIPOINTER_ETHE,
            tipoLan=constantes.REDE_TIPOLAN_DHCP)

    el = conf._xml()  # xml.etree.ElementTree.Element
    assert el.find('tipoInter').text == constantes.REDE_TIPOINTER_ETHE
    assert el.find('tipoLan').text == constantes.REDE_TIPOLAN_DHCP
