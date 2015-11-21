# -*- coding: utf-8 -*-
#
# satcfe/resposta/cancelarultimavenda.py
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


class RespostaCancelarUltimaVenda(RespostaSAT):
    """Lida com as respostas da função ``CancelarUltimaVenda`` (veja o método
    :meth:`~satcfe.base.FuncoesSAT.cancelar_ultima_venda`). Os atributos
    esperados em caso de sucesso, são:

    .. sourcecode:: text

        numeroSessao (int)
        EEEEE (unicode)
        CCCC (unicode)
        mensagem (unicode)
        cod (unicode)
        mensagemSEFAZ (unicode)
        arquivoCFeBase64 (unicode)
        timeStamp (datetime.datetime)
        chaveConsulta (unicode)
        valorTotalCFe (decimal.Decimal)
        CPFCNPJValue (unicode)
        assinaturaQRCODE (unicode)

    Em caso de falha, são esperados apenas os atributos:

    .. sourcecode:: text

        numeroSessao (int)
        EEEEE (unicode)
        CCCC (unicode)
        mensagem (unicode)
        cod (unicode)
        mensagemSEFAZ (unicode)

    Finalmente, como último recurso, a resposta poderá incluir apenas os
    atributos padrão, conforme descrito na constante
    :attr:`~satcfe.resposta.padrao.RespostaSAT.CAMPOS`.
    """

    def xml(self):
        """Retorna o XML do CF-e-SAT de cancelamento decodificado."""
        return base64.b64decode(getattr(self, 'arquivoCFeBase64', ''))


    def qrcode(self):
        """Resulta nos dados que compõem o QRCode."""
        return dados_qrcode(self.xml())


    @staticmethod
    def analisar(retorno):
        """Constrói uma :class:`RespostaCancelarUltimaVenda` a partir do
        retorno informado.

        :param unicode retorno: Retorno da função ``CancelarUltimaVenda``.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='EnviarDadosVenda',
                classe_resposta=RespostaCancelarUltimaVenda,
                campos=(
                        ('numeroSessao', int),
                        ('EEEEE', unicode),
                        ('CCCC', unicode),
                        ('mensagem', unicode),
                        ('cod', unicode),
                        ('mensagemSEFAZ', unicode),
                        ('arquivoCFeBase64', unicode),
                        ('timeStamp', as_datetime),
                        ('chaveConsulta', unicode),
                        ('valorTotalCFe', Decimal),
                        ('CPFCNPJValue', unicode),
                        ('assinaturaQRCODE', unicode),
                    ),
                campos_alternativos=[
                        # se a venda falhar apenas os primeiros seis campos
                        # especificados na ER deverão ser retornados...
                        (
                                ('numeroSessao', int),
                                ('EEEEE', unicode),
                                ('CCCC', unicode),
                                ('mensagem', unicode),
                                ('cod', unicode),
                                ('mensagemSEFAZ', unicode),
                        ),
                        # por via das dúvidas, considera o padrão de campos,
                        # caso não haja nenhuma coincidência...
                        RespostaSAT.CAMPOS,
                    ]
            )
        if resposta.EEEEE not in ('07000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta
