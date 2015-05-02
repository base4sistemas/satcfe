# -*- coding: utf-8 -*-
#
# satcfe/test/ft/dimep/d-sat/test_d-sat.py
#
# Copyright 2015 Base4 Sistemas Ltda ME
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

import os
import sys

import pytest

from satcomum.constantes import WINDOWS_STDCALL

# assume plataforma windows, por enquanto
pytestmark = pytest.mark.skipif(
        sys.platform != 'win32',
        reason='requires Microsoft Windows')

# define os atributos que serão lidos pelas fixtures
convencao = WINDOWS_STDCALL # será lido pela fixture fsat
caminho_dll = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
        'kit', 'windows', 'dllsat.dll') # será lido pela fixture fsat


def test_consultar_sat(fsat):
    resposta = fsat.consultar_sat()


def test_consultar_status_operacional(fsat):
    pass


def test_teste_fim_a_fim(fimafim, fsat):
    pass
