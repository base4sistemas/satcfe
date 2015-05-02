# -*- coding: utf-8 -*-
#
# satcfe/resposta.py
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

from unidecode import unidecode

from satcomum import util


CAMPOS_PADRAO = (
        ('numeroSessao', int),
        ('EEEEE', unicode),
        ('mensagem', unicode),
        ('cod', unicode),
        ('mensagemSEFAZ', unicode),)


class ErroRespostaSATInvalida(Exception):
    """
    Lançada quando a resposta dada por uma função da DLL SAT não contém
    informação que faça sentido dentro do contexto. Este erro é diferente de
    uma :exc:`ExcecaoRespostaSAT` que é lançada quando a resposta faz sentido
    mas é interpretada como uma exceção a um comando que falhou.
    """
    pass


class ExcecaoRespostaSAT(Exception):
    """
    Lançada quando uma resposta à uma função da DLL SAT (comando SAT) é
    interpretada como tendo falhado. São casos em que a resposta é perfeitamente
    válida mas é interpretada como falha.

    Por exemplo, quando a função ``ConsultarSAT`` é invocada e a resposta
    indica um código ``EEEEE`` diferente de ``08000``, então uma exceção como
    esta será lançada.
    """

    def __init__(self, resposta):
        _x = lambda p: unidecode(p) if isinstance(p, unicode) else p
        super(ExcecaoRespostaSAT, self).__init__(
                '%s, numeroSessao=%s, EEEEE="%s", mensagem="%s", '
                'cod="%s", mensagemSEFAZ="%s"' % (
                        resposta.atributos.funcao or 'F(?)',
                        _x(getattr(resposta, 'numeroSessao', '?')),
                        _x(getattr(resposta, 'EEEEE', '?')),
                        _x(getattr(resposta, 'mensagem', '?')),
                        _x(getattr(resposta, 'cod', '?')),
                        _x(getattr(resposta, 'mensagemSEFAZ', '?')),))
        self._resposta = resposta


    @property
    def resposta(self):
        return self._resposta


class Atributos(object):
    def __init__(self, **kwargs):
        super(Atributos, self).__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)


class RespostaSAT(object):
    def __init__(self, **kwargs):
        super(RespostaSAT, self).__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)


    @staticmethod
    def enviar_dados_venda(retorno):
        resposta = analisar_retorno(util.forcar_unicode(retorno),
                funcao='EnviarDadosVenda',
                campos=(
                        ('numeroSessao', int),
                        ('EEEEE', unicode),
                        ('CCCC', unicode),
                        ('mensagem', unicode),
                        ('cod', unicode),
                        ('mensagemSEFAZ', unicode),
                        ('arquivoCFeSAT', unicode),
                        ('timeStamp', utils.from_ansi_datetime),
                        ('chaveConsulta', unicode),
                        ('valorTotalCFe', Decimal),
                        ('CPFCNPJValue', unicode),
                        ('assinaturaQRCODE', unicode),
                    ),
                campos_alternativos=[
                        # se a venda falhar apenas os primeiros seis campos
                        # especificados na ER deverão ser retornados...
                        (
                                ('numeroSessao', int),
                                ('EEEEE', unicode),
                                ('CCCC', unicode),
                                ('mensagem', unicode),
                                ('cod', unicode),
                                ('mensagemSEFAZ', unicode),
                        ),
                        # por via das dúvidas, considera o padrão de campos,
                        # caso não haja nenhuma coincidência...
                        CAMPOS_PADRAO,
                    ]
            )
        if resposta.EEEEE not in ('06000',):
            raise ExcecaoRespostaSAT(resposta)
        return RespostaVenda(resposta)


    @staticmethod
    def consultar_sat(retorno):
        resposta = analisar_retorno(util.forcar_unicode(retorno),
                funcao='ConsultarSAT')
        if resposta.EEEEE not in ('08000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta


    @staticmethod
    def extrair_logs(retorno):
        resposta = analisar_retorno(util.forcar_unicode(retorno),
                funcao='ExtrairLogs',
                campos=CAMPOS_PADRAO + (
                        ('arquivoLog', unicode)
                    )
            )
        if resposta.EEEEE not in ('15000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta


def analisar_retorno(retorno,
        campos=CAMPOS_PADRAO,
        campos_alternativos=[],
        funcao=None,
        manter_verbatim=True):
    """
    Analisa o retorno (supostamente um retorno de uma função do SAT) conforme o
    padrão e campos esperados. O retorno deverá possuir dados separados entre
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

    :return: Um objeto :class:`RespostaSAT`.

    """

    if '|' not in retorno:
        raise ErroRespostaSATInvalida('Resposta nao possui pipes separando os '
                'campos: "%s"' % retorno)

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
                            len(campos), len(partes), retorno,))
    else:
        relacao_campos = campos

    resultado = {}

    def _enumerate(sequence):
        for index, value in enumerate(sequence):
            yield index, value[0], value[1]

    for indice, campo, conversor in _enumerate(relacao_campos):
        resultado[campo] = conversor(partes[indice])

    resposta = RespostaSAT(**resultado)
    resposta.atributos = Atributos(**dict(
            funcao=funcao,
            verbatim=retorno if manter_verbatim else None))

    return resposta


