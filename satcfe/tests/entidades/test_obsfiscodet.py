# -*- coding: utf-8 -*-
#
# satcfe/tests/entidades/test_obsfiscodet.py
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

from satcfe.entidades import ObsFiscoDet


def test_simples():
    xml_esperado = (
            '<obsFiscoDet xCampoDet="Cod. Produto ANP">'
            '<xTextoDet>320101001</xTextoDet>'
            '</obsFiscoDet>'
        )
    obs = ObsFiscoDet(xCampoDet='Cod. Produto ANP', xTextoDet='320101001')
    assert ET.tostring(obs._xml(), encoding='unicode') == xml_esperado