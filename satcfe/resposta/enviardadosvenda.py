# -*- coding: utf-8 -*-
#
# satcfe/resposta/enviardadosvenda.py
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
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import xml.etree.ElementTree as ET

from decimal import Decimal
from io import StringIO

from builtins import str as text

from satcomum.ersat import dados_qrcode

from ..excecoes import ExcecaoRespostaSAT
from ..util import as_datetime
from ..util import base64_to_str
from .padrao import RespostaSAT
from .padrao import analisar_retorno


EMITIDO_COM_SUCESSO = '06000'


class RespostaEnviarDadosVenda(RespostaSAT):
    """Lida com as respostas da função ``EnviarDadosVenda`` (veja o método
    :meth:`~satcfe.base.FuncoesSAT.enviar_dados_venda`). Os atributos
    esperados em caso de sucesso, são:

    .. sourcecode:: text

        numeroSessao (int)
        EEEEE (text)
        CCCC (text)
        mensagem (text)
        cod (text)
        mensagemSEFAZ (text)
        arquivoCFeSAT (text)
        timeStamp (datetime.datetime)
        chaveConsulta (text)
        valorTotalCFe (decimal.Decimal)
        CPFCNPJValue (text)
        assinaturaQRCODE (text)

    Em caso de falha, são esperados apenas os atributos:

    .. sourcecode:: text

        numeroSessao (int)
        EEEEE (text)
        CCCC (text)
        mensagem (text)
        cod (text)
        mensagemSEFAZ (text)

    Finalmente, como último recurso, a resposta poderá incluir apenas os
    atributos padrão, conforme descrito na constante
    :attr:`~satcfe.resposta.padrao.RespostaSAT.CAMPOS`.

    .. note::

        Aqui, ``text`` diz respeito à um objeto ``unicode`` (Python 2) ou
        ``str`` (Python 3). Veja ``builtins.str`` da biblioteca ``future``.

    """

    def xml(self):
        """Retorna o XML do CF-e-SAT decodificado de Base64.

        :rtype: str
        """
        if self._sucesso():
            return base64_to_str(self.arquivoCFeSAT)
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
        """Constrói uma :class:`RespostaEnviarDadosVenda` a partir do
        retorno informado.

        :param str retorno: Retorno da função ``EnviarDadosVenda``.
        """
        resposta = analisar_retorno(
                retorno,
                funcao='EnviarDadosVenda',
                classe_resposta=RespostaEnviarDadosVenda,
                campos=(
                        ('numeroSessao', int),
                        ('EEEEE', text),
                        ('CCCC', text),
                        ('mensagem', text),
                        ('cod', text),
                        ('mensagemSEFAZ', text),
                        ('arquivoCFeSAT', text),
                        ('timeStamp', as_datetime),
                        ('chaveConsulta', text),
                        ('valorTotalCFe', Decimal),
                        ('CPFCNPJValue', text),
                        ('assinaturaQRCODE', text),
                    ),
                campos_alternativos=[
                        # se a venda falhar apenas os primeiros seis campos
                        # especificados na ER deverão ser retornados...
                        (
                                ('numeroSessao', int),
                                ('EEEEE', text),
                                ('CCCC', text),
                                ('mensagem', text),
                                ('cod', text),
                                ('mensagemSEFAZ', text),
                        ),
                        # por via das dúvidas, considera o padrão de campos,
                        # caso não haja nenhuma coincidência...
                        RespostaSAT.CAMPOS,
                    ]
            )
        if resposta.EEEEE not in (EMITIDO_COM_SUCESSO,):
            raise ExcecaoRespostaSAT(resposta)
        return resposta
