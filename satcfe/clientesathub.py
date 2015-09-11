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

from satcomum import constantes

import satcfe

from .base import FuncoesSAT
from .config import conf

from .resposta import RespostaAtivarSAT
from .resposta import RespostaCancelarUltimaVenda
from .resposta import RespostaConsultarNumeroSessao
from .resposta import RespostaConsultarStatusOperacional
from .resposta import RespostaEnviarDadosVenda
from .resposta import RespostaExtrairLogs
from .resposta import RespostaSAT
from .resposta import RespostaTesteFimAFim


class ClienteSATHub(FuncoesSAT):
    """Fornece acesso concorrente a um equipamento SAT remoto.

    O acesso é feito consumindo-se a API RESTful `SATHub`_ que irá efetivamente
    acessar um equipamento SAT e responder através de uma conexão HTTP.

    As respostas às funções SAT serão trabalhadas resultando em objetos Python
    regulares cujos atributos representam as peças de informação conforme
    descrito, função por função, na ER SAT.

    .. _`SATHub`: https://github.com/base4sistemas/sathub

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


    def ativar_sat(self, tipo_certificado, cnpj, codigo_uf):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.ativar_sat`.

        :return: Uma resposta SAT especializada em ``AtivarSAT``.
        :rtype: satcfe.resposta.ativarsat.RespostaAtivarSAT
        """
        resp = self._http_post('ativarsat',
                tipo_certificado=tipo_certificado,
                cnpj=cnpj,
                codigo_uf=codigo_uf)
        conteudo = resp.json()
        return RespostaAtivarSAT.analisar(conteudo.get('retorno'))


    def comunicar_certificado_icpbrasil(self, certificado):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.comunicar_certificado_icpbrasil`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        resp = self._http_post('comunicarcertificadoicpbrasil',
                certificado=certificado)
        conteudo = resp.json()
        return RespostaSAT.comunicar_certificado_icpbrasil(
                conteudo.get('retorno'))


    def enviar_dados_venda(self, dados_venda):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.enviar_dados_venda`.

        :return: Uma resposta SAT especializada em ``EnviarDadosVenda``.
        :rtype: satcfe.resposta.enviardadosvenda.RespostaEnviarDadosVenda
        """
        resp = self._http_post('enviardadosvenda',
                dados_venda=dados_venda.documento())
        conteudo = resp.json()
        return RespostaEnviarDadosVenda.analisar(conteudo.get('retorno'))


    def cancelar_ultima_venda(self, chave_cfe, dados_cancelamento):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.cancelar_ultima_venda`.

        :return: Uma resposta SAT especializada em ``CancelarUltimaVenda``.
        :rtype: satcfe.resposta.cancelarultimavenda.RespostaCancelarUltimaVenda
        """
        resp = self._http_post('cancelarultimavenda',
                chave_cfe=chave_cfe,
                dados_cancelamento=dados_cancelamento.documento())
        conteudo = resp.json()
        return RespostaCancelarUltimaVenda.analisar(conteudo.get('retorno'))


    def consultar_sat(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.consultar_sat`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        resp = self._http_post('consultarsat')
        conteudo = resp.json()
        return RespostaSAT.consultar_sat(conteudo.get('retorno'))


    def teste_fim_a_fim(self, dados_venda):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.teste_fim_a_fim`.

        :return: Uma resposta SAT especializada em ``TesteFimAFim``.
        :rtype: satcfe.resposta.testefimafim.RespostaTesteFimAFim
        """
        resp = self._http_post('testefimafim',
                dados_venda=dados_venda.documento())
        conteudo = resp.json()
        return RespostaTesteFimAFim.analisar(conteudo.get('retorno'))


    def consultar_status_operacional(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.consultar_status_operacional`.

        :return: Uma resposta SAT especializada em ``ConsultarStatusOperacional``.
        :rtype: satcfe.resposta.consultarstatusoperacional.RespostaConsultarStatusOperacional
        """
        resp = self._http_post('consultarstatusoperacional')
        conteudo = resp.json()
        return RespostaConsultarStatusOperacional.analisar(
                conteudo.get('retorno'))


    def consultar_numero_sessao(self, numero_sessao):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.consultar_numero_sessao`.

        :return: Uma resposta SAT que irá depender da sessão consultada.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        resp = self._http_post('consultarnumerosessao',
                numero_sessao=numero_sessao)
        conteudo = resp.json()
        return RespostaConsultarNumeroSessao.analisar(conteudo.get('retorno'))


    def configurar_interface_de_rede(self, configuracao):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.configurar_interface_de_rede`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        resp = self._http_post('configurarinterfacederede',
                configuracao=configuracao.documento())
        conteudo = resp.json()
        return RespostaSAT.configurar_interface_de_rede(conteudo.get('retorno'))


    def associar_assinatura(self, sequencia_cnpj, assinatura_ac):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.associar_assinatura`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        resp = self._http_post('associarassinatura',
                sequencia_cnpj=sequencia_cnpj, assinatura_ac=assinatura_ac)
        # (!) resposta baseada na redação com efeitos até 31-12-2016
        conteudo = resp.json()
        return RespostaSAT.associar_assinatura(conteudo.get('retorno'))


    def atualizar_software_sat(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.atualizar_software_sat`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        resp = self._http_post('atualizarsoftwaresat')
        conteudo = resp.json()
        return RespostaSAT.atualizar_software_sat(conteudo.get('retorno'))


    def extrair_logs(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.extrair_logs`.

        :return: Uma resposta SAT especializada em ``ExtrairLogs``.
        :rtype: satcfe.resposta.extrairlogs.RespostaExtrairLogs
        """
        resp = self._http_post('extrairlogs')
        conteudo = resp.json()
        return RespostaExtrairLogs.analisar(conteudo.get('retorno'))


    def bloquear_sat(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.bloquear_sat`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        resp = self._http_post('bloquearsat')
        conteudo = resp.json()
        return RespostaSAT.bloquear_sat(conteudo.get('retorno'))


    def desbloquear_sat(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.desbloquear_sat`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        resp = self._http_post('desbloquearsat')
        conteudo = resp.json()
        return RespostaSAT.desbloquear_sat(conteudo.get('retorno'))


    def trocar_codigo_de_ativacao(self, novo_codigo_ativacao,
            opcao=constantes.CODIGO_ATIVACAO_REGULAR,
            codigo_emergencia=None):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.trocar_codigo_de_ativacao`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        resp = self._http_post('trocarcodigodeativacao',
                novo_codigo_ativacao=novo_codigo_ativacao,
                opcao=opcao,
                codigo_emergencia=codigo_emergencia)
        conteudo = resp.json()
        return RespostaSAT.trocar_codigo_de_ativacao(conteudo.get('retorno'))
