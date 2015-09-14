# -*- coding: utf-8 -*-
#
# satcfe/resposta/padrao.py
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

from satcomum.util import forcar_unicode

from ..excecoes import ExcecaoRespostaSAT
from ..excecoes import ErroRespostaSATInvalida
from ..util import as_ascii


class RespostaSAT(object):
    """Base para representação de respostas das funções da biblioteca SAT.
    A maior parte das funções SAT resultam em respostas que contém um conjunto
    padrão de atributos (veja o atributo :attr:`CAMPOS`), descritos na ER SAT:

    .. sourcecode:: text

        numeroSessao (int)
        EEEEE (unicode)
        mensagem (unicode)
        cod (unicode)
        mensagemSEFAZ (unicode)

    Além dos atributos padrão, a resposta deverá conter uma referência para o
    nome da função SAT a que a resposta se refere e ao conteúdo original da
    resposta, através dos atributos:

    .. sourcecode:: python

        resposta.atributos.funcao
        resposta.atributos.verbatim

    Esta classe fornece uma série de métodos construtores (*factory methods*)
    para respostas que são comuns. Para as respostas que não são comuns, existem
    especializações desta classe.
    """

    class _Atributos(object):
        pass


    CAMPOS = (
            ('numeroSessao', int),
            ('EEEEE', unicode),
            ('mensagem', unicode),
            ('cod', unicode),
            ('mensagemSEFAZ', unicode),
        )
    """Campos padrão esperados em uma resposta e a sua função de conversão para
    o tipo Python, a partir da resposta original (unicode).
    """


    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.atributos = RespostaSAT._Atributos()
        self.atributos.funcao = None
        self.atributos.verbatim = None


    @staticmethod
    def comunicar_certificado_icpbrasil(retorno):
        """Constrói uma :class:`RespostaSAT` para o retorno (unicode) da função
        :meth:`~satcfe.base.FuncoesSAT.comunicar_certificado_icpbrasil`.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='ComunicarCertificadoICPBRASIL')
        if resposta.EEEEE not in ('05000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta


    @staticmethod
    def consultar_sat(retorno):
        """Constrói uma :class:`RespostaSAT` para o retorno (unicode) da função
        :meth:`~satcfe.base.FuncoesSAT.consultar_sat`.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='ConsultarSAT')
        if resposta.EEEEE not in ('08000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta


    @staticmethod
    def configurar_interface_de_rede(retorno):
        """Constrói uma :class:`RespostaSAT` para o retorno (unicode) da função
        :meth:`~satcfe.base.FuncoesSAT.configurar_interface_de_rede`.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='ConfigurarInterfaceDeRede')
        if resposta.EEEEE not in ('12000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta


    @staticmethod
    def associar_assinatura(retorno):
        """Constrói uma :class:`RespostaSAT` para o retorno (unicode) da função
        :meth:`~satcfe.base.FuncoesSAT.associar_assinatura`.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='AssociarAssinatura')
        if resposta.EEEEE not in ('13000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta


    @staticmethod
    def atualizar_software_sat(retorno):
        """Constrói uma :class:`RespostaSAT` para o retorno (unicode) da função
        :meth:`~satcfe.base.FuncoesSAT.atualizar_software_sat`.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='AtualizarSoftwareSAT')
        if resposta.EEEEE not in ('14000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta


    @staticmethod
    def bloquear_sat(retorno):
        """Constrói uma :class:`RespostaSAT` para o retorno (unicode) da função
        :meth:`~satcfe.base.FuncoesSAT.bloquear_sat`.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='BloquearSAT')
        if resposta.EEEEE not in ('16000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta


    @staticmethod
    def desbloquear_sat(retorno):
        """Constrói uma :class:`RespostaSAT` para o retorno (unicode) da função
        :meth:`~satcfe.base.FuncoesSAT.desbloquear_sat`.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='DesbloquearSAT')
        if resposta.EEEEE not in ('17000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta


    @staticmethod
    def trocar_codigo_de_ativacao(retorno):
        """Constrói uma :class:`RespostaSAT` para o retorno (unicode) da função
        :meth:`~satcfe.base.FuncoesSAT.trocar_codigo_de_ativacao`.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='TrocarCodigoDeAtivacao')
        if resposta.EEEEE not in ('18000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta


def analisar_retorno(retorno,
        classe_resposta=RespostaSAT, campos=RespostaSAT.CAMPOS,
        campos_alternativos=[], funcao=None, manter_verbatim=True):
    """Analisa o retorno (supostamente um retorno de uma função do SAT) conforme
    o padrão e campos esperados. O retorno deverá possuir dados separados entre
    si através de pipes e o número de campos deverá coincidir com os campos
    especificados.

    O campos devem ser especificados como uma tupla onde cada elemento da tupla
    deverá ser uma tupla contendo dois elementos: o nome do campo e uma função
    de conversão a partir de uma string unicode. Por exemplo:

    .. sourcecode:: python

        >>> retorno = '123456|08000|SAT em operacao||'
        >>> resposta = analisar_retorno(retorno, funcao='ConsultarSAT')
        >>> resposta.numeroSessao
        123456
        >>> resposta.EEEEE
        u'08000'
        >>> resposta.mensagem
        u'SAT em operacao'
        >>> resposta.cod
        u''
        >>> resposta.mensagemSEFAZ
        u''
        >>> resposta.atributos.funcao
        'ConsultarSAT'
        >>> resposta.atributos.verbatim
        '123456|08000|SAT em operacao||'

    :param unicode retorno: O conteúdo **unicode** da resposta retornada pela
        função da DLL SAT.

    :param type classe_resposta: O tipo :class:`RespostaSAT` ou especialização
        que irá representar o retorno, após sua decomposição em campos.

    :param tuple campos: Especificação dos campos (nomes) e seus conversores a
        a partir do tipo ``unicode``.

    :param list campos_alternativos: Especifica conjuntos de campos alternativos
        que serão considerados caso o número de campos encontrados na resposta
        não coincida com o número de campos especificados em ``campos``.
        Para que a relação alternativa de campos funcione, é importante que
        cada relação de campos alternativos tenha um número diferente de campos.

    :param str funcao: Nome da função da DLL SAT que gerou o retorno, que
        estará disponível nos atributos adicionais à resposta.

    :param bool manter_verbatim: Se uma cópia verbatim da resposta deverá ser
        mantida nos atributos adicionais à resposta.

    :raises ErroRespostaSATInvalida: Se o retorno não estiver em conformidade
        com o padrão esperado ou se não possuir os campos especificados.

    :return: Uma instância de :class:`RespostaSAT` ou especialização.
    :rtype: satcfe.resposta.padrao.RespostaSAT

    """

    if '|' not in retorno:
        raise ErroRespostaSATInvalida('Resposta nao possui pipes separando os '
                'campos: "%s"' % as_ascii(retorno))

    partes = retorno.split('|')

    if len(partes) != len(campos):
        # procura por uma relação alternativa de campos do retorno
        for relacao_alternativa in campos_alternativos:
            if len(partes) == len(relacao_alternativa):
                relacao_campos = relacao_alternativa
                break
        else:
            raise ErroRespostaSATInvalida('Resposta nao possui o numero '
                    'esperado de campos. Esperados %d campos, mas '
                    'contem %d: "%s"' % (
                            len(campos), len(partes), as_ascii(retorno),))
    else:
        relacao_campos = campos

    resultado = {}

    def _enumerate(sequence):
        for index, value in enumerate(sequence):
            yield index, value[0], value[1]

    for indice, campo, conversor in _enumerate(relacao_campos):
        resultado[campo] = conversor(partes[indice])

    resposta = classe_resposta(**resultado)
    resposta.atributos.funcao = funcao
    resposta.atributos.verbatim = retorno if manter_verbatim else None

    return resposta
