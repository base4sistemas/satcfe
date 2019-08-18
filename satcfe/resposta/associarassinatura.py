# -*- coding: utf-8 -*-
#
# satcfe/resposta/associarassinatura.py
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

from builtins import str as text

from ..excecoes import ExcecaoRespostaSAT
from .padrao import RespostaSAT
from .padrao import analisar_retorno


class RespostaAssociarAssinatura(RespostaSAT):
    """Lida com as respostas da função ``AssociarAssinatura`` (veja o método
    :meth:`~satcfe.base.FuncoesSAT.associar_assinatura`). Os atributos
    esperados na resposta são:

    .. sourcecode:: text

        numeroSessao (int)
        EEEEE (text)
        CCCC (text)
        mensagem (text)
        cod (text)
        mensagemSEFAZ (text)

    .. note::

        Aqui, ``text`` diz respeito à um objeto ``unicode`` (Python 2) ou
        ``str`` (Python 3). Veja ``builtins.str`` da biblioteca ``future``.

    """

    @classmethod
    def analisar(cls, retorno):
        """Constrói uma instância da resposta a partir do retorno informado.

        :param str retorno: Retorno da função ``AssociarAssinatura``.
        """
        resposta = analisar_retorno(
                retorno,
                funcao='AssociarAssinatura',
                classe_resposta=RespostaAssociarAssinatura,
                campos=(
                        ('numeroSessao', int),
                        ('EEEEE', text),
                        ('CCCC', text),
                        ('mensagem', text),
                        ('cod', text),
                        ('mensagemSEFAZ', text),
                    ),
                campos_alternativos=[
                        # se a ativação falhar espera-se o padrão de campos
                        # no retorno (embora isto não esteja explícito na ER
                        # SAT, usa os campos padrão como um fallback razoável)
                        RespostaSAT.CAMPOS,
                    ]
            )
        if resposta.EEEEE not in ('13000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta
