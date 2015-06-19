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

from .base import _FuncoesSAT
from .config import conf

from .resposta import RespostaCancelarUltimaVenda
from .resposta import RespostaConsultarStatusOperacional
from .resposta import RespostaEnviarDadosVenda
from .resposta import RespostaExtrairLogs
from .resposta import RespostaSAT
from .resposta import RespostaTesteFimAFim


class ClienteSATLocal(_FuncoesSAT):
    """
    Acesso ao equipamento SAT conectado na máquina local, para acesso às
    funções da DLL do SAT-CF-e.
    """

    def __init__(self, *args, **kwargs):
        super(ClienteSATLocal, self).__init__(*args, **kwargs)


    def comunicar_certificado_icpbrasil(self, certificado):
        retorno = super(ClienteSATLocal, self).\
                comunicar_certificado_icpbrasil(certificado)
        return RespostaSAT.comunicar_certificado_icpbrasil(retorno)


    def enviar_dados_venda(self, dados_venda):
        retorno = super(ClienteSATLocal, self).enviar_dados_venda(dados_venda)
        return RespostaEnviarDadosVenda.analisar(retorno)


    def cancelar_ultima_venda(self, chave_cfe, dados_cancelamento):
        retorno = super(ClienteSATLocal, self).\
                cancelar_ultima_venda(chave_cfe, dados_cancelamento)
        return RespostaCancelarUltimaVenda.analisar(retorno)


    def consultar_sat(self):
        retorno = super(ClienteSATLocal, self).consultar_sat()
        return RespostaSAT.consultar_sat(retorno)


    def teste_fim_a_fim(self, dados_venda):
        retorno = super(ClienteSATLocal, self).teste_fim_a_fim(dados_venda)
        return RespostaTesteFimAFim.analisar(retorno)


    def consultar_status_operacional(self):
        retorno = super(ClienteSATLocal, self).consultar_status_operacional()
        return RespostaConsultarStatusOperacional.analisar(retorno)


    def configurar_interface_de_rede(self, configuracao):
        retorno = super(ClienteSATLocal, self).\
                configurar_interface_de_rede(configuracao)
        return RespostaSAT.configurar_interface_de_rede(retorno)


    def associar_assinatura(self, sequencia_cnpj, assinatura_ac):
        retorno = super(ClienteSATLocal, self).\
                associar_assinatura(sequencia_cnpj, assinatura_ac)
        # (!) resposta baseada na redação com efeitos até 31-12-2016
        return RespostaSAT.associar_assinatura(retorno)


    def atualizar_software_sat(self):
        retorno = super(ClienteSATLocal, self).atualizar_software_sat()
        return RespostaSAT.atualizar_software_sat(retorno)


    def extrair_logs(self):
        retorno = super(ClienteSATLocal, self).extrair_logs()
        return RespostaExtrairLogs.analisar(retorno)


    def bloquear_sat(self):
        retorno = super(ClienteSATLocal, self).bloquear_sat()
        return RespostaSAT.bloquear_sat(retorno)


    def desbloquear_sat(self):
        retorno = super(ClienteSATLocal, self).desbloquear_sat()
        return RespostaSAT.desbloquear_sat(retorno)
