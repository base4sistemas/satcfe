# -*- coding: utf-8 -*-
#
# satcfe/resposta/consultarnumerosessao.py
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

from collections import namedtuple

from ..excecoes import ErroRespostaSATInvalida
from ..excecoes import ExcecaoRespostaSAT
from .associarassinatura import RespostaAssociarAssinatura
from .ativarsat import RespostaAtivarSAT
from .cancelarultimavenda import RespostaCancelarUltimaVenda
from .consultarstatusoperacional import RespostaConsultarStatusOperacional
from .enviardadosvenda import RespostaEnviarDadosVenda
from .extrairlogs import RespostaExtrairLogs
from .padrao import RespostaSAT
from .padrao import analisar_retorno
from .testefimafim import RespostaTesteFimAFim


_RESPOSTAS_POSSIVEIS = (
        # (!) todas as funções SAT, exceto ConsultarNumeroSessao
        (4000, RespostaAtivarSAT.analisar),
        (5000, RespostaSAT.comunicar_certificado_icpbrasil),
        (6000, RespostaEnviarDadosVenda.analisar),
        (7000, RespostaCancelarUltimaVenda.analisar),
        (8000, RespostaSAT.consultar_sat),
        (9000, RespostaTesteFimAFim.analisar),
        (10000, RespostaConsultarStatusOperacional.analisar),
        (12000, RespostaSAT.configurar_interface_de_rede),
        (13000, RespostaAssociarAssinatura),
        (14000, RespostaSAT.atualizar_software_sat),
        (15000, RespostaExtrairLogs.analisar),
        (16000, RespostaSAT.bloquear_sat),
        (17000, RespostaSAT.desbloquear_sat),
        (18000, RespostaSAT.trocar_codigo_de_ativacao),
    )


_RespostaParcial = namedtuple('_RespostaParcial', 'numeroSessao EEEEE')


class RespostaConsultarNumeroSessao(RespostaSAT):
    """Lida com as respostas da função ``ConsultarNumeroSessao`` (veja o método
    :meth:`~satcfe.base.FuncoesSAT.consultar_numero_sessao`). Como as respostas
    dependem do número da sessão consultado, o método de construção
    :meth:`analisar` deverá resultar na resposta apropriada para cada retorno.
    """

    @staticmethod
    def analisar(retorno):
        """Constrói uma :class:`RespostaSAT` ou especialização dependendo da
        função SAT encontrada na sessão consultada.

        :param str retorno: Retorno da função ``ConsultarNumeroSessao``.
        """
        if '|' not in retorno:
            raise ErroRespostaSATInvalida(
                    'Resposta não possui pipes '
                    'separando os campos: {!r}'.format(retorno))

        resposta = _RespostaParcial(*(retorno.split('|')[:2]))

        try:
            eeeee = int(resposta.EEEEE)
        except ValueError:
            # não é possível converter 'EEEEE' para inteiro;
            # deixa seguir com a pós-análise do retorno
            pass
        else:
            if eeeee not in range(11001, 11999):
                # não está na faixa de códigos específicos da própria
                # função ConsultarNumeroSessao; testa por uma faixa de códigos
                # entre as respostas possíveis...
                for faixa, construtor in _RESPOSTAS_POSSIVEIS:
                    if eeeee in range(faixa, faixa+1000):
                        return construtor(retorno)

        return RespostaConsultarNumeroSessao._pos_analise(retorno)

    @staticmethod
    def _pos_analise(retorno):
        resposta = analisar_retorno(
                retorno,
                funcao='ConsultarNumeroSessao',
                classe_resposta=RespostaConsultarNumeroSessao)
        if resposta.EEEEE not in ('11000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta
