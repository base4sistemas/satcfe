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
from .resposta import RespostaExtrairLogs
from .resposta import RespostaSAT


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


    # def _http_get(self, metodo, params):
    #     return requests.get(self._url(metodo), params=params,
    #             headers=self._request_headers())


    def _http_post(self, metodo, **payload):
        if 'numero_caixa' not in payload:
            payload.update({'numero_caixa': conf.numero_caixa})
        headers = self._request_headers()
        resp = requests.post(self._url(metodo), data=payload, headers=headers)
        resp.raise_for_status()
        return resp


    def enviar_dados_venda(self, dados_venda):
        raise NotImplementedError()


    def consultar_sat(self):
        resp = self._http_post('consultarsat')
        conteudo = resp.json()
        return RespostaSAT.consultar_sat(conteudo.get('retorno'))


    def extrair_logs(self):
        resp = self._http_post('extrairlogs')
        conteudo = resp.json()
        return RespostaExtrairLogs.analisar(conteudo.get('retorno'))

