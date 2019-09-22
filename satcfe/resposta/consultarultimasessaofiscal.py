# -*- coding: utf-8 -*-
#
# satcfe/resposta/consultarultimasessaofiscal.py
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

from collections import namedtuple

from ..excecoes import ErroRespostaSATInvalida
from ..excecoes import ExcecaoRespostaSAT
from .cancelarultimavenda import RespostaCancelarUltimaVenda
from .enviardadosvenda import RespostaEnviarDadosVenda
from .padrao import RespostaSAT
from .padrao import analisar_retorno


_RESPOSTAS_POSSIVEIS = (
        (6000, RespostaEnviarDadosVenda.analisar),
        (7000, RespostaCancelarUltimaVenda.analisar),
    )


_RespostaParcial = namedtuple('_RespostaParcial', 'numeroSessao EEEEE')


class RespostaConsultarUltimaSessaoFiscal(RespostaSAT):
    """Lida com as respostas da função ``ConsultarUltimaSessaoFiscal`` (veja o
    método :meth:`~satcfe.base.FuncoesSAT.consultar_numero_sessao`). Como as
    respostas dependem do última comando "fiscal" executado pelo equipamento
    SAT, o método de construção :meth:`analisar` deverá resultar na resposta
    apropriada para cada retorno.
    """

    @staticmethod
    def analisar(retorno):
        """Constrói uma :class:`RespostaSAT` ou especialização dependendo da
        função SAT encontrada na última sessão fiscal.

        :param str retorno: Retorno da função ``ConsultarUltimaSessaoFiscal``.
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
            if eeeee not in range(19001, 19999):
                # não está na faixa de códigos específicos da própria
                # função ConsultarUltimaSessaoFiscal; testa por uma faixa de
                # códigos entre as respostas possíveis...
                for faixa, construtor in _RESPOSTAS_POSSIVEIS:
                    if eeeee in range(faixa, faixa+1000):
                        return construtor(retorno)

        return RespostaConsultarUltimaSessaoFiscal._pos_analise(retorno)

    @staticmethod
    def _pos_analise(retorno):
        resposta = analisar_retorno(
                retorno,
                funcao='ConsultarUltimaSessaoFiscal',
                classe_resposta=RespostaConsultarUltimaSessaoFiscal)
        if resposta.EEEEE not in ('19000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta
