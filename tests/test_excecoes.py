# -*- coding: utf-8 -*-
#
# tests/test_excecoes.py
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

from satcfe.excecoes import ExcecaoRespostaSAT


class _MockRespostaSAT(object):

    class Atributos(object):
        pass

    def __init__(self):
        self.numeroSessao = '123456'
        self.EEEEE = ''
        self.mensagem = 'Mensagem com acentuação'
        self.cod = '0'
        self.mensagemSEFAZ = 'Mensagem com acentuação da SEFAZ'
        self.atributos = _MockRespostaSAT.Atributos()
        self.atributos.funcao = 'FuncaoTeste'


def test_excecao_resposta_sat():
    resposta = _MockRespostaSAT()

    try:
        raise ExcecaoRespostaSAT(resposta)
    except ExcecaoRespostaSAT as ex:
        assert ex.resposta is resposta
        assert str(ex) == (
                '{}, numeroSessao={!r}, EEEEE={!r}, mensagem={!r}, '
                'cod={!r}, mensagemSEFAZ={!r}'
            ).format(resposta.atributos.funcao,
                     resposta.numeroSessao,
                     resposta.EEEEE,
                     resposta.mensagem,
                     resposta.cod,
                     resposta.mensagemSEFAZ)
