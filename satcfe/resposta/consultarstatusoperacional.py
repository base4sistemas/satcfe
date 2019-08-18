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
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from builtins import str as text

from ..excecoes import ExcecaoRespostaSAT
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


def _stripped_str(s):
    return text(s).strip()


class RespostaConsultarStatusOperacional(RespostaSAT):
    """Lida com as respostas da função ``ConsultarStatusOperacional`` (veja o
    método :meth:`~satcfe.base.FuncoesSAT.consultar_status_operacional`).
    Os atributos esperados em caso de sucesso, são:

    +---------------------+----------------------------------+
    | Atributo            | Tipo Python                      |
    +=====================+==================================+
    | ``numeroSessao``    | ``int``                          |
    +---------------------+----------------------------------+
    | ``EEEEE``           | ``text``                         |
    +---------------------+----------------------------------+
    | ``mensagem``        | ``text``                         |
    +---------------------+----------------------------------+
    | ``cod``             | ``text``                         |
    +---------------------+----------------------------------+
    | ``mensagemSEFAZ``   | ``text``                         |
    +---------------------+----------------------------------+
    | ``NSERIE``          | ``text``                         |
    +---------------------+----------------------------------+
    | ``TIPO_LAN``        | ``text``                         |
    +---------------------+----------------------------------+
    | ``LAN_IP``          | ``text``                         |
    +---------------------+----------------------------------+
    | ``LAN_MAC``         | ``text``                         |
    +---------------------+----------------------------------+
    | ``LAN_MASK``        | ``text``                         |
    +---------------------+----------------------------------+
    | ``LAN_GW``          | ``text``                         |
    +---------------------+----------------------------------+
    | ``LAN_DNS_1``       | ``text``                         |
    +---------------------+----------------------------------+
    | ``LAN_DNS_2``       | ``text``                         |
    +---------------------+----------------------------------+
    | ``STATUS_LAN``      | ``text``                         |
    +---------------------+----------------------------------+
    | ``NIVEL_BATERIA``   | ``text``                         |
    +---------------------+----------------------------------+
    | ``MT_TOTAL``        | ``text``                         |
    +---------------------+----------------------------------+
    | ``MT_USADA``        | ``text``                         |
    +---------------------+----------------------------------+
    | ``DH_ATUAL``        | ``datetime.datetime``            |
    +---------------------+----------------------------------+
    | ``VER_SB``          | ``text``                         |
    +---------------------+----------------------------------+
    | ``VER_LAYOUT``      | ``text``                         |
    +---------------------+----------------------------------+
    | ``ULTIMO_CF_E_SAT`` | ``text``                         |
    +---------------------+----------------------------------+
    | ``LISTA_INICIAL``   | ``text``                         |
    +---------------------+----------------------------------+
    | ``LISTA_FINAL``     | ``text``                         |
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

    .. note::

        Aqui, ``text`` diz respeito à um objeto ``unicode`` (Python 2) ou
        ``str`` (Python 3). Veja ``builtins.str`` da biblioteca ``future``.

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

        :param str retorno: Retorno da função ``ConsultarStatusOperacional``.
        """
        resposta = analisar_retorno(
                retorno,
                funcao='ConsultarStatusOperacional',
                classe_resposta=RespostaConsultarStatusOperacional,
                campos=RespostaSAT.CAMPOS + (
                        ('NSERIE', _stripped_str),
                        ('TIPO_LAN', _stripped_str),
                        ('LAN_IP', normalizar_ip),
                        ('LAN_MAC', text),
                        ('LAN_MASK', normalizar_ip),
                        ('LAN_GW', normalizar_ip),
                        ('LAN_DNS_1', normalizar_ip),
                        ('LAN_DNS_2', normalizar_ip),
                        ('STATUS_LAN', _stripped_str),
                        ('NIVEL_BATERIA', _stripped_str),
                        ('MT_TOTAL', _stripped_str),
                        ('MT_USADA', _stripped_str),
                        ('DH_ATUAL', as_datetime),
                        ('VER_SB', _stripped_str),
                        ('VER_LAYOUT', _stripped_str),
                        ('ULTIMO_CF_E_SAT', _stripped_str),
                        ('LISTA_INICIAL', _stripped_str),
                        ('LISTA_FINAL', _stripped_str),
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
