# -*- coding: utf-8 -*-
#
# satcfe/tests/test_consultarsat.py
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
import pytest

from unidecode import unidecode


@pytest.mark.skipif(
        pytest.config.getoption('--skip-consultarsat') or
        pytest.config.getoption('--skip-funcoes-sat'),
        reason='Funcao `ConsultarSAT` explicitamente ignorada')
def test_consultarsat(clientesatlocal):
    resposta = clientesatlocal.consultar_sat()
    assert resposta.EEEEE in ('08000',)
    assert unidecode(resposta.mensagem) == 'SAT em operacao'
