# -*- coding: utf-8 -*-
#
# satcfe/resposta/consultarstatusoperacional.py
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
import errno
import os
import tempfile

from satcomum.util import forcar_unicode

from ..excecoes import ExcecaoRespostaSAT
from ..util import as_clean_unicode
from ..util import as_date
from ..util import as_datetime
from ..util import as_datetime_or_none
from ..util import normalizar_ip
from .padrao import RespostaSAT
from .padrao import analisar_retorno


DESBLOQUEADO = 0
BLOQUEADO_SEFAZ = 1
BLOQUEADO_CONTRIBUINTE = 2
BLOQUEADO_AUTO = 3
BLOQUEADO_PARA_DESATIVACAO = 4

ESTADOS_OPERACAO = (
        (DESBLOQUEADO, u'Desbloqueado'),
        (BLOQUEADO_SEFAZ, u'Bloqueado pelo SEFAZ'),
        (BLOQUEADO_CONTRIBUINTE, u'Bloqueado pelo contribuinte'),
        (BLOQUEADO_AUTO, u'Bloqueado autonomamente'),
        (BLOQUEADO_PARA_DESATIVACAO, u'Bloqueado para desativação'),
    )
"""Códigos do estados de operação e suas descrições amigáveis."""


class RespostaConsultarStatusOperacional(RespostaSAT):
    """Lida com as respostas da função ``ConsultarStatusOperacional`` (veja o
    método :meth:`~satcfe.base.FuncoesSAT.consultar_status_operacional`).
    Os atributos esperados em caso de sucesso, são:

    +---------------------+----------------------------------+
    | Atributo            | Tipo Python                      |
    +=====================+==================================+
    | ``numeroSessao``    | ``int``                          |
    +---------------------+----------------------------------+
    | ``EEEEE``           | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``mensagem``        | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``cod``             | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``mensagemSEFAZ``   | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``NSERIE``          | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``TIPO_LAN``        | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``LAN_IP``          | ``str``                          |
    +---------------------+----------------------------------+
    | ``LAN_MAC``         | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``LAN_MASK``        | ``str``                          |
    +---------------------+----------------------------------+
    | ``LAN_GW``          | ``str``                          |
    +---------------------+----------------------------------+
    | ``LAN_DNS_1``       | ``str``                          |
    +---------------------+----------------------------------+
    | ``LAN_DNS_2``       | ``str``                          |
    +---------------------+----------------------------------+
    | ``STATUS_LAN``      | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``NIVEL_BATERIA``   | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``MT_TOTAL``        | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``MT_USADA``        | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``DH_ATUAL``        | ``datetime.datetime``            |
    +---------------------+----------------------------------+
    | ``VER_SB``          | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``VER_LAYOUT``      | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``ULTIMO_CF_E_SAT`` | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``LISTA_INICIAL``   | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``LISTA_FINAL``     | ``unicode``                      |
    +---------------------+----------------------------------+
    | ``DH_CFE``          | ``datetime.datetime``|``None``   |
    +---------------------+----------------------------------+
    | ``DH_ULTIMA``       | ``datetime.datetime``            |
    +---------------------+----------------------------------+
    | ``CERT_EMISSAO``    | ``datetime.date``                |
    +---------------------+----------------------------------+
    | ``CERT_VENCIMENTO`` | ``datetime.date``                |
    +---------------------+----------------------------------+
    | ``ESTADO_OPERACAO`` | ``int``                          |
    +---------------------+----------------------------------+

    Em caso de falha, são esperados apenas os atributos padrão, conforme
    descrito na constante :attr:`~satcfe.resposta.padrao.RespostaSAT.CAMPOS`.
    """

    @property
    def status(self):
        """Nome amigável do campo ``ESTADO_OPERACAO``, conforme a "Tabela de
        Informações do Status do SAT".
        """
        for valor, rotulo in ESTADOS_OPERACAO:
            if self.ESTADO_OPERACAO == valor:
                return rotulo
        return u'(desconhecido: {})'.format(self.ESTADO_OPERACAO)


    @staticmethod
    def analisar(retorno):
        """Constrói uma :class:`RespostaConsultarStatusOperacional` a partir do
        retorno informado.

        :param unicode retorno: Retorno da função ``ConsultarStatusOperacional``.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='ConsultarStatusOperacional',
                classe_resposta=RespostaConsultarStatusOperacional,
                campos=RespostaSAT.CAMPOS + (
                        ('NSERIE', as_clean_unicode),
                        ('TIPO_LAN', as_clean_unicode),
                        ('LAN_IP', normalizar_ip),
                        ('LAN_MAC', unicode),
                        ('LAN_MASK', normalizar_ip),
                        ('LAN_GW', normalizar_ip),
                        ('LAN_DNS_1', normalizar_ip),
                        ('LAN_DNS_2', normalizar_ip),
                        ('STATUS_LAN', as_clean_unicode),
                        ('NIVEL_BATERIA', as_clean_unicode),
                        ('MT_TOTAL', as_clean_unicode),
                        ('MT_USADA', as_clean_unicode),
                        ('DH_ATUAL', as_datetime),
                        ('VER_SB', as_clean_unicode),
                        ('VER_LAYOUT', as_clean_unicode),
                        ('ULTIMO_CF_E_SAT', as_clean_unicode),
                        ('LISTA_INICIAL', as_clean_unicode),
                        ('LISTA_FINAL', as_clean_unicode),
                        ('DH_CFE', as_datetime_or_none),
                        ('DH_ULTIMA', as_datetime),
                        ('CERT_EMISSAO', as_date),
                        ('CERT_VENCIMENTO', as_date),
                        ('ESTADO_OPERACAO', int),
                    ),
                campos_alternativos=[
                        # se falhar resultarão apenas os 5 campos padrão
                        RespostaSAT.CAMPOS,
                    ]
            )
        if resposta.EEEEE not in ('10000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta
