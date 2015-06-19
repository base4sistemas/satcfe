# -*- coding: utf-8 -*-
#
# satcfe/clientesathub.py
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

import json

import requests

import satcfe

from .base import _FuncoesSAT
from .config import conf

from .resposta import RespostaCancelarUltimaVenda
from .resposta import RespostaConsultarStatusOperacional
from .resposta import RespostaEnviarDadosVenda
from .resposta import RespostaExtrairLogs
from .resposta import RespostaSAT
from .resposta import RespostaTesteFimAFim


class ClienteSATHub(_FuncoesSAT):
    """
    Acesso concorrente ao equipamento SAT conectado remotamente, para acesso às
    funções da DLL do SAT-CF-e. O acesso é feito via API RESTful para um
    serviço que irá efetivamente acessar o equipamento SAT e retornar a
    resposta através de uma conexão HTTP.
    """

    def _request_headers(self):
        headers = {
                'user-agent': 'satcfe/{}/ER-{}'.format(
                        satcfe.__version__, satcfe.VERSAO_ER),
            }
        return headers


    def _url(self, metodo):
        return 'http://{}:{}/{}/{}'.format(
                conf.sathub.host,
                conf.sathub.port,
                conf.sathub.baseurl.strip('/'), metodo)


    def _http_post(self, metodo, **payload):
        if 'numero_caixa' not in payload:
            payload.update({'numero_caixa': conf.numero_caixa})
        headers = self._request_headers()
        resp = requests.post(self._url(metodo), data=payload, headers=headers)
        resp.raise_for_status()
        return resp


    def comunicar_certificado_icpbrasil(self, certificado):
        resp = self._http_post('comunicarcertificadoicpbrasil',
                certificado=certificado)
        conteudo = resp.json()
        return RespostaSAT.comunicar_certificado_icpbrasil(
                conteudo.get('retorno'))


    def enviar_dados_venda(self, dados_venda):
        resp = self._http_post('enviardadosvenda',
                dados_venda=dados_venda.documento())
        conteudo = resp.json()
        return RespostaEnviarDadosVenda.analisar(conteudo.get('retorno'))


    def cancelar_ultima_venda(self, chave_cfe, dados_cancelamento):
        resp = self._http_post('cancelarultimavenda',
                chave_cfe=chave_cfe,
                dados_cancelamento=dados_cancelamento.documento())
        conteudo = resp.json()
        return RespostaCancelarUltimaVenda.analisar(conteudo.get('retorno'))


    def consultar_sat(self):
        resp = self._http_post('consultarsat')
        conteudo = resp.json()
        return RespostaSAT.consultar_sat(conteudo.get('retorno'))


    def teste_fim_a_fim(self, dados_venda):
        resp = self._http_post('testefimafim',
                dados_venda=dados_venda.documento())
        conteudo = resp.json()
        return RespostaTesteFimAFim.analisar(conteudo.get('retorno'))


    def consultar_status_operacional(self):
        resp = self._http_post('consultarstatusoperacional')
        conteudo = resp.json()
        return RespostaConsultarStatusOperacional.analisar(
                conteudo.get('retorno'))


    def configurar_interface_de_rede(self, configuracao):
        resp = self._http_post('configurarinterfacederede',
                configuracao=configuracao.documento())
        conteudo = resp.json()
        return RespostaSAT.configurar_interface_de_rede(conteudo.get('retorno'))


    def associar_assinatura(self, sequencia_cnpj, assinatura_ac):
        resp = self._http_post('associarassinatura',
                sequencia_cnpj=sequencia_cnpj, assinatura_ac=assinatura_ac)
        # (!) resposta baseada na redação com efeitos até 31-12-2016
        conteudo = resp.json()
        return RespostaSAT.associar_assinatura(conteudo.get('retorno'))


    def atualizar_software_sat(self):
        resp = self._http_post('atualizarsoftwaresat')
        conteudo = resp.json()
        return RespostaSAT.atualizar_software_sat(conteudo.get('retorno'))


    def extrair_logs(self):
        resp = self._http_post('extrairlogs')
        conteudo = resp.json()
        return RespostaExtrairLogs.analisar(conteudo.get('retorno'))


    def bloquear_sat(self):
        resp = self._http_post('bloquearsat')
        conteudo = resp.json()
        return RespostaSAT.bloquear_sat(conteudo.get('retorno'))


    def desbloquear_sat(self):
        resp = self._http_post('desbloquearsat')
        conteudo = resp.json()
        return RespostaSAT.desbloquear_sat(conteudo.get('retorno'))

