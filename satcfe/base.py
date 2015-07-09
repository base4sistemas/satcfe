# -*- coding: utf-8 -*-
#
# satcfe/base.py
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

import ctypes
import os
import random

from ctypes import c_int
from ctypes import c_char_p

from satcomum import constantes

from .config import conf


class _Prototype(object):
    def __init__(self, argtypes, restype=c_char_p):
        self.argtypes = argtypes
        self.restype = restype


FUNCTION_PROTOTYPES = dict(
        AtivarSAT=_Prototype([c_int, c_int, c_char_p, c_char_p, c_int]),
        ComunicarCertificadoICPBRASIL=_Prototype([c_int, c_char_p, c_char_p]),
        EnviarDadosVenda=_Prototype([c_int, c_char_p, c_char_p]),
        CancelarUltimaVenda=_Prototype([c_int, c_char_p, c_char_p, c_char_p]),
        ConsultarSAT=_Prototype([c_int,]),
        TesteFimAFim=_Prototype([c_int, c_char_p, c_char_p]),
        ConsultarStatusOperacional=_Prototype([c_int, c_char_p]),
        ConsultarNumeroSessao=_Prototype([c_int, c_char_p, c_int]),
        ConfigurarInterfaceDeRede=_Prototype([c_int, c_char_p, c_char_p]),
        AssociarAssinatura=_Prototype([c_int, c_char_p, c_char_p, c_char_p]),
        AtualizarSoftwareSAT=_Prototype([c_int, c_char_p]),
        ExtrairLogs=_Prototype([c_int, c_char_p]),
        BloquearSAT=_Prototype([c_int, c_char_p]),
        DesbloquearSAT=_Prototype([c_int, c_char_p]),
        TrocarCodigoDeAtivacao=_Prototype([c_int, c_char_p, c_int, c_char_p, c_char_p])
    )


class DLLSAT(object):
    """
    Configura a localização da DLL do equipamento SAT e mantém uma
    referência carregada para a ela, conforme a convenção de chamada.
    """

    def __init__(self, caminho=None, convencao=constantes.STANDARD_C):
        self._libsat = None
        self.caminho = caminho
        self.convencao = convencao
        self.carregar()


    @property
    def ref(self):
        """Uma referência para a biblioteca SAT carregada."""
        return self._libsat


    @property
    def caminho(self):
        """Caminho completo, incluindo o nome do arquivo, para a biblioteca
        SAT (DLL ou *shared object*).

        :raises ValueError: Se a biblioteca não existir no caminho indicado.
        """
        return self._caminho


    @caminho.setter
    def caminho(self, valor):
        if not os.path.exists(valor):
            raise ValueError('Biblioteca SAT inexistente em: {}'.format(valor))
        self._caminho = valor


    @property
    def convencao(self):
        """Convenção de chamada para a biblioteca SAT. Deverá ser um dos valores
        disponíveis na contante :attr:`~satcomum.constantes.CONVENCOES_CHAMADA`.

        :raises ValueError: Se a convenção de chamada não for reconhecida.
        """
        return self._convencao


    @convencao.setter
    def convencao(self, valor):
        if valor not in [v for v,s in constantes.CONVENCOES_CHAMADA]:
            raise ValueError('Convencao de chamada invalida: {}'.format(valor))
        self._convencao = valor


    def carregar(self):
        """Carrega (ou recarrega) a biblioteca SAT.

        :raises ValueError: Se a convenção de chamada não for reconhecida.
        """
        if self._libsat is not None:
            del self._libsat
            self._libsat = None

        if constantes.STANDARD_C == self.convencao:
            loader = ctypes.CDLL
        elif constantes.WINDOWS_STDCALL == self.convencao:
            loader = ctypes.WinDLL
        else:
            raise ValueError('Convencao de chamada desconhecida: %s' %
                    self.convencao)

        self._libsat = loader(self.caminho)


class NumeroSessaoMemoria(object):
    """Implementa um numerador de sessão simples, baseado em memória, não
    persistente, que irá gerar um número de sessão (seis dígitos) diferente
    entre os 100 últimos números de sessão gerados, conforme ER SAT.
    """

    def __init__(self, tamanho=100):
        super(NumeroSessaoMemoria, self).__init__()
        self._memoria = []
        self._tamanho = tamanho


    def __call__(self, *args, **kwargs):
        while True:
            numero = random.randint(100000, 999999)
            if numero not in self._memoria:
                self._memoria.append(numero)
                if len(self._memoria) > self._tamanho:
                    self._memoria.pop(0) # remove o mais antigo
                break
        return numero


class FuncoesSAT(object):
    """Estabelece a interface básica para acesso às funções da biblioteca SAT.

    A intenção é que esta classe seja a base para classes mais especializadas
    capazes de trabalhar as respostas, resultando em objetos mais úteis, já que
    os métodos desta classe invocam as funções da biblioteca SAT e retornam o
    resultado *verbatim*.
    """

    def __init__(self, dll=None, numerador_sessao=None):
        self._dll = dll
        self._numerador_sessao = numerador_sessao or NumeroSessaoMemoria()


    def gerar_numero_sessao(self):
        """Gera o número de sessão para a próxima invocação de função SAT."""
        return self._numerador_sessao()


    def __getattr__(self, name):
        if name.startswith('invocar__'):
            metodo_sat = name.replace('invocar__', '')
            proto = FUNCTION_PROTOTYPES[metodo_sat]
            fptr = getattr(self._dll.ref, metodo_sat)
            fptr.argtypes = proto.argtypes
            fptr.restype = proto.restype
            return fptr
        raise AttributeError('{!r} object has no attribute {!r}'.format(
                self.__class__.__name__, name))


    def comunicar_certificado_icpbrasil(self, certificado):
        """Função ``ComunicarCertificadoICPBRASIL`` conforme ER SAT, item 6.1.2.
        Envio do certificado criado pela ICP-Brasil.

        :param str certificado: Conteúdo do certificado digital criado pela
            autoridade certificadora ICP-Brasil.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        return self.invocar__ComunicarCertificadoICPBRASIL(
                self.gerar_numero_sessao(), conf.codigo_ativacao, certificado)


    def enviar_dados_venda(self, dados_venda):
        """Função ``EnviarDadosVenda`` conforme ER SAT, item 6.1.3. Envia o
        CF-e de venda para o equipamento SAT, que o enviará para autorização
        pela SEFAZ.

        :param dados_venda: Uma instância de :class:`~satcfe.entidades.CFeVenda`
            ou uma string contendo o XML do CF-e de venda.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        cfe_venda = dados_venda \
                if isinstance(dados_venda, basestring) \
                else dados_venda.documento()

        return self.invocar__EnviarDadosVenda(
                self.gerar_numero_sessao(), conf.codigo_ativacao, cfe_venda)


    def cancelar_ultima_venda(self, chave_cfe, dados_cancelamento):
        """Função ``CancelarUltimaVenda`` conforme ER SAT, item 6.1.4. Envia o
        CF-e de cancelamento para o equipamento SAT, que o enviará para
        autorização e cancelamento do CF-e pela SEFAZ.

        :param chave_cfe: String contendo a chave do CF-e a ser cancelado,
            prefixada com o literal ``CFe``.

        :param dados_cancelamento: Uma instância
            de :class:`~satcfe.entidades.CFeCancelamento` ou uma string
            contendo o XML do CF-e de cancelamento.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        cfe_canc = dados_cancelamento \
                if isinstance(dados_cancelamento, basestring) \
                else dados_cancelamento.documento()

        return self.invocar__CancelarUltimaVenda(
                self.gerar_numero_sessao(), conf.codigo_ativacao,
                chave_cfe, cfe_canc)


    def consultar_sat(self):
        """Função ``ConsultarSAT`` conforme ER SAT, item 6.1.5. Usada para
        testes de comunicação entre a AC e o equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        return self.invocar__ConsultarSAT(self.gerar_numero_sessao())


    def teste_fim_a_fim(self, dados_venda):
        """Função ``TesteFimAFim`` conforme ER SAT, item 6.1.6. Teste de
        comunicação entre a AC, o equipamento SAT e a SEFAZ.

        :param dados_venda: Uma instância de :class:`~satcfe.entidades.CFeVenda`
            ou uma string contendo o XML do CF-e de venda de teste.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        cfe_venda = dados_venda \
                if isinstance(dados_venda, basestring) \
                else dados_venda.documento()

        return self.invocar__TesteFimAFim(
                self.gerar_numero_sessao(), conf.codigo_ativacao, cfe_venda)


    def consultar_status_operacional(self):
        """Função ``ConsultarStatusOperacional`` conforme ER SAT, item 6.1.7.
        Consulta do status operacional do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        return self.invocar__ConsultarStatusOperacional(
                self.gerar_numero_sessao(), conf.codigo_ativacao)


    def configurar_interface_de_rede(self, configuracao):
        """Função ``ConfigurarInterfaceDeRede`` conforme ER SAT, item 6.1.9.
        Configurção da interface de comunicação do equipamento SAT.

        :param configuracao: Instância de :class:`~satcfe.rede.ConfiguracaoRede`
            ou uma string contendo o XML com as configurações de rede.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        conf_xml = configuracao \
                if isinstance(configuracao, basestring) \
                else configuracao.documento()

        return self.invocar__ConfigurarInterfaceDeRede(
                self.gerar_numero_sessao(), conf.codigo_ativacao, conf_xml)


    def associar_assinatura(self, sequencia_cnpj, assinatura_ac):
        """Função ``AssociarAssinatura`` conforme ER SAT, item 6.1.10.
        Associação da assinatura do aplicativo comercial.

        :param sequencia_cnpj: Sequência string de 28 dígitos composta do CNPJ
            do desenvolvedor da AC e do CNPJ do estabelecimento comercial
            contribuinte, conforme ER SAT, item 2.3.1.

        :param assinatura_ac: Sequência string contendo a assinatura digital do
            parâmetro ``sequencia_cnpj`` codificada em base64.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        return self.invocar__AssociarAssinatura(
                self.gerar_numero_sessao(), conf.codigo_ativacao,
                sequencia_cnpj, assinatura_ac)


    def atualizar_software_sat(self):
        """Função ``AtualizarSoftwareSAT`` conforme ER SAT, item 6.1.11.
        Atualização do software do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        return self.invocar__AtualizarSoftwareSAT(
                self.gerar_numero_sessao(), conf.codigo_ativacao)


    def extrair_logs(self):
        """Função ``ExtrairLogs`` conforme ER SAT, item 6.1.12. Extração dos
        registros de log do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        return self.invocar__ExtrairLogs(
                self.gerar_numero_sessao(), conf.codigo_ativacao)


    def bloquear_sat(self):
        """Função ``BloquearSAT`` conforme ER SAT, item 6.1.13. Bloqueio
        operacional do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        return self.invocar__BloquearSAT(
                self.gerar_numero_sessao(), conf.codigo_ativacao)


    def desbloquear_sat(self):
        """Função ``DesbloquearSAT`` conforme ER SAT, item 6.1.14. Desbloqueio
        operacional do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        return self.invocar__DesbloquearSAT(
                self.gerar_numero_sessao(), conf.codigo_ativacao)
