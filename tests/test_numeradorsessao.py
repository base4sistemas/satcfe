# -*- coding: utf-8 -*-
#
# tests/test_numeradorsessao.py
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

from satcfe.base import NumeroSessaoMemoria


def test_numerador_sessao_memoria():
    numerador = NumeroSessaoMemoria(tamanho=5)

    n1 = numerador()
    assert 100000 <= n1 <= 999999, 'Numero de sessão deve possuir 6 digitos.'
    assert n1 in numerador

    n2 = numerador()
    n3 = numerador()
    n4 = numerador()
    n5 = numerador()
    assert len(set([n1, n2, n3, n4, n5])) == 5, (
            'Os números gerados não devem repetir-se.'
        )

    n6 = numerador()
    assert n6 in numerador
    assert n5 in numerador
    assert n4 in numerador
    assert n3 in numerador
    assert n2 in numerador

    assert n1 not in numerador, (
            'Ao esgotar-se o tamanho máximo do numerador, o primeiro número '
            'gerado deveria ter sido descartado (first in, first out).'
        )
