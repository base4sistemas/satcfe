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
import xml.etree.ElementTree as ET

from io import StringIO

from satcomum.ersat import dados_qrcode

from ..excecoes import ExcecaoRespostaSAT
from ..util import as_datetime
from ..util import base64_to_str
from .padrao import RespostaSAT
from .padrao import analisar_retorno


EMITIDO_COM_SUCESSO = '09000'


class RespostaTesteFimAFim(RespostaSAT):
    """Lida com as respostas da função ``TesteFimAFim`` (veja o método
    :meth:`~satcfe.base.FuncoesSAT.teste_fim_a_fim`). Os atributos
    esperados em caso de sucesso, são:

    .. sourcecode:: text

        numeroSessao (int)
        EEEEE (str)
        mensagem (str)
        cod (str)
        mensagemSEFAZ (str)
        arquivoCFeBase64 (str)
        timeStamp (datetime.datetime)
        numDocFiscal (int)
        chaveConsulta (str)

    Em caso de falha, são esperados apenas os atributos padrão, conforme
    descrito na constante :attr:`~satcfe.resposta.padrao.RespostaSAT.CAMPOS`.
    """

    def xml(self):
        """Retorna o XML do CF-e-SAT decodificado.

        :rtype: str
        """
        if self._sucesso():
            return base64_to_str(self.arquivoCFeBase64)
        else:
            raise ExcecaoRespostaSAT(self)

    def qrcode(self):
        """Resulta nos dados que compõem o QRCode.

        :rtype: str
        """
        if self._sucesso():
            tree = ET.parse(StringIO(self.xml()))
            return dados_qrcode(tree)
        else:
            raise ExcecaoRespostaSAT(self)

    def _sucesso(self):
        return self.EEEEE == EMITIDO_COM_SUCESSO

    @staticmethod
    def analisar(retorno):
        """Constrói uma :class:`RespostaTesteFimAFim` a partir do retorno
        informado.

        :param str retorno: Retorno da função ``TesteFimAFim``.

        :raises ExcecaoRespostaSAT: Se o atributo ``EEEEE`` não indicar o
            código de sucesso ``09000`` para ``TesteFimAFim``.
        """
        resposta = analisar_retorno(
                retorno,
                funcao='TesteFimAFim',
                classe_resposta=RespostaTesteFimAFim,
                campos=(
                        ('numeroSessao', int),
                        ('EEEEE', str),
                        ('mensagem', str),
                        ('cod', str),
                        ('mensagemSEFAZ', str),
                        ('arquivoCFeBase64', str),
                        ('timeStamp', as_datetime),
                        ('numDocFiscal', int),
                        ('chaveConsulta', str),
                    ),
                campos_alternativos=[
                        RespostaSAT.CAMPOS,
                    ]
            )
        if resposta.EEEEE not in (EMITIDO_COM_SUCESSO,):
            raise ExcecaoRespostaSAT(resposta)
        return resposta
