# -*- coding: utf-8 -*-
#
# satcfe/excecoes.py
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

from .util import as_ascii


class ErroRespostaSATInvalida(Exception):
    """
    Lançada quando a resposta dada por uma função da DLL SAT não contém
    informação que faça sentido dentro do contexto. Este erro é diferente de
    uma :exc:`ExcecaoRespostaSAT` que é lançada quando a resposta faz sentido
    mas é interpretada como uma exceção a um comando que falhou.
    """
    pass


class ExcecaoRespostaSAT(Exception):
    """
    Lançada quando uma resposta à uma função da DLL SAT (comando SAT) é
    interpretada como tendo falhado. São casos em que a resposta é perfeitamente
    válida mas é interpretada como falha.

    Por exemplo, quando a função ``ConsultarSAT`` é invocada e a resposta
    indica um código ``EEEEE`` diferente de ``08000``, então uma exceção como
    esta será lançada.
    """

    def __init__(self, resposta):

        super(ExcecaoRespostaSAT, self).__init__(
                '%s, numeroSessao=%s, EEEEE="%s", mensagem="%s", '
                'cod="%s", mensagemSEFAZ="%s"' % (
                        resposta.atributos.funcao or 'F(?)',
                        as_ascii(getattr(resposta, 'numeroSessao', '?')),
                        as_ascii(getattr(resposta, 'EEEEE', '?')),
                        as_ascii(getattr(resposta, 'mensagem', '?')),
                        as_ascii(getattr(resposta, 'cod', '?')),
                        as_ascii(getattr(resposta, 'mensagemSEFAZ', '?')),))
        self._resposta = resposta


    @property
    def resposta(self):
        return self._resposta
