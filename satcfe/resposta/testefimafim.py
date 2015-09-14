# -*- coding: utf-8 -*-
#
# satcfe/resposta/testefimafim.py
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

from decimal import Decimal

from satcomum.ersat import dados_qrcode
from satcomum.util import forcar_unicode

from ..excecoes import ExcecaoRespostaSAT
from ..util import as_datetime
from .padrao import RespostaSAT
from .padrao import analisar_retorno


class RespostaTesteFimAFim(RespostaSAT):
    """Lida com as respostas da função ``TesteFimAFim`` (veja o método
    :meth:`~satcfe.base.FuncoesSAT.teste_fim_a_fim`). Os atributos
    esperados em caso de sucesso, são:

    .. sourcecode:: text

        numeroSessao (int)
        EEEEE (unicode)
        mensagem (unicode)
        cod (unicode)
        mensagemSEFAZ (unicode)
        arquivoCFeBase64 (unicode)
        timeStamp (datetime.datetime)
        numDocFiscal (int)
        chaveConsulta (unicode)

    Em caso de falha, são esperados apenas os atributos padrão, conforme
    descrito na constante :attr:`~satcfe.resposta.padrao.RespostaSAT.CAMPOS`.
    """

    def xml(self):
        """Retorna o XML do CF-e-SAT decodificado."""
        return base64.b64decode(self.arquivoCFeBase64)


    def qrcode(self):
        """Resulta nos dados que compõem o QRCode."""
        return dados_qrcode(self.xml())


    @staticmethod
    def analisar(retorno):
        """Constrói uma :class:`RespostaTesteFimAFim` a partir do retorno
        informado.

        :param unicode retorno: Retorno da função ``TesteFimAFim``.

        :raises ExcecaoRespostaSAT: Se o atributo ``EEEEE`` não indicar o
            código de sucesso ``09000`` para ``TesteFimAFim``.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='TesteFimAFim',
                classe_resposta=RespostaTesteFimAFim,
                campos=(
                        ('numeroSessao', int),
                        ('EEEEE', unicode),
                        ('mensagem', unicode),
                        ('cod', unicode),
                        ('mensagemSEFAZ', unicode),
                        ('arquivoCFeBase64', unicode),
                        ('timeStamp', as_datetime),
                        ('numDocFiscal', int),
                        ('chaveConsulta', unicode),
                    ),
                campos_alternativos=[
                        RespostaSAT.CAMPOS,
                    ]
            )
        if resposta.EEEEE not in ('09000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta
