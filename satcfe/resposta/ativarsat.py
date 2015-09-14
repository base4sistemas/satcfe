# -*- coding: utf-8 -*-
#
# satcfe/resposta/ativarsat.py
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

import base64

from satcomum.util import forcar_unicode

from ..excecoes import ExcecaoRespostaSAT
from .padrao import RespostaSAT
from .padrao import analisar_retorno


ATIVADO_CORRETAMENTE = '04000'
CSR_ICPBRASIL_CRIADO_SUCESSO = '04006'


class RespostaAtivarSAT(RespostaSAT):
    """Lida com as respostas da função ``AtivarSAT`` (veja o método
    :meth:`~satcfe.base.FuncoesSAT.ativar_sat`). Os atributos esperados em
    caso de sucesso, são:

    .. sourcecode:: text

        numeroSessao (int)
        EEEEE (unicode)
        mensagem (unicode)
        cod (unicode)
        mensagemSEFAZ (unicode)
        CSR (unicode)

    Em caso de falha, são esperados apenas os atributos padrão, conforme
    descrito na constante :attr:`~satcfe.resposta.padrao.RespostaSAT.CAMPOS`.
    """

    def csr(self):
        """Retorna o CSR (**Certificate Signing Request**) decodificado."""
        return base64.b64decode(self.CSR)


    @staticmethod
    def analisar(retorno):
        """Constrói uma :class:`RespostaAtivarSAT` a partir do retorno
        informado.

        :param unicode retorno: Retorno da função ``AtivarSAT``.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='AtivarSAT',
                classe_resposta=RespostaAtivarSAT,
                campos=(
                        ('numeroSessao', int),
                        ('EEEEE', unicode),
                        ('mensagem', unicode),
                        ('cod', unicode),
                        ('mensagemSEFAZ', unicode),
                        ('CSR', unicode),
                    ),
                campos_alternativos=[
                        # se a ativação falhar espera-se o padrão de campos
                        # no retorno...
                        RespostaSAT.CAMPOS,
                    ]
            )
        if resposta.EEEEE not in (
                ATIVADO_CORRETAMENTE,
                CSR_ICPBRASIL_CRIADO_SUCESSO,):
            raise ExcecaoRespostaSAT(resposta)
        return resposta
