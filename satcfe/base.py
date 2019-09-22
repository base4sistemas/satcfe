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
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import collections
import ctypes
import random
import warnings

from ctypes import c_int
from ctypes import c_char_p

import six

from satcomum import constantes


class _Prototype(object):
    __slots__ = ('argtypes', 'restype')

    def __init__(self, argtypes, restype=c_char_p):
        self.argtypes = argtypes
        self.restype = restype


FUNCTION_PROTOTYPES = dict(
        AtivarSAT=_Prototype([c_int, c_int, c_char_p, c_char_p, c_int]),
        ComunicarCertificadoICPBRASIL=_Prototype([c_int, c_char_p, c_char_p]),
        EnviarDadosVenda=_Prototype([c_int, c_char_p, c_char_p]),
        CancelarUltimaVenda=_Prototype([c_int, c_char_p, c_char_p, c_char_p]),
        ConsultarSAT=_Prototype([c_int]),
        TesteFimAFim=_Prototype([c_int, c_char_p, c_char_p]),
        ConsultarStatusOperacional=_Prototype([c_int, c_char_p]),
        ConsultarNumeroSessao=_Prototype([c_int, c_char_p, c_int]),
        ConfigurarInterfaceDeRede=_Prototype([c_int, c_char_p, c_char_p]),
        AssociarAssinatura=_Prototype([c_int, c_char_p, c_char_p, c_char_p]),
        AtualizarSoftwareSAT=_Prototype([c_int, c_char_p]),
        ExtrairLogs=_Prototype([c_int, c_char_p]),
        BloquearSAT=_Prototype([c_int, c_char_p]),
        DesbloquearSAT=_Prototype([c_int, c_char_p]),
        TrocarCodigoDeAtivacao=_Prototype([
                c_int,
                c_char_p,
                c_int,
                c_char_p,
                c_char_p]),
        ConsultarUltimaSessaoFiscal=_Prototype([c_int, c_char_p]),
    )


class BibliotecaSAT(object):
    """Configura a localização da biblioteca que efetivamente acessará o
    equipamento SAT. A biblioteca deverá ser uma DLL (*dynamic linked library*,
    em sistemas Microsoft Windows) ou uma *shared library* em sistemas baseados
    no UNIX ou GNU/Linux.

    :param string caminho: Caminho completo para a biblioteca SAT.

    :param integer convencao: Opcional. Indica a convenção de chamada da
        biblioteca, devendo ser uma das constantes definidas em
        :attr:`~satcomum.constantes.CONVENCOES_CHAMADA`. Se não for informado,
        a convenção de chamada será decidida conforme a extensão do nome do
        arquivo, assumindo :attr:`~satcomum.constantes.WINDOWS_STDCALL` para as
        extensões ``.DLL`` ou ``.dll``. Quaisquer outras extensões, assume a
        convenção de chamada :attr:`~satcomum.constantes.STANDARD_C`.

    """

    def __init__(self, caminho, convencao=None):
        self._libsat = None
        self._caminho = caminho
        self._convencao = convencao
        self._carregar()

    def _carregar(self):
        """Carrega (ou recarrega) a biblioteca SAT. Se a convenção de chamada
        ainda não tiver sido definida, será determinada pela extensão do
        arquivo da biblioteca.

        :raises ValueError: Se a convenção de chamada não puder ser determinada
            ou se não for um valor válido.
        """
        if self._convencao is None:
            if self._caminho.endswith(('.DLL', '.dll')):
                self._convencao = constantes.WINDOWS_STDCALL
            else:
                self._convencao = constantes.STANDARD_C

        if self._convencao == constantes.STANDARD_C:
            loader = ctypes.CDLL

        elif self._convencao == constantes.WINDOWS_STDCALL:
            loader = ctypes.WinDLL

        else:
            raise ValueError((
                    'Convencao de chamada desconhecida: {!r}'
                ).format(self._convencao))

        self._libsat = loader(self._caminho)

    @property
    def ref(self):
        """Uma referência para a biblioteca SAT carregada."""
        return self._libsat

    @property
    def caminho(self):
        """Caminho completo para a biblioteca SAT."""
        return self._caminho

    @property
    def convencao(self):
        """Convenção de chamada para a biblioteca SAT.
        Deverá ser um dos valores disponíveis na contante
        :attr:`~satcomum.constantes.CONVENCOES_CHAMADA`.
        """
        return self._convencao


class NumeroSessaoMemoria(object):
    """Implementa um numerador de sessão simples, baseado em memória, não
    persistente, que irá gerar um número de sessão (seis dígitos) diferente
    entre os ``n`` últimos números de sessão gerados. Conforme a ER SAT, um
    número de sessão não poderá ser igual aos últimos ``100`` números.
    """

    def __init__(self, tamanho=100):
        super(NumeroSessaoMemoria, self).__init__()
        self._tamanho = tamanho
        self._memoria = collections.deque(maxlen=tamanho)

    def __contains__(self, item):
        return item in self._memoria

    def __call__(self, *args, **kwargs):
        while True:
            numero = random.randint(100000, 999999)
            if numero not in self._memoria:
                self._memoria.append(numero)
                break
        return numero


class FuncoesSAT(object):
    """Estabelece a interface básica para acesso às funções da biblioteca SAT.

    A intenção é que esta classe seja a base para classes mais especializadas
    capazes de trabalhar as respostas, resultando em objetos mais úteis, já que
    os métodos desta classe invocam as funções da biblioteca SAT e retornam o
    resultado *verbatim*.

    As funções implementadas estão descritas na ER SAT, item 6.1.

    +---------+-----------------------------------+-----------------------------------------+
    | Item ER | Função                            | Método                                  |
    +=========+===================================+=========================================+
    | 6.1.1   | ``AtivarSAT``                     | :meth:`ativar_sat`                      |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.2   | ``ComunicarCertificadoICPBRASIL`` | :meth:`comunicar_certificado_icpbrasil` |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.3   | ``EnviarDadosVenda``              | :meth:`enviar_dados_venda`              |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.4   | ``CancelarUltimaVenda``           | :meth:`cancelar_ultima_venda`           |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.5   | ``ConsultarSAT``                  | :meth:`consultar_sat`                   |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.6   | ``TesteFimAFim``                  | :meth:`teste_fim_a_fim`                 |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.7   | ``ConsultarStatusOperacional``    | :meth:`consultar_status_operacional`    |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.8   | ``ConsultarNumeroSessao``         | :meth:`consultar_numero_sessao`         |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.9   | ``ConfigurarInterfaceDeRede``     | :meth:`configurar_interface_de_rede`    |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.10  | ``AssociarAssinatura``            | :meth:`associar_assinatura`             |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.11  | ``AtualizarSoftwareSAT``          | :meth:`atualizar_software_sat`          |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.12  | ``ExtrairLogs``                   | :meth:`extrair_logs`                    |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.13  | ``BloquearSAT``                   | :meth:`bloquear_sat`                    |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.14  | ``DesbloquearSAT``                | :meth:`desbloquear_sat`                 |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.15  | ``TrocarCodigoDeAtivacao``        | :meth:`trocar_codigo_de_ativacao`       |
    +---------+-----------------------------------+-----------------------------------------+
    | 6.1.16  | ``ConsultarUltimaSessaoFiscal``   | :meth:`consultar_ultima_sessao_fiscal`  |
    +---------+-----------------------------------+-----------------------------------------+

    :param biblioteca: Uma instância de :class:`BibliotecaSAT`.

    :param string codigo_ativacao: Código de ativação. Senha definida pelo
        contribuinte no software de ativação, conforme item 2.1.1 da ER SAT.

    :param numerador_sessao: Opcional. Um ``callable`` capaz de gerar um
        número de sessão conforme descrito no item 6, alínea "a", "Funções do
        Equipamento SAT", da ER SAT. Se não for especificado, será utilizado
        um :class:`NumeroSessaoMemoria`.

    """  # noqa: E501

    def __init__(
            self,
            biblioteca,
            codigo_ativacao=None,
            numerador_sessao=None,
            encoding='utf-8',
            encoding_errors='strict'):
        """
        TODO: documentar os parâmetros aqui
        """
        self._biblioteca = biblioteca
        self._codigo_ativacao = codigo_ativacao
        self._numerador_sessao = numerador_sessao or NumeroSessaoMemoria()
        self._encoding = encoding
        self._encoding_errors = encoding_errors

    @property
    def biblioteca(self):
        return self._biblioteca

    @property
    def codigo_ativacao(self):
        return self._codigo_ativacao

    @property
    def encoding(self):
        return self._encoding

    @property
    def encoding_errors(self):
        return self._encoding_errors

    def _invocar(self, funcname, *args, **kwargs):
        if funcname not in FUNCTION_PROTOTYPES:
            raise ValueError((
                    'There is no function prototype named: {!r}'
                ).format(funcname))

        proto = FUNCTION_PROTOTYPES[funcname]
        fptr = getattr(self._biblioteca.ref, funcname)
        fptr.argtypes = proto.argtypes
        fptr.restype = proto.restype

        encoded_args = []

        for argument in args:
            if isinstance(argument, str):
                argument = argument.encode(
                        encoding=self.encoding,
                        errors=self.encoding_errors)
            encoded_args.append(argument)

        raw_response = fptr(*encoded_args, **kwargs)

        return raw_response.decode(
                encoding=self.encoding,
                errors=self.encoding_errors)

    def gerar_numero_sessao(self):
        """Gera o número de sessão para a próxima invocação de função SAT."""
        return self._numerador_sessao()

    def ativar_sat(self, tipo_certificado, cnpj, codigo_uf):
        """Função ``AtivarSAT`` conforme ER SAT, item 6.1.1.
        Ativação do equipamento SAT. Dependendo do tipo do certificado, o
        procedimento de ativação é complementado enviando-se o certificado
        emitido pela ICP-Brasil (:meth:`comunicar_certificado_icpbrasil`).

        :param int tipo_certificado: Deverá ser um dos valores
            :attr:`satcomum.constantes.CERTIFICADO_ACSAT_SEFAZ`,
            :attr:`satcomum.constantes.CERTIFICADO_ICPBRASIL` ou
            :attr:`satcomum.constantes.CERTIFICADO_ICPBRASIL_RENOVACAO`, mas
            nenhuma validação será realizada antes que a função de ativação
            seja efetivamente invocada.

        :param str cnpj: Número do CNPJ do estabelecimento contribuinte,
            contendo apenas os dígitos. Nenhuma validação do número do CNPJ
            será realizada antes que a função de ativação seja efetivamente
            invocada.

        :param int codigo_uf: Código da unidade federativa onde o equipamento
            SAT será ativado (eg. ``35`` para o Estado de São Paulo). Nenhuma
            validação do código da UF será realizada antes que a função de
            ativação seja efetivamente invocada.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        resposta = self._invocar(
                'AtivarSAT',
                self.gerar_numero_sessao(),
                tipo_certificado,
                self.codigo_ativacao,
                cnpj,
                codigo_uf)
        return resposta

    def comunicar_certificado_icpbrasil(self, certificado):
        """Função ``ComunicarCertificadoICPBRASIL`` conforme ER SAT, item 6.1.2.
        Envio do certificado criado pela ICP-Brasil.

        :param str certificado: Conteúdo do certificado digital criado pela
            autoridade certificadora ICP-Brasil.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        resposta = self._invocar(
                'ComunicarCertificadoICPBRASIL',
                self.gerar_numero_sessao(),
                self.codigo_ativacao,
                certificado)
        return resposta

    def enviar_dados_venda(self, dados_venda, *args, **kwargs):
        """Função ``EnviarDadosVenda`` conforme ER SAT, item 6.1.3. Envia o
        CF-e de venda para o equipamento SAT, que o enviará para autorização
        pela SEFAZ.

        :param dados_venda: Instância de :class:`~satcfe.entidades.CFeVenda` ou
            uma string contendo o XML do CF-e de venda.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        cfe_venda = resolver_documento(dados_venda, *args, **kwargs)
        resposta = self._invocar(
                'EnviarDadosVenda',
                self.gerar_numero_sessao(),
                self._codigo_ativacao,
                cfe_venda)
        return resposta

    def cancelar_ultima_venda(
            self,
            chave_cfe,
            dados_cancelamento,
            *args,
            **kwargs):
        """Função ``CancelarUltimaVenda`` conforme ER SAT, item 6.1.4. Envia o
        CF-e de cancelamento para o equipamento SAT, que o enviará para
        autorização e cancelamento do CF-e pela SEFAZ.

        :param chave_cfe: String contendo a chave do CF-e de venda que será
            cancelado (deve possuir o prefixo ``"CFe"`` seguido dos dígitos
            da chave do CF-e-SAT autorizado anteriormente).

        :param dados_cancelamento: Uma instância
            de :class:`~satcfe.entidades.CFeCancelamento` ou uma string
            contendo o XML do CF-e de cancelamento.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        cfe_canc = resolver_documento(dados_cancelamento, *args, **kwargs)
        resposta = self._invocar(
                'CancelarUltimaVenda',
                self.gerar_numero_sessao(),
                self._codigo_ativacao,
                chave_cfe,
                cfe_canc)
        return resposta

    def consultar_sat(self):
        """Função ``ConsultarSAT`` conforme ER SAT, item 6.1.5. Usada para
        testes de comunicação entre a AC e o equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: str
        """
        resposta = self._invocar('ConsultarSAT', self.gerar_numero_sessao())
        return resposta

    def teste_fim_a_fim(self, dados_venda, *args, **kwargs):
        """Função ``TesteFimAFim`` conforme ER SAT, item 6.1.6. Teste de
        comunicação entre a AC, o equipamento SAT e a SEFAZ.

        :param dados_venda: Instância de :class:`~satcfe.entidades.CFeVenda` ou
            uma string contendo o XML do CF-e de venda de teste.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        cfe_venda = resolver_documento(dados_venda, *args, **kwargs)
        resposta = self._invocar(
                'TesteFimAFim',
                self.gerar_numero_sessao(),
                self._codigo_ativacao,
                cfe_venda)
        return resposta

    def consultar_status_operacional(self):
        """Função ``ConsultarStatusOperacional`` conforme ER SAT, item 6.1.7.
        Consulta do status operacional do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        resposta = self._invocar(
                'ConsultarStatusOperacional',
                self.gerar_numero_sessao(),
                self._codigo_ativacao)
        return resposta

    def consultar_numero_sessao(self, numero_sessao):
        """Função ``ConsultarNumeroSessao`` conforme ER SAT, item 6.1.8.
        Consulta o equipamento SAT por um número de sessão específico.

        :param int numero_sessao: Número da sessão que se quer consultar.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        resposta = self._invocar(
                'ConsultarNumeroSessao',
                self.gerar_numero_sessao(),
                self._codigo_ativacao,
                numero_sessao)
        return resposta

    def configurar_interface_de_rede(self, configuracao, *args, **kwargs):
        """Função ``ConfigurarInterfaceDeRede`` conforme ER SAT, item 6.1.9.
        Configuração da interface de comunicação do equipamento SAT.

        :param configuracao: Um objeto :class:`~satcfe.rede.ConfiguracaoRede`
            ou uma string contendo o XML com as configurações de rede.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        conf_xml = resolver_documento(configuracao, *args, **kwargs)
        resposta = self._invocar(
                'ConfigurarInterfaceDeRede',
                self.gerar_numero_sessao(),
                self._codigo_ativacao,
                conf_xml)
        return resposta

    def associar_assinatura(self, sequencia_cnpj, assinatura_ac):
        """Função ``AssociarAssinatura`` conforme ER SAT, item 6.1.10.
        Associação da assinatura do aplicativo comercial.

        :param sequencia_cnpj: Sequência string de 28 dígitos composta do CNPJ
            do desenvolvedor da AC e do CNPJ do estabelecimento comercial
            contribuinte, conforme ER SAT, item 2.1.3.

        :param assinatura_ac: Sequência string contendo a assinatura digital do
            parâmetro ``sequencia_cnpj`` codificada em base64.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        resposta = self._invocar(
                'AssociarAssinatura',
                self.gerar_numero_sessao(),
                self._codigo_ativacao,
                sequencia_cnpj,
                assinatura_ac)
        return resposta

    def atualizar_software_sat(self):
        """Função ``AtualizarSoftwareSAT`` conforme ER SAT, item 6.1.11,
        Atualização do software do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        resposta = self._invocar(
                'AtualizarSoftwareSAT',
                self.gerar_numero_sessao(),
                self._codigo_ativacao)
        return resposta

    def extrair_logs(self):
        """Função ``ExtrairLogs`` conforme ER SAT, item 6.1.12. Extração dos
        registros de log do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        resposta = self._invocar(
                'ExtrairLogs',
                self.gerar_numero_sessao(),
                self._codigo_ativacao)
        return resposta

    def bloquear_sat(self):
        """Função ``BloquearSAT`` conforme ER SAT, item 6.1.13. Bloqueio
        operacional do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        resposta = self._invocar(
                'BloquearSAT',
                self.gerar_numero_sessao(),
                self._codigo_ativacao)
        return resposta

    def desbloquear_sat(self):
        """Função ``DesbloquearSAT`` conforme ER SAT, item 6.1.14. Desbloqueio
        operacional do equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        resposta = self._invocar(
                'DesbloquearSAT',
                self.gerar_numero_sessao(),
                self._codigo_ativacao)
        return resposta

    def trocar_codigo_de_ativacao(
            self, novo_codigo_ativacao,
            opcao=constantes.CODIGO_ATIVACAO_REGULAR,
            codigo_emergencia=None):
        """Função ``TrocarCodigoDeAtivacao`` conforme ER SAT, item 6.1.15.
        Troca do código de ativação do equipamento SAT. YouX.

        :param str novo_codigo_ativacao: O novo código de ativação escolhido
            pelo contribuinte.

        :param int opcao: Indica se deverá ser utilizado o código de ativação
            atualmente configurado, que é um código de ativação regular,
            definido pelo contribuinte, ou se deverá ser usado um código de
            emergência. Deverá ser o valor de uma das constantes
            :attr:`satcomum.constantes.CODIGO_ATIVACAO_REGULAR` (padrão) ou
            :attr:`satcomum.constantes.CODIGO_ATIVACAO_EMERGENCIA`.
            Nenhuma validação será realizada antes que a função seja
            efetivamente invocada. Entretanto, se opção de código de ativação
            indicada for ``CODIGO_ATIVACAO_EMERGENCIA``, então o argumento que
            informa o ``codigo_emergencia`` será checado e deverá avaliar como
            verdadeiro.

        :param str codigo_emergencia: O código de ativação de emergência, que
            é definido pelo fabricante do equipamento SAT. Este código deverá
            ser usado quando o usuário perder o código de ativação regular, e
            precisar definir um novo código de ativação. Note que, o argumento
            ``opcao`` deverá ser informado com o valor
            :attr:`satcomum.constantes.CODIGO_ATIVACAO_EMERGENCIA` para que
            este código de emergência seja considerado.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string

        :raises ValueError: Se o novo código de ativação avaliar como falso
            (possuir uma string nula por exemplo) ou se o código de emergencia
            avaliar como falso quando a opção for pelo código de ativação de
            emergência.

        .. warning::

            De acordo com a :term:`ER SAT`, a função ``TrocarCodigoDeAtivacao``
            requer que o novo código de ativação seja especificado duas vezes.

            Este método ignora isso e apenas informa o mesmo código de ativação
            duas vezes na chamada da função. O entendimento é de que a
            confirmação do código de ativação é responsabilidade de outras
            camadas da aplicação (eg. interface com o usuário) e, portanto,
            fora do escopo desta biblioteca.

        """
        if not novo_codigo_ativacao:
            raise ValueError((
                    'Novo codigo de ativacao invalido: {!r}'
                ).format(novo_codigo_ativacao))

        codigo_ativacao = self._codigo_ativacao

        if opcao not in (v for v, s in constantes.TIPOS_CODIGOS_ATIVACAO):
            raise ValueError((
                    'Opcao de tipo de codigo de ativacao inesperado: '
                    'opcao={!r}'
                ).format(opcao))

        if opcao == constantes.CODIGO_ATIVACAO_EMERGENCIA:
            if codigo_emergencia:
                codigo_ativacao = codigo_emergencia
            else:
                raise ValueError((
                        'Codigo de ativacao de emergencia invalido: '
                        '{!r} (opcao={!r})'
                    ).format(codigo_emergencia, opcao))

        resposta = self._invocar(
                'TrocarCodigoDeAtivacao',
                self.gerar_numero_sessao(),
                codigo_ativacao,
                opcao,
                novo_codigo_ativacao,
                novo_codigo_ativacao)

        # NOTA: Em tese o novo código de ativação deverá passar a ser utilizado
        # pela implementação cliente. Este método em si não tem condições de
        # avaliar o sucesso ou fracasso do resultado sem provocar uma exceção
        # prematura, já que apenas retorna os dados brutos.
        #
        # A implementação especializada deverá alternar o código de ativação
        # atual para o novo código de ativação em caso de sucesso ao analisar o
        # retorno da função, para que as chamadas às funções SAT subsequentes
        # tenham sucesso.
        return resposta

    def consultar_ultima_sessao_fiscal(self):
        """Função ``ConsultarUltimaSessaoFiscal`` conforme ER SAT, item 6.1.16.
        Retorna a resposta da última sessão fiscal, isto é, do último comando
        fiscal (``EnviarDadosVenda`` ou ``CancelarUltimaVenda``) executado pelo
        equipamento SAT.

        :return: Retorna *verbatim* a resposta da função SAT.
        :rtype: string
        """
        resposta = self._invocar(
                'ConsultarUltimaSessaoFiscal',
                self.gerar_numero_sessao(),
                self._codigo_ativacao)
        return resposta


def resolver_documento(dados, *args, **kwargs):
    if isinstance(dados, six.string_types):
        conteudo = dados
        if args or kwargs:
            warnings.warn(
                    (
                        'O documento foi informado como um valor str, que '
                        'sera enviado literalmente para o equipamento; '
                        'isso implica em ignorar os argumentos extras '
                        'informados (para efeito de construcao do conteudo '
                        'do documento): args={!r}; kwargs={!r}'
                    ).format(args, kwargs),
                    category=UserWarning,
                    stacklevel=3)
    else:
        if hasattr(dados, 'documento') \
                and callable(dados.documento):
            conteudo = dados.documento(*args, **kwargs)
        else:
            raise ValueError((
                    'O argumento deve ser informado como um valor str (com o '
                    'conteudo do documento pronto para ser enviado ao '
                    'equipamento SAT) ou um objeto que possua um metodo '
                    '\'documento()\' capaz de gerar o conteudo do documento; '
                    'informado: {!r}'
                ).format(dados))
    return conteudo
