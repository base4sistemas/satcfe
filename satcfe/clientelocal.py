# -*- coding: utf-8 -*-
#
# satcfe/clientelocal.py
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

from satcomum import constantes

from .base import FuncoesSAT

from .resposta import RespostaAssociarAssinatura
from .resposta import RespostaAtivarSAT
from .resposta import RespostaCancelarUltimaVenda
from .resposta import RespostaConsultarNumeroSessao
from .resposta import RespostaConsultarStatusOperacional
from .resposta import RespostaConsultarUltimaSessaoFiscal
from .resposta import RespostaEnviarDadosVenda
from .resposta import RespostaExtrairLogs
from .resposta import RespostaSAT
from .resposta import RespostaTesteFimAFim


class ClienteSATLocal(FuncoesSAT):
    """Fornece acesso ao equipamento SAT conectado na máquina local.

    As respostas às funções SAT serão trabalhadas resultando em objetos Python
    regulares cujos atributos representam as peças de informação conforme
    descrito, função por função, na ER SAT.
    """

    def __init__(self, *args, **kwargs):
        super(ClienteSATLocal, self).__init__(*args, **kwargs)

    def ativar_sat(self, tipo_certificado, cnpj, codigo_uf):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.ativar_sat`.

        :return: Uma resposta SAT especilizada em ``AtivarSAT``.
        :rtype: satcfe.resposta.ativarsat.RespostaAtivarSAT
        """
        retorno = super(ClienteSATLocal, self).ativar_sat(
                tipo_certificado,
                cnpj,
                codigo_uf)
        return RespostaAtivarSAT.analisar(retorno)

    def comunicar_certificado_icpbrasil(self, certificado):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.comunicar_certificado_icpbrasil`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).comunicar_certificado_icpbrasil(
                certificado)
        return RespostaSAT.comunicar_certificado_icpbrasil(retorno)

    def enviar_dados_venda(self, dados_venda, *args, **kwargs):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.enviar_dados_venda`.

        :return: Uma resposta SAT especializada em ``EnviarDadosVenda``.
        :rtype: satcfe.resposta.enviardadosvenda.RespostaEnviarDadosVenda
        """
        retorno = super(ClienteSATLocal, self).enviar_dados_venda(
                dados_venda,
                *args,
                **kwargs)
        return RespostaEnviarDadosVenda.analisar(retorno)

    def cancelar_ultima_venda(
            self,
            chave_cfe,
            dados_cancelamento,
            *args,
            **kwargs):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.cancelar_ultima_venda`.

        :return: Uma resposta SAT especializada em ``CancelarUltimaVenda``.
        :rtype: satcfe.resposta.cancelarultimavenda.RespostaCancelarUltimaVenda
        """
        retorno = super(ClienteSATLocal, self).cancelar_ultima_venda(
                chave_cfe,
                dados_cancelamento,
                *args,
                **kwargs)
        return RespostaCancelarUltimaVenda.analisar(retorno)

    def consultar_sat(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.consultar_sat`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).consultar_sat()
        return RespostaSAT.consultar_sat(retorno)

    def teste_fim_a_fim(self, dados_venda, *args, **kwargs):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.teste_fim_a_fim`.

        :return: Uma resposta SAT especializada em ``TesteFimAFim``.
        :rtype: satcfe.resposta.testefimafim.RespostaTesteFimAFim
        """
        retorno = super(ClienteSATLocal, self).teste_fim_a_fim(
                dados_venda,
                *args,
                **kwargs)
        return RespostaTesteFimAFim.analisar(retorno)

    def consultar_status_operacional(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.consultar_status_operacional`.

        :return: Uma resposta SAT especializada em
            ``ConsultarStatusOperacional``.
        :rtype: satcfe.resposta.consultarstatusoperacional.RespostaConsultarStatusOperacional
        """  # noqa: E501
        retorno = super(ClienteSATLocal, self).consultar_status_operacional()
        return RespostaConsultarStatusOperacional.analisar(retorno)

    def consultar_numero_sessao(self, numero_sessao):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.consultar_numero_sessao`.

        :return: Uma resposta SAT que irá depender da sessão consultada.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).consultar_numero_sessao(
                numero_sessao)
        return RespostaConsultarNumeroSessao.analisar(retorno)

    def configurar_interface_de_rede(self, configuracao, *args, **kwargs):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.configurar_interface_de_rede`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).configurar_interface_de_rede(
                configuracao,
                *args,
                **kwargs)
        return RespostaSAT.configurar_interface_de_rede(retorno)

    def associar_assinatura(self, sequencia_cnpj, assinatura_ac):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.associar_assinatura`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).associar_assinatura(
                sequencia_cnpj,
                assinatura_ac)
        return RespostaAssociarAssinatura.analisar(retorno)

    def atualizar_software_sat(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.atualizar_software_sat`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).atualizar_software_sat()
        return RespostaSAT.atualizar_software_sat(retorno)

    def extrair_logs(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.extrair_logs`.

        :return: Uma resposta SAT especializada em ``ExtrairLogs``.
        :rtype: satcfe.resposta.extrairlogs.RespostaExtrairLogs
        """
        retorno = super(ClienteSATLocal, self).extrair_logs()
        return RespostaExtrairLogs.analisar(retorno)

    def bloquear_sat(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.bloquear_sat`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).bloquear_sat()
        return RespostaSAT.bloquear_sat(retorno)

    def desbloquear_sat(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.desbloquear_sat`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).desbloquear_sat()
        return RespostaSAT.desbloquear_sat(retorno)

    def trocar_codigo_de_ativacao(
            self, novo_codigo_ativacao,
            opcao=constantes.CODIGO_ATIVACAO_REGULAR,
            codigo_emergencia=None):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.trocar_codigo_de_ativacao`.

        :return: Uma resposta SAT padrão.
        :rtype: satcfe.resposta.padrao.RespostaSAT
        """
        retorno = super(ClienteSATLocal, self).trocar_codigo_de_ativacao(
                novo_codigo_ativacao,
                opcao=opcao,
                codigo_emergencia=codigo_emergencia)

        resposta = RespostaSAT.trocar_codigo_de_ativacao(retorno)

        # NOTA: Se não foi lançada nenhuma exceção, assume que a troca do
        # código de ativação foi bem sucedida. Alterna o código de ativação
        # atual para o novo código de ativação para que as chamadas
        # subsequentes tenham sucesso.
        self._codigo_ativacao = novo_codigo_ativacao

        return resposta

    def consultar_ultima_sessao_fiscal(self):
        """Sobrepõe :meth:`~satcfe.base.FuncoesSAT.consultar_ultima_sessao_fiscal`.

        :return: Uma resposta SAT que irá depender do último comando "fiscal"
            executado pelo equipmamento SAT, que poderá ser uma venda ou um
            cancelamento de venda.

        :rtype: satcfe.resposta.consultarultimasessaofiscal.RespostaConsultarUltimaSessaoFiscal |
            satcfe.resposta.enviardadosvenda.RespostaEnviarDadosVenda |
            satcfe.resposta.cancelarultimavenda.RespostaCancelarUltimaVenda

        """  # noqa: E501
        retorno = super(ClienteSATLocal, self).consultar_ultima_sessao_fiscal()
        return RespostaConsultarUltimaSessaoFiscal.analisar(retorno)
