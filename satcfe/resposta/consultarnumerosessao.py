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

from collections import namedtuple

from satcomum.util import forcar_unicode

from ..excecoes import ExcecaoRespostaSAT
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
        (13000, RespostaSAT.associar_assinatura),
        (14000, RespostaSAT.atualizar_software_sat),
        (15000, RespostaExtrairLogs.analisar),
        (16000, RespostaSAT.bloquear_sat),
        (17000, RespostaSAT.desbloquear_sat),
        (18000, RespostaSAT.trocar_codigo_de_ativacao),
    )


_RespostaParcial = namedtuple('_RespostaParcial', 'numeroSessao EEEEE')


class RespostaConsultarNumeroSessao(RespostaSAT):

    @staticmethod
    def analisar(retorno):
        if '|' not in retorno:
            raise ErroRespostaSATInvalida('Resposta nao possui pipes '
                    'separando os campos: {!r}'.format(retorno))

        resposta = _RespostaParcial(*(retorno.split('|')[:2]))

        for faixa, construtor in _RESPOSTAS_POSSIVEIS:
            if int(resposta.EEEEE) in xrange(faixa, faixa+1000):
                return construtor(retorno)

        return RespostaConsultarNumeroSessao._pos_analise(retorno)


    @staticmethod
    def _pos_analise(retorno):
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='ConsultarNumeroSessao',
                classe_resposta=RespostaConsultarNumeroSessao,
                campos=(
                        ('numeroSessao', int),
                        ('EEEEE', unicode),
                        ('mensagem', unicode),
                        ('cod', unicode),
                        ('mensagemSEFAZ', unicode),
                    ),
            )
        if resposta.EEEEE not in ('11000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta
