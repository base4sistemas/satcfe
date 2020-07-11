# -*- coding: utf-8 -*-
#
# tests/test_resposta_padrao.py
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

from satcfe.resposta.padrao import analisar_retorno


def test_analisar_retorno_simples():
    retorno = '123456|08000|SAT em operacao||'
    resposta = analisar_retorno(retorno, funcao='ConsultarSAT')
    assert resposta.numeroSessao == 123456
    assert resposta.EEEEE == '08000'
    assert resposta.mensagem == 'SAT em operacao'
    assert resposta.cod == ''
    assert resposta.mensagemSEFAZ == ''
    assert resposta.atributos.funcao == 'ConsultarSAT'
    assert resposta.atributos.verbatim == '123456|08000|SAT em operacao||'
