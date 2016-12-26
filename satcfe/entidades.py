# -*- coding: utf-8 -*-
#
# satcfe/entidade.py
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

"""Representação das entidades que compõem o layout do CF-e.

A documentação oficial para os atributos que as classes de entidades
referenciam, estão na Especificação Técnica de Requisitos (ER) do SAT, item
4.2.2, Layout do Arquivo de Venda (CF-e-SAT) que pode ser obtido no `site
oficial <http://www.fazenda.sp.gov.br/sat/>`_.

Nem todas as classes que representam os grupos de informações do CF-e possuem o
mesmo nome usado no item 4.2.2 do layout do arquivo de venda ou no item 4.2.3 do
layout do arquivo de cancelamento. **Entretanto, todos os elementos e atributos,
possuem exatamente o mesmo nome usado na ER SAT**.

A tabela abaixo, relaciona as classes de entidades com os grupos que elas
representam:

+------------------+------+--------------------------------+
| Grupo            | ID   | Classe de Entidade             |
+==================+======+================================+
| ``emit``         | C01  | :class:`Emitente`              |
+------------------+------+--------------------------------+
| ``dest``         | E01  | :class:`Destinatario`          |
+------------------+------+--------------------------------+
| ``entrega``      | G01  | :class:`LocalEntrega`          |
+------------------+------+--------------------------------+
| ``det``          | H01  | :class:`Detalhamento`          |
+------------------+------+--------------------------------+
| ``prod``         | I01  | :class:`ProdutoServico`        |
+------------------+------+--------------------------------+
| ``obsFiscoDet``  | I17  | :class:`ObsFiscoDet`           |
+------------------+------+--------------------------------+
| ``ICMS00``       | N02  | :class:`ICMS00`                |
+------------------+------+--------------------------------+
| ``ICMS40``       | N03  | :class:`ICMS40`                |
+------------------+------+--------------------------------+
| ``ICMSSN102``    | N04  | :class:`ICMSSN102`             |
+------------------+------+--------------------------------+
| ``ICMSSN900``    | N05  | :class:`ICMSSN900`             |
+------------------+------+--------------------------------+
| ``PISAliq``      | Q02  | :class:`PISAliq`               |
+------------------+------+--------------------------------+
| ``PISQtde``      | Q03  | :class:`PISQtde`               |
+------------------+------+--------------------------------+
| ``PISNT``        | Q04  | :class:`PISNT`                 |
+------------------+------+--------------------------------+
| ``PISSN``        | Q05  | :class:`PISSN`                 |
+------------------+------+--------------------------------+
| ``PISOutr``      | Q06  | :class:`PISOutr`               |
+------------------+------+--------------------------------+
| ``PISST``        | R01  | :class:`PISST`                 |
+------------------+------+--------------------------------+
| ``COFINSAliq``   | S02  | :class:`COFINSAliq`            |
+------------------+------+--------------------------------+
| ``COFINSQtde``   | S03  | :class:`COFINSQtde`            |
+------------------+------+--------------------------------+
| ``COFINSNT``     | S04  | :class:`COFINSNT`              |
+------------------+------+--------------------------------+
| ``COFINSSN``     | S05  | :class:`COFINSSN`              |
+------------------+------+--------------------------------+
| ``COFINSOutr``   | S06  | :class:`COFINSOutr`            |
+------------------+------+--------------------------------+
| ``COFINSST``     | T01  | :class:`COFINSST`              |
+------------------+------+--------------------------------+
| ``ISSQN``        | U01  | :class:`ISSQN`                 |
+------------------+------+--------------------------------+
| ``imposto``      | M01  | :class:`Imposto`               |
+------------------+------+--------------------------------+
| ``DescAcrEntr``  | W19  | :class:`DescAcrEntr`           |
+------------------+------+--------------------------------+
| ``MP``           | WA02 | :class:`MeioPagamento`         |
+------------------+------+--------------------------------+
| ``infAdic``      | Z01  | :class:`InformacoesAdicionais` |
+------------------+------+--------------------------------+

Hierarquia dos elementos XML do layout do CF-e, ER SAT, item 4.2.2.

Destinatário e Local de entrega:

    .. sourcecode:: text

        infCFe (A01, 1)
        |
        +--- dest (E01, 1)
        |
        +--- entrega (G01, 0..1)
        :


Detalhamento dos produtos/serviços e impostos:

    .. sourcecode:: text

        infCFe (A01, 1)
        |
        +--- det (H01, 1..500)
        |    |
        |    +--- prod (I01, 1)
        |    |    |
        |    |    +--- obsFiscoDet (I17, 0..10)
        |    |
        |    +--- imposto (M01, 1)
        |         |
        |         +--- ICMS (N01, 0..1)
        :         |    |
        :         |    +--- ICMS00 (N02, 0..1)
        .         |    |         > ICMS 00, 20, 90
        .         |    |
                  |    +--- ICMS40 (N03, 0..1)
                  |    |         > ICMS 40, 41, 60
                  |    |
                  |    +--- ICMSSN102 (N04, 0..1)
                  |    |         > cRegTrib = 1, Simples Nacional
                  |    |         > CSOSN 102, 300, 400, 500
                  |    |
                  |    +--- ICMSSN900 (N05, 0..1)
                  |              > cRegTrib = 1, Simples Nacional
                  |              > CSOSN 900
                  |
                  +--- PIS (Q01, 1..1)
                  |    |
                  |    +--- PISAliq (Q02, 0..1)
                  |    |         > CST 01, 02, 05
                  |    |
                  |    +--- PISQtde (Q03, 0..1)
                  |    |         > CST 03
                  |    |
                  |    +--- PISNT (Q04, 0..1)
                  |    |         > Não Tributado
                  |    |         > CST 04, 06, 07, 08, 09
                  |    |
                  |    +--- PISSN (Q05, 0..1)
                  |    |         > Simples Nacional
                  |    |         > CST 49
                  |    |
                  |    +--- PISOutr (Q06, 0..1)
                  |              > Outras Operações
                  |              > CST 99
                  |
                  +--- PISST (R01, 0..1)
                  |          > Substituição Tributária
                  |
                  +--- COFINS (S01, 1..1)
                  |    |
                  |    +--- COFINSAliq (S02, 0..1)
                  |    |         > CST 01, 02, 05
                  |    |
                  |    +--- COFINSQtde (S03, 0..1)
                  |    |         > CST 03
                  |    |
                  |    +--- COFINSNT (S04, 0..1)
                  |    |         > Não Tributado
                  |    |         > CST 04, 06, 07, 08, 09
                  |    |
                  |    +--- COFINSSN (S05, 0..1)
                  |    |         > Simples Nacional
                  |    |         > CST 49
                  |    +--- COFINSOutr (S06, 0..1)
                  |              > Outras Operações
                  |              > CST 99
                  |
                  +--- COFINSST (T01, 0..1)
                  |          > Substituição Tributária
                  |
                  +--- ISSQN (U01, 0..1)


Totais:

    .. sourcecode:: text

        infCFe (A01, 1)
        |
        +--- total (W01, 1)
        |    |
        |    +--- ICMSTot (W02, 0..1)
        |    |          > Neste grupo, todos os elementos
        :    |          > são calculados pelo equipamento SAT
        :    |
        .    +--- ISSQNTot (W12, 0..1)
        .    |          > Neste grupo, todos os elementos
             |          > são calculados pelo equipamento SAT
             |
             +--- DescAcrEntr (W19, 0..1)


Pagamento:

    .. sourcecode:: text

        infCFe (A01, 1)
        |
        +--- pgto (WA01, 1)
        :    |
             +--- MP (WA02, 1..10)

"""

import re
import xml.etree.ElementTree as ET

from decimal import Decimal

import cerberus

from unidecode import unidecode

from satcomum import br
from satcomum import constantes


class ExtendedValidator(cerberus.Validator):

    def _validate_type_decimal(self, field, value):
        if not isinstance(value, Decimal):
            self._error(field,
                    cerberus.errors.ERROR_BAD_TYPE % Decimal.__name__)


    def _validate_type_ipv4(self, field, value):
            if isinstance(value, basestring):
                _bytes = [int(b, 10) for b in value.split('.') \
                        if int(b, 10) in xrange(0, 256)]
                if len(_bytes) != 4:
                    self._error(field, cerberus.errors.ERROR_BAD_TYPE % 'IPv4')


    def _validate_type_cnpj(self, field, value):
        if not br.is_cnpj(value, estrito=True):
            self._error(field, 'numero CNPJ "%s" invalido' % value)


    def _validate_type_assinatura_ac(self, field, value):
        if re.match(r'^[ -~]{344}$', value):
            # assume que quaisquer 344 'printable chars' formem uma
            # assinatura de AC válida...
            pass
        elif value == constantes.ASSINATURA_AC_TESTE:
            pass
        else:
            self._error(field, "campo '%s' nao possui uma assinatura AC "
                    "valida: %s" % (field, value,))


class Entidade(object):
    """Classe base para todas as classes que representem as entidades da
    implementação do SAT-CF-e. Aqui, chamaremos de "entidade" as classes que
    representem os grupos de dados que são usados para formar o XML do CF-e de
    venda ou de cancelamento.

    Basicamente, as subclasses precisam sobre-escrever a implementação do
    método ``_construir_elemento_xml``, definir o atributo ``_schema`` e,
    quando necessário, implementar uma especialização do validador `Cerberus`_
    no atributo ``_validator_class``.

    .. _`Cerberus`: http://docs.python-cerberus.org/

    """

    _erros = {}


    def __init__(self, schema={}, validator_class=None, **kwargs):
        super(Entidade, self).__init__()
        self._schema = schema
        self._validator_class = validator_class or ExtendedValidator
        self._validator = self._validator_class(self._schema)

        # define como atributos e valores desta instância os argumentos
        # nomeados, desde que coincidam com as chaves no schema
        for key, value in kwargs.items():
            if key not in self._schema.keys():
                raise AttributeError('{!r} object has no attribute {!r}'.format(
                        self.__class__.__name__, key))
            setattr(self, key, value)


    @property
    def erros(self):
        return dict(Entidade._erros)


    def validar(self):
        if not self._validator.validate(self._schema_fields()):
            nome_entidade = self.__class__.__name__
            Entidade._erros[nome_entidade] = self._validator.errors
            raise cerberus.ValidationError('Entidade "{}" possui '
                    'atributos invalidos.'.format(nome_entidade))


    def documento(self, *args, **kwargs):
        """Resulta no documento XML como string, que pode ou não incluir a
        declaração XML no início do documento.
        """
        forcar_unicode = kwargs.pop('forcar_unicode', False)
        incluir_xml_decl = kwargs.pop('incluir_xml_decl', True)
        doc = ET.tostring(self._xml(*args, **kwargs),
                encoding='utf-8').decode('utf-8')
        if forcar_unicode:
            if incluir_xml_decl:
                doc = u'{}\n{}'.format(constantes.XML_DECL_UNICODE, doc)
        else:
            if incluir_xml_decl:
                doc = '{}\n{}'.format(constantes.XML_DECL, unidecode(doc))
            else:
                doc = unidecode(doc)
        return doc


    def _xml(self, *args, **kwargs):
        self.validar()
        return self._construir_elemento_xml(*args, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        raise NotImplementedError()


    def _schema_fields(self):
        return {k: v for k, v in self.__dict__.items() if k in self._schema}



class Emitente(Entidade):
    """Identificação do emitente do CF-e (``emit``, grupo ``C01``).

    :param str CNPJ: Número do CNPJ do emitente do CF-e, contendo apenas os
        digitos e incluindo os zeros não significativos.

    :param str IE: Número de Inscrição Estadual do emitente do CF-e, contendo
        apenas digitos.

    :param str IM: *Opcional*. Deve ser informado o número da Inscrição
        Municipal quando o CF-e possuir itens com prestação de serviços
        sujeitos ao ISSQN, por exemplo.

    :param str cRegTribISSQN: *Opcional*. Indica o regime especial de tributação
        do ISSQN. Veja as constantes em
        :attr:`~satcomum.constantes.C15_CREGTRIBISSQN_EMIT`.

    :param str indRatISSQN: *Opcional*. Indicador de rateio do desconto sobre o
        subtotal entre itens sujeitos à tributação pelo ISSQN. Veja as
        constantes em :attr:`~satcomum.constantes.C16_INDRATISSQN_EMIT`.

    .. sourcecode:: python

        >>> emit = Emitente(CNPJ='08427847000169', IE='111222333444', indRatISSQN='S')
        >>> ET.tostring(emit._xml())
        '<emit><CNPJ>08427847000169</CNPJ><IE>111222333444</IE><indRatISSQN>S</indRatISSQN></emit>'

        >>> emit = Emitente(
        ...         CNPJ='08427847000169',
        ...         IE='111222333444',
        ...         IM='123456789012345',
        ...         cRegTribISSQN='1',
        ...         indRatISSQN='S')
        >>> ET.tostring(emit._xml())
        '<emit><CNPJ>08427847000169</CNPJ><IE>111222333444</IE><IM>123456789012345</IM><cRegTribISSQN>1</cRegTribISSQN><indRatISSQN>S</indRatISSQN></emit>'

    """

    def __init__(self, **kwargs):
        super(Emitente, self).__init__(schema={
                'CNPJ': {
                        'type': 'cnpj',
                        'required': True},
                'IE': {
                        'type': 'string',
                        'required': True,
                        'regex': r'^\d{2,12}$'},
                'IM': {
                        'type': 'string',
                        'required': False,
                        'regex': r'^\d{1,15}$'},
                'cRegTribISSQN': {
                        'type': 'string',
                        'required': False,
                        'allowed':
                                [v for v,s in constantes.C15_CREGTRIBISSQN_EMIT]},
                'indRatISSQN': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.C16_INDRATISSQN_EMIT]},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):

        emit = ET.Element('emit')
        ET.SubElement(emit, 'CNPJ').text = self.CNPJ
        ET.SubElement(emit, 'IE').text = self.IE

        if hasattr(self, 'IM'):
            ET.SubElement(emit, 'IM').text = self.IM

        if hasattr(self, 'cRegTribISSQN'):
            ET.SubElement(emit, 'cRegTribISSQN').text = self.cRegTribISSQN

        ET.SubElement(emit, 'indRatISSQN').text = self.indRatISSQN

        return emit


class Destinatario(Entidade):
    """Identificação do destinatário do CF-e (``dest``, grupo ``E01``).

    :param str CNPJ: Número do CNPJ do destinatário, contendo apenas os
        digitos e incluindo os zeros não significativos. **Não deve ser
        informado se o ``CPF`` for informado.**

    :param str CPF: Número do CPF do destinatário, contendo apenas os digitos e
        incluindo os zeros não significativos. **Não deve ser informado se o
        ``CNPJ`` for informado.**

    :param str xNome: *Opcional*. Nome ou razão social do destinatário.

    Note que os parâmetros ``CNPJ`` e ``CPF`` são mutuamente exclusivos.

    .. sourcecode:: python

        >>> dest = Destinatario()
        >>> ET.tostring(dest._xml(), encoding='utf-8')
        '<dest />'
        >>> dest = Destinatario(CNPJ='08427847000169')
        >>> ET.tostring(dest._xml(), encoding='utf-8')
        '<dest><CNPJ>08427847000169</CNPJ></dest>'
        >>> dest = Destinatario(CPF='11122233396', xNome=u'Fulano Beltrano')
        >>> ET.tostring(dest._xml(), encoding='utf-8')
        '<dest><CPF>11122233396</CPF><xNome>Fulano Beltrano</xNome></dest>'
        >>> dest = Destinatario(CPF='11122233396', CNPJ='08427847000169')
        >>> dest._xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # testa criação do XML para cancelamento; o nome deverá ser ignorado
        >>> dest = Destinatario(CPF='11122233396', xNome=u'Fulano Beltrano')
        >>> ET.tostring(dest._xml(cancelamento=True), encoding='utf-8')
        '<dest><CPF>11122233396</CPF></dest>'

    """

    class _Validator(ExtendedValidator):

        def _validate_type_CNPJ_E02(self, field, value):
            if 'CPF' in self.document:
                self._error(field,
                        u'CNPJ (E02) e CPF (E03) são mutuamente exclusivos.')
            elif not br.is_cnpj(value):
                self._error(field, u'CNPJ (E02) não é válido: "%s"' % value)

        def _validate_type_CPF_E03(self, field, value):
            if 'CNPJ' in self.document:
                self._error(field,
                        u'CNPJ (E02) e CPF (E03) são mutuamente exclusivos.')
            elif not br.is_cpf(value):
                self._error(field, u'CPF (E03) não é válido: "%s"' % value)


    def __init__(self, **kwargs):
        super(Destinatario, self).__init__(schema={
                'CNPJ': {'type': 'CNPJ_E02'}, # E02
                'CPF': {'type': 'CPF_E03'}, # E03
                'xNome': { # E04
                        'type': 'string',
                        'required': False,
                        'minlength': 2, 'maxlength': 60}
            }, validator_class=Destinatario._Validator, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):

        is_cancelamento = kwargs.pop('cancelamento', False)

        dest = ET.Element('dest')

        if hasattr(self, 'CNPJ'):
            ET.SubElement(dest, 'CNPJ').text = self.CNPJ

        if hasattr(self, 'CPF'):
            ET.SubElement(dest, 'CPF').text = self.CPF

        if hasattr(self, 'xNome') and not is_cancelamento:
            ET.SubElement(dest, 'xNome').text = self.xNome

        return dest


class LocalEntrega(Entidade):
    """Identificação do Local de Entrega (``entrega``, grupo ``G01``).

    :param str xLgr:
    :param str nro:
    :param str xCpl: *Opcional*
    :param str xBairro:
    :param str xMun:
    :param str UF:

    .. sourcecode:: python

        >>> entrega = LocalEntrega()
        >>> ET.tostring(entrega._xml(), encoding='utf-8')
        Traceback (most recent call last):
         ...
        ValidationError: ...
        >>> entrega.xLgr = 'Rua Armando Gulim'
        >>> entrega.nro = '65'
        >>> entrega.xBairro = 'Parque Gloria III'
        >>> entrega.xMun = 'Catanduva'
        >>> entrega.UF = 'SP'
        >>> ET.tostring(entrega._xml(), encoding='utf-8')
        '<entrega><xLgr>Rua Armando Gulim</xLgr><nro>65</nro><xBairro>Parque Gloria III</xBairro><xMun>Catanduva</xMun><UF>SP</UF></entrega>'

    """

    class _Validator(ExtendedValidator):
        def _validate_type_UF_G07(self, field, value):
            if not br.is_uf(value):
                self._error(field, u'UF (G07) do Local de Entrega, '
                        u'não é válido: "%s"' % value)


    def __init__(self, **kwargs):
        super(LocalEntrega, self).__init__(schema={
                'xLgr': { # G02
                        'type': 'string',
                        'required': True,
                        'minlength': 2, 'maxlength': 60},
                'nro': { # G03
                        'type': 'string',
                        'required': True,
                        'minlength': 1, 'maxlength': 60},
                'xCpl': { # G04
                        'type': 'string',
                        'required': False,
                        'minlength': 1, 'maxlength': 60},
                'xBairro': { # G05
                        'type': 'string',
                        'required': True,
                        'minlength': 1, 'maxlength': 60},
                'xMun': { # G06
                        'type': 'string',
                        'required': True,
                        'minlength': 2, 'maxlength': 60},
                'UF': { # G07
                        'type': 'UF_G07',
                        'required': True},
            }, validator_class=LocalEntrega._Validator, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):

        entrega = ET.Element('entrega')
        ET.SubElement(entrega, 'xLgr').text = self.xLgr
        ET.SubElement(entrega, 'nro').text = self.nro

        if hasattr(self, 'xCpl'):
            ET.SubElement(entrega, 'xCpl').text = self.xCpl

        ET.SubElement(entrega, 'xBairro').text = self.xBairro
        ET.SubElement(entrega, 'xMun').text = self.xMun
        ET.SubElement(entrega, 'UF').text = self.UF

        return entrega


class Detalhamento(Entidade):
    """Detalhamento do produto ou serviço do CF-e (``det``, grupo ``H01``).

    :param ProdutoServico produto:
    :param Imposto imposto:
    :param str infAdProd: *Opcional*

    Note que o atributo XML ``nItem`` (``H02``) não é determinado aqui, mas
    atribuído automaticamente, conforme a sua posição na lista de
    :attr:`~CFeVenda.detalhamentos`.

    .. sourcecode:: python

        >>> det = Detalhamento(
        ...         produto=ProdutoServico(
        ...                 cProd='123456',
        ...                 xProd='BORRACHA STAEDTLER',
        ...                 CFOP='5102',
        ...                 uCom='UN',
        ...                 qCom=Decimal('1.0000'),
        ...                 vUnCom=Decimal('5.75'),
        ...                 indRegra='A'),
        ...         imposto=Imposto(
        ...                 pis=PISSN(CST='49'),
        ...                 cofins=COFINSSN(CST='49'),
        ...                 icms=ICMSSN102(Orig='2', CSOSN='500')),
        ...         infAdProd='Teste')
        >>> ET.tostring(det._xml(nItem=1))
        '<det nItem="1"><prod><cProd>123456</cProd><xProd>BORRACHA STAEDTLER</xProd><CFOP>5102</CFOP><uCom>UN</uCom><qCom>1.0000</qCom><vUnCom>5.75</vUnCom><indRegra>A</indRegra></prod><imposto><ICMS><ICMSSN102><Orig>2</Orig><CSOSN>500</CSOSN></ICMSSN102></ICMS><PIS><PISSN><CST>49</CST></PISSN></PIS><COFINS><COFINSSN><CST>49</CST></COFINSSN></COFINS></imposto><infAdProd>Teste</infAdProd></det>'

    """

    def __init__(self, produto=None, imposto=None, **kwargs):
        self._produto = produto
        self._imposto = imposto
        super(Detalhamento, self).__init__(schema={
               'infAdProd': {
                        'type': 'string',
                        'required': False,
                        'minlength': 1, 'maxlength': 500},
            }, **kwargs)


    @property
    def produto(self):
        """O produto ou serviço como uma instância de :class:`ProdutoServico`
        ao qual o detalhamento se refere.
        """
        return self._produto


    @property
    def imposto(self):
        """O grupo de tributos incidentes no produto ou serviço ao qual o
        detalhamento se refere, como uma instância de :class:`Imposto`.
        """
        return self._imposto


    def _construir_elemento_xml(self, *args, **kwargs):

        det = ET.Element('det')
        det.attrib['nItem'] = str(kwargs.pop('nItem'))

        det.append(self.produto._xml())
        det.append(self.imposto._xml())

        if hasattr(self, 'infAdProd'):
            ET.SubElement(det, 'infAdProd').text = self.infAdProd

        return det


class ProdutoServico(Entidade):
    """Produto ou serviço do CF-e (``prod``, grupo ``I01``).

    :param str cProd:
    :param str cEAN: *Opcional*
    :param str xProd:
    :param str NCM: *Opcional*
    :param str CFOP:
    :param str uCom:
    :param Decimal qCom:
    :param Decimal vUnCom:
    :param str indRegra:
    :param Decimal vDesc: *Opcional*
    :param Decimal vOutro: *Opcional*
    :param list observacoes_fisco: *Opcional*

    .. sourcecode:: python

        # apenas os atributos requeridos;
        # note que, diferente da NF-e/NFC-e a ER SAT indica que o
        # atributo NCM não é obrigatório
        >>> prod = ProdutoServico(
        ...         cProd='123456',
        ...         xProd='BORRACHA STAEDTLER',
        ...         CFOP='5102',
        ...         uCom='UN',
        ...         qCom=Decimal('1.0000'),
        ...         vUnCom=Decimal('5.75'),
        ...         indRegra='A')
        >>> ET.tostring(prod._xml())
        '<prod><cProd>123456</cProd><xProd>BORRACHA STAEDTLER</xProd><CFOP>5102</CFOP><uCom>UN</uCom><qCom>1.0000</qCom><vUnCom>5.75</vUnCom><indRegra>A</indRegra></prod>'

        # todos os atributos (se vDesc for informado, então não informa vOutro)
        >>> prod = ProdutoServico(
        ...         cProd='123456',
        ...         cEAN='4007817525074',
        ...         xProd='BORRACHA STAEDTLER',
        ...         NCM='40169200',
        ...         CFOP='5102',
        ...         uCom='UN',
        ...         qCom=Decimal('1.0000'),
        ...         vUnCom=Decimal('5.75'),
        ...         indRegra='A',
        ...         vDesc=Decimal('0.25'))
        >>> ET.tostring(prod._xml())
        '<prod><cProd>123456</cProd><cEAN>4007817525074</cEAN><xProd>BORRACHA STAEDTLER</xProd><NCM>40169200</NCM><CFOP>5102</CFOP><uCom>UN</uCom><qCom>1.0000</qCom><vUnCom>5.75</vUnCom><indRegra>A</indRegra><vDesc>0.25</vDesc></prod>'

        # todos os atributos (informando vOutro)
        >>> prod = ProdutoServico(
        ...         cProd='123456',
        ...         cEAN='4007817525074',
        ...         xProd='BORRACHA STAEDTLER',
        ...         NCM='40169200',
        ...         CFOP='5102',
        ...         uCom='UN',
        ...         qCom=Decimal('1.0000'),
        ...         vUnCom=Decimal('5.75'),
        ...         indRegra='A',
        ...         vOutro=Decimal('0.25'))
        >>> ET.tostring(prod._xml())
        '<prod><cProd>123456</cProd><cEAN>4007817525074</cEAN><xProd>BORRACHA STAEDTLER</xProd><NCM>40169200</NCM><CFOP>5102</CFOP><uCom>UN</uCom><qCom>1.0000</qCom><vUnCom>5.75</vUnCom><indRegra>A</indRegra><vOutro>0.25</vOutro></prod>'

        # informa vDesc e vOutro, não deve validar
        >>> prod = ProdutoServico(
        ...         cProd='123456',
        ...         xProd='BORRACHA STAEDTLER',
        ...         CFOP='5102',
        ...         uCom='UN',
        ...         qCom=Decimal('1.0000'),
        ...         vUnCom=Decimal('5.75'),
        ...         indRegra='A',
        ...         vDesc=Decimal('0.25'),
        ...         vOutro=Decimal('0.25'))
        >>> prod._xml()
        Traceback (most recent call last):
         ...
        ValidationError: 'ProdutoServico' (grupo H01 'prod') atributos 'vDesc' e 'vOutro' sao mutuamente exclusivos

    """

    def __init__(self, observacoes_fisco=[], **kwargs):
        self._observacoes_fisco = observacoes_fisco
        super(ProdutoServico, self).__init__(schema={
                'cProd': { # I02
                        'type': 'string',
                        'required': True,
                        'minlength': 1, 'maxlength': 60},
                'cEAN': { # I03
                        'type': 'string',
                        'required': False,
                        'regex': r'^(\d{8}|\d{12}|\d{13}|\d{14})$'},
                'xProd': { # I04
                        'type': 'string',
                        'required': True,
                        'minlength': 1, 'maxlength': 120},
                'NCM': { # I05
                        'type': 'string',
                        'required': False,
                        'regex': r'^(\d{2}|\d{8})$'},
                'CFOP': { # I06
                        'type': 'string',
                        'required': True,
                        'regex': r'^\d{4}$'},
                'uCom': { # I07
                        'type': 'string',
                        'required': True,
                        'minlength': 1, 'maxlength': 6},
                'qCom': { # I08
                        'type': 'decimal',
                        'required': True},
                'vUnCom': { # I09
                        'type': 'decimal',
                        'required': True},
                'indRegra': { # I11
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.I11_INDREGRA]},
                'vDesc': { # I12
                        'type': 'decimal',
                        'required': False},
                'vOutro': { # I13
                        'type': 'decimal',
                        'required': False},
            }, **kwargs)


    @property
    def observacoes_fisco(self):
        """Cada produto, pode opcionalmente, conter uma lista de campos de uso
        livre do fisco, cujos campos e valores são representados por instâncias
        da classe :class:`ObsFiscoDet`.
        """
        return self._observacoes_fisco


    def _construir_elemento_xml(self, *args, **kwargs):

        if hasattr(self, 'vDesc') and hasattr(self, 'vOutro'):
            raise cerberus.ValidationError("'%s' (grupo H01 'prod') atributos "
                    "'vDesc' e 'vOutro' sao mutuamente exclusivos" %
                    self.__class__.__name__)

        prod = ET.Element('prod')
        ET.SubElement(prod, 'cProd').text = self.cProd

        if hasattr(self, 'cEAN'):
            ET.SubElement(prod, 'cEAN').text = self.cEAN

        ET.SubElement(prod, 'xProd').text = self.xProd

        if hasattr(self, 'NCM'):
            ET.SubElement(prod, 'NCM').text = self.NCM

        ET.SubElement(prod, 'CFOP').text = self.CFOP
        ET.SubElement(prod, 'uCom').text = self.uCom
        ET.SubElement(prod, 'qCom').text = str(self.qCom)
        ET.SubElement(prod, 'vUnCom').text = str(self.vUnCom)
        ET.SubElement(prod, 'indRegra').text = self.indRegra

        if hasattr(self, 'vDesc'):
            ET.SubElement(prod, 'vDesc').text = str(self.vDesc)

        if hasattr(self, 'vOutro'):
            ET.SubElement(prod, 'vOutro').text = str(self.vOutro)

        if self.observacoes_fisco:
            for obs in self.observacoes_fisco:
                prod.append(obs._xml())

        return prod


class ObsFiscoDet(Entidade):
    """Grupo do campo de uso livre do Fisco (``obsFiscoDet``, grupo ``I17``).

    :param str xCampoDet:
    :param str xTextoDet:

    .. sourcecode:: python

        >>> obs = ObsFiscoDet(xCampoDet='Cod. Produto ANP', xTextoDet='320101001')
        >>> ET.tostring(obs._xml())
        '<obsFiscoDet xCampoDet="Cod. Produto ANP"><xTextoDet>320101001</xTextoDet></obsFiscoDet>'

    """

    def __init__(self, **kwargs):
        super(ObsFiscoDet, self).__init__(schema={
                'xCampoDet': {
                        'type': 'string',
                        'required': True,
                        'minlength': 1, 'maxlength': 20},
                'xTextoDet': {
                        'type': 'string',
                        'required': True,
                        'minlength': 1, 'maxlength': 60},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        obs = ET.Element('obsFiscoDet')
        obs.attrib['xCampoDet'] = self.xCampoDet
        ET.SubElement(obs, 'xTextoDet').text = self.xTextoDet
        return obs


class ICMS00(Entidade):
    """Grupo de tributação do ICMS 00, 20 e 90 (``ICMS00``, grupo ``N02``).

    :param str Orig:
    :param str CST:
    :param Decimal pICMS:

    .. sourcecode:: python

        >>> icms = ICMS00(Orig='0', CST='00', pICMS=Decimal('18.00'))
        >>> ET.tostring(icms._xml())
        '<ICMS00><Orig>0</Orig><CST>00</CST><pICMS>18.00</pICMS></ICMS00>'

    """

    def __init__(self, **kwargs):
        super(ICMS00, self).__init__(schema={
                'Orig': { # N06
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.N06_ORIG]},
                'CST': { # N07
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.N07_CST_ICMS00]},
                'pICMS': {
                        'type': 'decimal',
                        'required': True},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        icms00 = ET.Element(self.__class__.__name__)
        ET.SubElement(icms00, 'Orig').text = self.Orig
        ET.SubElement(icms00, 'CST').text = self.CST
        ET.SubElement(icms00, 'pICMS').text = str(self.pICMS)
        return icms00


class ICMS40(Entidade):
    """Grupo de tributação do ICMS 40, 41 e 60 (``ICMS40``, grupo ``N03``).

    :param str Orig:
    :param str CST:

    .. sourcecode:: python

        >>> icms = ICMS40(Orig='0', CST='60')
        >>> ET.tostring(icms._xml())
        '<ICMS40><Orig>0</Orig><CST>60</CST></ICMS40>'

    """

    def __init__(self, **kwargs):
        super(ICMS40, self).__init__(schema={
                'Orig': { # N06
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.N06_ORIG]},
                'CST': { # N07
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.N07_CST_ICMS40]},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        icms40 = ET.Element('ICMS40')
        ET.SubElement(icms40, 'Orig').text = self.Orig
        ET.SubElement(icms40, 'CST').text = self.CST
        return icms40


class ICMSSN102(Entidade):
    """Grupo de tributação do ICMS Simples Nacional, CSOSN 102, 300, 400 e 500
    (``ICMSSN102``, grupo ``N04``).

    :param str Orig:
    :param str CSOSN:

    .. sourcecode:: python

        >>> icms = ICMSSN102(Orig='0', CSOSN='500')
        >>> ET.tostring(icms._xml())
        '<ICMSSN102><Orig>0</Orig><CSOSN>500</CSOSN></ICMSSN102>'

    """

    def __init__(self, **kwargs):
        super(ICMSSN102, self).__init__(schema={
                'Orig': { # N06
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.N06_ORIG]},
                'CSOSN': { # N10
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.N10_CSOSN_ICMSSN102]},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        icmssn102 = ET.Element('ICMSSN102')
        ET.SubElement(icmssn102, 'Orig').text = self.Orig
        ET.SubElement(icmssn102, 'CSOSN').text = self.CSOSN
        return icmssn102


class ICMSSN900(Entidade):
    """Grupo de tributação do ICMS Simples Nacional, CSOSN 900 (``ICMSSN900``,
    grupo ``N05``).

    :param str Orig:
    :param str CSOSN:
    :param Decimal pICMS:

    .. sourcecode:: python

        >>> icms = ICMSSN900(Orig='0', CSOSN='900', pICMS=Decimal('18.00'))
        >>> ET.tostring(icms._xml())
        '<ICMSSN900><Orig>0</Orig><CSOSN>900</CSOSN><pICMS>18.00</pICMS></ICMSSN900>'

    """

    def __init__(self, **kwargs):
        super(ICMSSN900, self).__init__(schema={
                'Orig': { # N06
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.N06_ORIG]},
                'CSOSN': { # N10
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.N10_CSOSN_ICMSSN900]},
                'pICMS': {
                        'type': 'decimal',
                        'required': True},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        icmssn900 = ET.Element('ICMSSN900')
        ET.SubElement(icmssn900, 'Orig').text = self.Orig
        ET.SubElement(icmssn900, 'CSOSN').text = self.CSOSN
        ET.SubElement(icmssn900, 'pICMS').text = str(self.pICMS)
        return icmssn900


class PISAliq(Entidade):
    """Grupo de PIS tributado pela alíquota, CST 01, 02 ou 05 (``PISAliq``,
    grupo ``Q02``).

    :param str CST:
    :param Decimal vBC:
    :param Decimal pPIS:

    .. sourcecode:: python

        >>> pis = PISAliq(CST='01', vBC=Decimal('1.00'), pPIS=Decimal('0.0065'))
        >>> ET.tostring(pis._xml())
        '<PISAliq><CST>01</CST><vBC>1.00</vBC><pPIS>0.0065</pPIS></PISAliq>'

    """

    def __init__(self, **kwargs):
        super(PISAliq, self).__init__(schema={
                'CST': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.Q07_CST_PISALIQ]},
                'vBC': {
                        'type': 'decimal',
                        'required': True},
                'pPIS': {
                        'type': 'decimal',
                        'required': True},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        pisaliq = ET.Element('PISAliq')
        ET.SubElement(pisaliq, 'CST').text = self.CST
        ET.SubElement(pisaliq, 'vBC').text = str(self.vBC)
        ET.SubElement(pisaliq, 'pPIS').text = str(self.pPIS)
        return pisaliq


class PISQtde(Entidade):
    """Grupo de PIS tributado por quantidade, CST 03 (``PISQtde``,
    grupo ``Q03``).

    :param str CST:
    :param Decimal qBCProd:
    :param Decimal vAliqProd:

    .. sourcecode:: python

        >>> pis = PISQtde(CST='03', qBCProd=Decimal('100.0000'), vAliqProd=Decimal('0.6500'))
        >>> ET.tostring(pis._xml())
        '<PISQtde><CST>03</CST><qBCProd>100.0000</qBCProd><vAliqProd>0.6500</vAliqProd></PISQtde>'

    """

    def __init__(self, **kwargs):
        super(PISQtde, self).__init__(schema={
                'CST': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.Q07_CST_PISQTDE]},
                'qBCProd': {
                        'type': 'decimal',
                        'required': True},
                'vAliqProd': {
                        'type': 'decimal',
                        'required': True},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        pisqtde = ET.Element('PISQtde')
        ET.SubElement(pisqtde, 'CST').text = self.CST
        ET.SubElement(pisqtde, 'qBCProd').text = str(self.qBCProd)
        ET.SubElement(pisqtde, 'vAliqProd').text = str(self.vAliqProd)
        return pisqtde


class PISNT(Entidade):
    """Grupo de PIS não tributado, CST 04, 06, 07 08 ou 09 (``PISNT``,
    grupo ``Q04``).

    :param str CST:

    .. sourcecode:: python

        >>> pis = PISNT(CST='04')
        >>> ET.tostring(pis._xml())
        '<PISNT><CST>04</CST></PISNT>'

    """

    def __init__(self, **kwargs):
        super(PISNT, self).__init__(schema={
                'CST': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.Q07_CST_PISNT]},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        pisnt = ET.Element('PISNT')
        ET.SubElement(pisnt, 'CST').text = self.CST
        return pisnt


class PISSN(Entidade):
    """Grupo de PIS para contribuíntes do Simples Nacional, CST 49 (``PISSN``,
    grupo ``Q05``).

    :param str CST:

    .. sourcecode:: python

        >>> pis = PISSN(CST='49')
        >>> ET.tostring(pis._xml())
        '<PISSN><CST>49</CST></PISSN>'

    """

    def __init__(self, **kwargs):
        super(PISSN, self).__init__(schema={
                'CST': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.Q07_CST_PISSN]},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        pissn = ET.Element('PISSN')
        ET.SubElement(pissn, 'CST').text = self.CST
        return pissn


class PISOutr(Entidade):
    """Grupo de PIS para outras operações, CST 99 (``PISOutr``, grupo ``Q06``).

    :param str CST:

    :param str vBC: *Opcional* Se informado deverá ser também informado o
        parâmetro ``pPIS``.

    :param str pPIS: *Opcional* Se informado deverá ser também informado o
        parâmetro ``vBC``.

    :param str qBCProd: *Opcional* Se informado deverá ser também informado o
        parâmetro ``vAliqProd``.

    :param str vAliqProd: *Opcional* Se informado deverá ser também informado o
        parâmetro ``qBCProd``.

    Os parâmetros ``vBC`` e ``qBCProd`` são mutuamente exclusivos, e um ou
    outro **devem** ser informados.

    .. sourcecode:: python

        >>> pis = PISOutr(CST='99', vBC=Decimal('1.00'), pPIS=Decimal('0.0065'))
        >>> ET.tostring(pis._xml())
        '<PISOutr><CST>99</CST><vBC>1.00</vBC><pPIS>0.0065</pPIS></PISOutr>'
        >>> pis = PISOutr(CST='99', qBCProd=Decimal('100.0000'), vAliqProd=Decimal('0.6500'))
        >>> ET.tostring(pis._xml())
        '<PISOutr><CST>99</CST><qBCProd>100.0000</qBCProd><vAliqProd>0.6500</vAliqProd></PISOutr>'

        # atributo vBC depende de pPIS que não foi informado
        >>> pis = PISOutr(CST='99', vBC=Decimal('1.00')) # vBC depende de pPIS
        >>> pis._xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # atributo qBCProd depende de vAliqProd que não foi informado
        >>> pis = PISOutr(CST='99', qBCProd=Decimal('100.0000'))
        >>> pis._xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # neste caso, deve falhar pois vBC ou qBCProd não foram informados
        >>> pis = PISOutr(CST='99')
        >>> pis._xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'PISOutr' requer exclusivamente 'vBC' ou 'qBCProd' (nenhum informado)

        # neste caso, deve falhar pois apenas um ou outro grupo pode ser informado:
        # ou informa-se vBC e pPIS ou informa-se qBCProd e vAliqProd
        >>> pis = PISOutr(CST='99', vBC=Decimal('1.00'), pPIS=Decimal('1.00'), qBCProd=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> pis._xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'PISOutr' requer exclusivamente 'vBC' ou 'qBCProd' (ambos informados)

        # neste caso as falhara pela ausencia das dependencias:
        # pPIS depende de vBC e vAliqProd depende de qBCProd
        >>> pis = PISOutr(CST='99', pPIS=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> pis._xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

    """

    def __init__(self, **kwargs):
        super(PISOutr, self).__init__(schema={
                'CST': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.Q07_CST_PISOUTR]},
                'vBC': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['pPIS']},
                'pPIS': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['vBC']},
                'qBCProd': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['vAliqProd']},
                'vAliqProd': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['qBCProd']},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):

        if hasattr(self, 'vBC') and hasattr(self, 'qBCProd'):
            raise cerberus.ValidationError("Grupo '%s' requer "
                    "exclusivamente 'vBC' ou 'qBCProd' (ambos informados)" %
                    self.__class__.__name__)

        elif not hasattr(self, 'vBC') and not hasattr(self, 'qBCProd'):
            raise cerberus.ValidationError("Grupo '%s' requer "
                    "exclusivamente 'vBC' ou 'qBCProd' (nenhum informado)" %
                    self.__class__.__name__)

        pisoutr = ET.Element(self.__class__.__name__)
        ET.SubElement(pisoutr, 'CST').text = self.CST

        if hasattr(self, 'vBC'):
            ET.SubElement(pisoutr, 'vBC').text = str(self.vBC)
            ET.SubElement(pisoutr, 'pPIS').text = str(self.pPIS)

        elif hasattr(self, 'qBCProd'):
            ET.SubElement(pisoutr, 'qBCProd').text = str(self.qBCProd)
            ET.SubElement(pisoutr, 'vAliqProd').text = \
                    str(self.vAliqProd)

        return pisoutr


class PISST(Entidade):
    """Grupo de PIS substituição tributária (``PISST``, grupo ``R01``).

    :param str vBC: *Opcional* Se informado deverá ser também informado o
        parâmetro ``pPIS``.

    :param str pPIS: *Opcional* Se informado deverá ser também informado o
        parâmetro ``vBC``.

    :param str qBCProd: *Opcional* Se informado deverá ser também informado o
        parâmetro ``vAliqProd``.

    :param str vAliqProd: *Opcional* Se informado deverá ser também informado o
        parâmetro ``qBCProd``.

    Os parâmetros ``vBC`` e ``qBCProd`` são mutuamente exclusivos, e um ou
    outro **devem** ser informados.

    .. sourcecode:: python

        >>> pis = PISST(vBC=Decimal('1.00'), pPIS=Decimal('0.0065'))
        >>> ET.tostring(pis._xml())
        '<PISST><vBC>1.00</vBC><pPIS>0.0065</pPIS></PISST>'
        >>> pis = PISST(qBCProd=Decimal('100.0000'), vAliqProd=Decimal('0.6500'))
        >>> ET.tostring(pis._xml())
        '<PISST><qBCProd>100.0000</qBCProd><vAliqProd>0.6500</vAliqProd></PISST>'

        # atributo vBC depende de pPIS que não foi informado
        >>> pis = PISST(vBC=Decimal('1.00')) # vBC depende de pPIS
        >>> pis._xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # atributo qBCProd depende de vAliqProd que não foi informado
        >>> pis = PISST(qBCProd=Decimal('100.0000'))
        >>> pis._xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # neste caso, deve falhar pois vBC ou qBCProd não foram informados
        >>> pis = PISST()
        >>> pis._xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'PISST' requer exclusivamente 'vBC' ou 'qBCProd' (nenhum informado)

        # neste caso, deve falhar pois apenas um ou outro grupo pode ser informado:
        # ou informa-se vBC e pPIS ou informa-se qBCProd e vAliqProd
        >>> pis = PISST(vBC=Decimal('1.00'), pPIS=Decimal('1.00'), qBCProd=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> pis._xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'PISST' requer exclusivamente 'vBC' ou 'qBCProd' (ambos informados)

        # neste caso as falhara pela ausencia das dependencias:
        # pPIS depende de vBC e vAliqProd depende de qBCProd
        >>> pis = PISST(pPIS=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> pis._xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

    """

    def __init__(self, **kwargs):
        super(PISST, self).__init__(schema={
                'vBC': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['pPIS']},
                'pPIS': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['vBC']},
                'qBCProd': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['vAliqProd']},
                'vAliqProd': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['qBCProd']},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):

        if hasattr(self, 'vBC') and hasattr(self, 'qBCProd'):
            raise cerberus.ValidationError("Grupo '%s' requer "
                    "exclusivamente 'vBC' ou 'qBCProd' (ambos informados)" %
                    self.__class__.__name__)

        elif not hasattr(self, 'vBC') and not hasattr(self, 'qBCProd'):
            raise cerberus.ValidationError("Grupo '%s' requer "
                    "exclusivamente 'vBC' ou 'qBCProd' (nenhum informado)" %
                    self.__class__.__name__)

        pisst = ET.Element(self.__class__.__name__)

        if hasattr(self, 'vBC'):
            ET.SubElement(pisst, 'vBC').text = str(self.vBC)
            ET.SubElement(pisst, 'pPIS').text = str(self.pPIS)

        elif hasattr(self, 'qBCProd'):
            ET.SubElement(pisst, 'qBCProd').text = str(self.qBCProd)
            ET.SubElement(pisst, 'vAliqProd').text = \
                    str(self.vAliqProd)

        return pisst


class COFINSAliq(Entidade):
    """Grupo de COFINS tributado pela alíquota, CST 01, 02 ou 05
    (``COFINSAliq``, grupo ``S02``).

    :param str CST:
    :param Decimal vBC:
    :param Decimal pCOFINS:

    .. sourcecode:: python

        >>> cofins = COFINSAliq(CST='01', vBC=Decimal('1.00'), pCOFINS=Decimal('0.0065'))
        >>> ET.tostring(cofins._xml())
        '<COFINSAliq><CST>01</CST><vBC>1.00</vBC><pCOFINS>0.0065</pCOFINS></COFINSAliq>'

    """

    def __init__(self, **kwargs):
        super(COFINSAliq, self).__init__(schema={
                'CST': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.S07_CST_COFINSALIQ]},
                'vBC': {
                        'type': 'decimal',
                        'required': True},
                'pCOFINS': {
                        'type': 'decimal',
                        'required': True},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        cofinsaliq = ET.Element(self.__class__.__name__)
        ET.SubElement(cofinsaliq, 'CST').text = self.CST
        ET.SubElement(cofinsaliq, 'vBC').text = str(self.vBC)
        ET.SubElement(cofinsaliq, 'pCOFINS').text = str(self.pCOFINS)
        return cofinsaliq


class COFINSQtde(Entidade):
    """Grupo de COFINS tributado por quantidade, CST 03 (``COFINSQtde``,
    grupo ``S03``).

    :param str CST:
    :param Decimal qBCProd:
    :param Decimal vAliqProd:

    .. sourcecode:: python

        >>> cofins = COFINSQtde(CST='03', qBCProd=Decimal('100.0000'), vAliqProd=Decimal('0.6500'))
        >>> ET.tostring(cofins._xml())
        '<COFINSQtde><CST>03</CST><qBCProd>100.0000</qBCProd><vAliqProd>0.6500</vAliqProd></COFINSQtde>'

    """

    def __init__(self, **kwargs):
        super(COFINSQtde, self).__init__(schema={
                'CST': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.S07_CST_COFINSQTDE]},
                'qBCProd': {
                        'type': 'decimal',
                        'required': True},
                'vAliqProd': {
                        'type': 'decimal',
                        'required': True},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        cofinsqtde = ET.Element(self.__class__.__name__)
        ET.SubElement(cofinsqtde, 'CST').text = self.CST
        ET.SubElement(cofinsqtde, 'qBCProd').text = str(self.qBCProd)
        ET.SubElement(cofinsqtde, 'vAliqProd').text = \
                str(self.vAliqProd)
        return cofinsqtde


class COFINSNT(Entidade):
    """Grupo de COFINS não tributado, CST 04, 06, 07 08 ou 09 (``COFINSNT``,
    grupo ``S04``).

    :param str CST:

    .. sourcecode:: python

        >>> cofins = COFINSNT(CST='04')
        >>> ET.tostring(cofins._xml())
        '<COFINSNT><CST>04</CST></COFINSNT>'

    """

    def __init__(self, **kwargs):
        super(COFINSNT, self).__init__(schema={
                'CST': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.S07_CST_COFINSNT]},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        cofinsnt = ET.Element(self.__class__.__name__)
        ET.SubElement(cofinsnt, 'CST').text = self.CST
        return cofinsnt


class COFINSSN(Entidade):
    """Grupo de COFINS para contribuíntes do Simples Nacional, CST 49
    (``COFINSSN``, grupo ``S05``).

    :param str CST:

    .. sourcecode:: python

        >>> cofins = COFINSSN(CST='49')
        >>> ET.tostring(cofins._xml())
        '<COFINSSN><CST>49</CST></COFINSSN>'

    """

    def __init__(self, **kwargs):
        super(COFINSSN, self).__init__(schema={
                'CST': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.S07_CST_COFINSSN]},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        cofinssn = ET.Element(self.__class__.__name__)
        ET.SubElement(cofinssn, 'CST').text = self.CST
        return cofinssn


class COFINSOutr(Entidade):
    """Grupo de COFINS para outras operações, CST 99 (``COFINSOutr``,
    grupo ``S06``).

    :param str CST:

    :param str vBC: *Opcional* Se informado deverá ser também informado o
        parâmetro ``pCOFINS``.

    :param str pCOFINS: *Opcional* Se informado deverá ser também informado o
        parâmetro ``vBC``.

    :param str qBCProd: *Opcional* Se informado deverá ser também informado o
        parâmetro ``vAliqProd``.

    :param str vAliqProd: *Opcional* Se informado deverá ser também informado o
        parâmetro ``qBCProd``.

    Os parâmetros ``vBC`` e ``qBCProd`` são mutuamente exclusivos, e um ou
    outro **devem** ser informados.

    .. sourcecode:: python

        >>> cofins = COFINSOutr(CST='99', vBC=Decimal('1.00'), pCOFINS=Decimal('0.0065'))
        >>> ET.tostring(cofins._xml())
        '<COFINSOutr><CST>99</CST><vBC>1.00</vBC><pCOFINS>0.0065</pCOFINS></COFINSOutr>'
        >>> cofins = COFINSOutr(CST='99', qBCProd=Decimal('100.0000'), vAliqProd=Decimal('0.6500'))
        >>> ET.tostring(cofins._xml())
        '<COFINSOutr><CST>99</CST><qBCProd>100.0000</qBCProd><vAliqProd>0.6500</vAliqProd></COFINSOutr>'

        # atributo vBC depende de pCOFINS que não foi informado
        >>> cofins = COFINSOutr(CST='99', vBC=Decimal('1.00')) # vBC depende de pCOFINS
        >>> cofins._xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # atributo qBCProd depende de vAliqProd que não foi informado
        >>> cofins = COFINSOutr(CST='99', qBCProd=Decimal('100.0000'))
        >>> cofins._xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # neste caso, deve falhar pois vBC ou qBCProd não foram informados
        >>> cofins = COFINSOutr(CST='99')
        >>> cofins._xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'COFINSOutr' requer exclusivamente 'vBC' ou 'qBCProd' (nenhum informado)

        # neste caso, deve falhar pois apenas um ou outro grupo pode ser informado:
        # ou informa-se vBC e pCOFINS ou informa-se qBCProd e vAliqProd
        >>> cofins = COFINSOutr(CST='99', vBC=Decimal('1.00'), pCOFINS=Decimal('1.00'), qBCProd=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> cofins._xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'COFINSOutr' requer exclusivamente 'vBC' ou 'qBCProd' (ambos informados)

        # neste caso as falhara pela ausencia das dependencias:
        # pCOFINS depende de vBC e vAliqProd depende de qBCProd
        >>> cofins = COFINSOutr(CST='99', pCOFINS=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> cofins._xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

    """

    def __init__(self, **kwargs):
        super(COFINSOutr, self).__init__(schema={
                'CST': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.S07_CST_COFINSOUTR]},
                'vBC': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['pCOFINS']},
                'pCOFINS': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['vBC']},
                'qBCProd': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['vAliqProd']},
                'vAliqProd': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['qBCProd']},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):

        if hasattr(self, 'vBC') and hasattr(self, 'qBCProd'):
            raise cerberus.ValidationError("Grupo '%s' requer "
                    "exclusivamente 'vBC' ou 'qBCProd' (ambos informados)" %
                    self.__class__.__name__)

        elif not hasattr(self, 'vBC') and not hasattr(self, 'qBCProd'):
            raise cerberus.ValidationError("Grupo '%s' requer "
                    "exclusivamente 'vBC' ou 'qBCProd' (nenhum informado)" %
                    self.__class__.__name__)

        cofinsoutr = ET.Element(self.__class__.__name__)
        ET.SubElement(cofinsoutr, 'CST').text = self.CST

        if hasattr(self, 'vBC'):
            ET.SubElement(cofinsoutr, 'vBC').text = str(self.vBC)
            ET.SubElement(cofinsoutr, 'pCOFINS').text = \
                    str(self.pCOFINS)

        elif hasattr(self, 'qBCProd'):
            ET.SubElement(cofinsoutr, 'qBCProd').text = \
                    str(self.qBCProd)
            ET.SubElement(cofinsoutr, 'vAliqProd').text = \
                    str(self.vAliqProd)

        return cofinsoutr


class COFINSST(Entidade):
    """Grupo de COFINS substituição tributária (``COFINSST``, grupo ``T01``).

    :param str vBC: *Opcional* Se informado deverá ser também informado o
        parâmetro ``pCOFINS``.

    :param str pCOFINS: *Opcional* Se informado deverá ser também informado o
        parâmetro ``vBC``.

    :param str qBCProd: *Opcional* Se informado deverá ser também informado o
        parâmetro ``vAliqProd``.

    :param str vAliqProd: *Opcional* Se informado deverá ser também informado o
        parâmetro ``qBCProd``.

    Os parâmetros ``vBC`` e ``qBCProd`` são mutuamente exclusivos, e um ou
    outro **devem** ser informados.

    .. sourcecode:: python

        >>> cofins = COFINSST(vBC=Decimal('1.00'), pCOFINS=Decimal('0.0065'))
        >>> ET.tostring(cofins._xml())
        '<COFINSST><vBC>1.00</vBC><pCOFINS>0.0065</pCOFINS></COFINSST>'
        >>> cofins = COFINSST(qBCProd=Decimal('100.0000'), vAliqProd=Decimal('0.6500'))
        >>> ET.tostring(cofins._xml())
        '<COFINSST><qBCProd>100.0000</qBCProd><vAliqProd>0.6500</vAliqProd></COFINSST>'

        # atributo vBC depende de pCOFINS que não foi informado
        >>> cofins = COFINSST(vBC=Decimal('1.00')) # vBC depende de pCOFINS
        >>> cofins._xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # atributo qBCProd depende de vAliqProd que não foi informado
        >>> cofins = COFINSST(qBCProd=Decimal('100.0000'))
        >>> cofins._xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # neste caso, deve falhar pois vBC ou qBCProd não foram informados
        >>> cofins = COFINSST()
        >>> cofins._xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'COFINSST' requer exclusivamente 'vBC' ou 'qBCProd' (nenhum informado)

        # neste caso, deve falhar pois apenas um ou outro grupo pode ser informado:
        # ou informa-se vBC e pCOFINS ou informa-se qBCProd e vAliqProd
        >>> cofins = COFINSST(vBC=Decimal('1.00'), pCOFINS=Decimal('1.00'), qBCProd=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> cofins._xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'COFINSST' requer exclusivamente 'vBC' ou 'qBCProd' (ambos informados)

        # neste caso as falhara pela ausencia das dependencias:
        # pCOFINS depende de vBC e vAliqProd depende de qBCProd
        >>> cofins = COFINSST(pCOFINS=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> cofins._xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

    """

    def __init__(self, **kwargs):
        super(COFINSST, self).__init__(schema={
                'vBC': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['pCOFINS']},
                'pCOFINS': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['vBC']},
                'qBCProd': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['vAliqProd']},
                'vAliqProd': {
                        'type': 'decimal',
                        'required': False,
                        'dependencies': ['qBCProd']},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):

        if hasattr(self, 'vBC') and hasattr(self, 'qBCProd'):
            raise cerberus.ValidationError("Grupo '%s' requer "
                    "exclusivamente 'vBC' ou 'qBCProd' (ambos informados)" %
                    self.__class__.__name__)

        elif not hasattr(self, 'vBC') and not hasattr(self, 'qBCProd'):
            raise cerberus.ValidationError("Grupo '%s' requer "
                    "exclusivamente 'vBC' ou 'qBCProd' (nenhum informado)" %
                    self.__class__.__name__)

        pisst = ET.Element(self.__class__.__name__)

        if hasattr(self, 'vBC'):
            ET.SubElement(pisst, 'vBC').text = str(self.vBC)
            ET.SubElement(pisst, 'pCOFINS').text = str(self.pCOFINS)

        elif hasattr(self, 'qBCProd'):
            ET.SubElement(pisst, 'qBCProd').text = str(self.qBCProd)
            ET.SubElement(pisst, 'vAliqProd').text = \
                    str(self.vAliqProd)

        return pisst


class ISSQN(Entidade):
    """Grupo do ISSQN (``ISSQN``, grupo ``U01``).

    :param Decimal vDeducISSQN:
    :param Decimal vAliq:
    :param str cMunFG: *Opcional*
    :param str cListServ: *Opcional*
    :param str cServTribMun: *Opcional*
    :param str cNatOp:
    :param str indIncFisc:

    .. sourcecode:: python

        >>> issqn = ISSQN(vDeducISSQN=Decimal('10.00'), vAliq=Decimal('7.00'), cNatOp='01', indIncFisc='2')
        >>> ET.tostring(issqn._xml())
        '<ISSQN><vDeducISSQN>10.00</vDeducISSQN><vAliq>7.00</vAliq><cNatOp>01</cNatOp><indIncFisc>2</indIncFisc></ISSQN>'

        >>> issqn = ISSQN(vDeducISSQN=Decimal('10.00'), vAliq=Decimal('7.00'), cNatOp='01', indIncFisc='2', cMunFG='3511102', cListServ='01.01', cServTribMun='01234567890123456789')
        >>> ET.tostring(issqn._xml())
        '<ISSQN><vDeducISSQN>10.00</vDeducISSQN><vAliq>7.00</vAliq><cMunFG>3511102</cMunFG><cListServ>01.01</cListServ><cServTribMun>01234567890123456789</cServTribMun><cNatOp>01</cNatOp><indIncFisc>2</indIncFisc></ISSQN>'

    """

    def __init__(self, **kwargs):
        super(ISSQN, self).__init__(schema={
                'vDeducISSQN': {
                        'type': 'decimal',
                        'required': True},
                'vAliq': {
                        'type': 'decimal',
                        'required': True},
                'cMunFG': {
                        'type': 'string',
                        'required': False,
                        'regex': r'^\d{7}$'},
                'cListServ': {
                        'type': 'string',
                        'required': False,
                        'regex': r'^\d{2}\.\d{2}$'},
                'cServTribMun': {
                        'type': 'string',
                        'required': False,
                        'minlength': 20, 'maxlength': 20},
                'cNatOp': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.U09_CNATOP_ISSQN]},
                'indIncFisc': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.U10_INDINCFISC_ISSQN]},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):

        issqn = ET.Element(self.__class__.__name__)

        ET.SubElement(issqn, 'vDeducISSQN').text = \
                str(self.vDeducISSQN)

        ET.SubElement(issqn, 'vAliq').text = str(self.vAliq)

        if hasattr(self, 'cMunFG'):
            ET.SubElement(issqn, 'cMunFG').text = self.cMunFG

        if hasattr(self, 'cListServ'):
            ET.SubElement(issqn, 'cListServ').text = self.cListServ

        if hasattr(self, 'cServTribMun'):
            ET.SubElement(issqn, 'cServTribMun').text = self.cServTribMun

        ET.SubElement(issqn, 'cNatOp').text = self.cNatOp
        ET.SubElement(issqn, 'indIncFisc').text = self.indIncFisc

        return issqn


class Imposto(Entidade):
    """Grupo de tributos incidentes no produto ou serviço (``imposto``,
    grupo ``M01``).

    :param icms: *Opcional* Deve ser uma instância de uma das classes dos
        grupos de ICMS (:class:`ICMS00`, :class:`ICMS40`, :class:`ICMSSN102`
        ou :class:`ICMSSN900`) se o item for um produto tributado pelo ICMS
        ou ``None`` em caso contrário.

    :param pis: Deve ser uma instância de uma das classes dos grupos de
        PIS (:class:`PISAliq`, :class:`PISQtde`, :class:`PISNT`, :class:`PISSN`
        ou :class:`PISOutr`).

    :param pisst: *Opcional* Instância de :class:`PISST` ou ``None``.

    :param str cofins: Deve ser uma instância de uma dlas classes dos grupos
        de COFINS (:class:`COFINSAliq`, :class:`COFINSQtde`, :class:`COFINSNT`,
        :class:`COFINSSN` ou :class:`COFINSOutr`).

    :param str cofinsst: *Opcional* Instância de :class:`COFINSST` ou ``None``.

    :param str issqn: *Opcional* Uma instância de :class:`ISSQN` se o item for
        um serviço tributado pelo ISSQN ou ``None`` em caso contrário.

    :param Decimal vItem12741: *Opcional* Valor aproximado dos tributos do
        produto ou serviço, conforme a Lei 12.741/12.

    .. sourcecode:: python

        >>> imposto = Imposto(
        ...         vItem12741=Decimal('0.10'),
        ...         icms=ICMS00(Orig='0', CST='00', pICMS=Decimal('18.00')),
        ...         pis=PISSN(CST='49'),
        ...         cofins=COFINSSN(CST='49'))
        >>> ET.tostring(imposto._xml())
        '<imposto><vItem12741>0.10</vItem12741><ICMS><ICMS00><Orig>0</Orig><CST>00</CST><pICMS>18.00</pICMS></ICMS00></ICMS><PIS><PISSN><CST>49</CST></PISSN></PIS><COFINS><COFINSSN><CST>49</CST></COFINSSN></COFINS></imposto>'

        # sem pis
        >>> imposto = Imposto(cofins=COFINSSN(CST='49'))
        >>> imposto._xml()
        Traceback (most recent call last):
         ...
        ValidationError: 'Imposto' (grupo M01 'imposto') atributo 'pis' nao pode ser 'None'

        # sem cofins
        >>> imposto = Imposto(pis=PISSN(CST='49'))
        >>> imposto._xml()
        Traceback (most recent call last):
         ...
        ValidationError: 'Imposto' (grupo M01 'imposto') atributo 'cofins' nao pode ser 'None'

    """

    def __init__(self, icms=None, pis=None, pisst=None,
            cofins=None, cofinsst=None, issqn=None, **kwargs):
        self._icms = icms
        self._pis = pis
        self._pisst = pisst
        self._cofins = cofins
        self._cofinsst = cofinsst
        self._issqn = issqn
        super(Imposto, self).__init__(schema={
                'vItem12741': { # M02
                        'type': 'decimal',
                        'required': False}
            }, **kwargs)


    @property
    def icms(self):
        """Um dos grupos de ICMS (:class:`ICMS00`, :class:`ICMS40`,
        :class:`ICMSSN102` ou :class:`ICMSSN900`) se o item for um produto
        tributado pelo ICMS ou ``None`` em caso contrário.
        """
        return self._icms


    @property
    def pis(self):
        """Um dos grupos de PIS (:class:`PISAliq`, :class:`PISQtde`,
        :class:`PISNT`, :class:`PISSN` ou :class:`PISOutr`).
        """
        return self._pis


    @property
    def pisst(self):
        """O grupo do PIS Substituição Tributária (:class:`PISST`) se for o
        caso, ou ``None``.
        """
        return self._pisst


    @property
    def cofins(self):
        """Um dos grupos de COFINS (:class:`COFINSAliq`, :class:`COFINSQtde`,
        :class:`COFINSNT`, :class:`COFINSSN` ou :class:`COFINSOutr`).
        """
        return self._cofins


    @property
    def cofinsst(self):
        """O grupo do COFINS Substituição Tributária (:class:`COFINSST`) se
        for o caso, ou ``None``.
        """
        return self._cofinsst


    @property
    def issqn(self):
        """O grupo de ISSQN (:class:`ISSQN`) se o item for um serviço
        tributado pelo ISSQN ou ``None`` em caso contrário.
        """
        return self._issqn


    def _construir_elemento_xml(self, *args, **kwargs):

        if self.pis is None:
            raise cerberus.ValidationError("'%s' (grupo M01 'imposto') "
                    "atributo 'pis' nao pode ser 'None'" %
                    self.__class__.__name__)

        if self.cofins is None:
            raise cerberus.ValidationError("'%s' (grupo M01 'imposto') "
                    "atributo 'cofins' nao pode ser 'None'" %
                    self.__class__.__name__)

        imposto = ET.Element('imposto')

        if hasattr(self, 'vItem12741'):
            ET.SubElement(imposto, 'vItem12741').text = \
                    str(self.vItem12741)

        if self.icms is not None:
            icms = ET.SubElement(imposto, 'ICMS')
            icms.append(self.icms._xml())

        pis = ET.SubElement(imposto, 'PIS')
        pis.append(self.pis._xml())

        if self.pisst is not None:
            imposto.append(self.pisst._xml())

        cofins = ET.SubElement(imposto, 'COFINS')
        cofins.append(self.cofins._xml())

        if self.cofinsst is not None:
            imposto.append(self.cofinsst._xml())

        if self.issqn is not None:
            imposto.append(self.issqn._xml())

        return imposto


class DescAcrEntr(Entidade):
    """Grupo de valores de entrada de desconto/acréscimo sobre subtotal
    (``DescAcrEntr``, grupo ``W19``).

    :param Decimal vDescSubtot: Valor de entrada de desconto sobre subtotal.
        Se este argumento for informado, então o argumento ``vAcresSubtot`` não
        deve ser informado.

    :param Decimal vAcresSubtot: Valor de entrada de acréscimo sobre subtotal.
        Se este argumento for informado, então o argumento ``vDescSubtot`` não
        deve ser informado.

    .. sourcecode:: python

        >>> grupo = DescAcrEntr()
        >>> ET.tostring(grupo._xml())
        '<DescAcrEntr />'

        >>> # os atributos são mutamente exclusivos
        >>> grupo = DescAcrEntr(
        ...         vDescSubtot=Decimal('0.01'),
        ...         vAcresSubtot=Decimal('0.02'))
        >>> ET.tostring(grupo._xml())
        Traceback (most recent call last):
         ...
        ValidationError: ...

        >>> grupo = DescAcrEntr(vDescSubtot=Decimal('0.01'))
        >>> ET.tostring(grupo._xml())
        '<DescAcrEntr><vDescSubtot>0.01</vDescSubtot></DescAcrEntr>'

        >>> grupo = DescAcrEntr(vAcresSubtot=Decimal('0.02'))
        >>> ET.tostring(grupo._xml())
        '<DescAcrEntr><vAcresSubtot>0.02</vAcresSubtot></DescAcrEntr>'

    """

    class _Validator(ExtendedValidator):

        def _validate_type_vDescSubtot_W20(self, field, value):
            if 'vAcresSubtot' in self.document:
                self._error(field,
                        u'vDescSubtot (W20) e vAcresSubtot (W21) são mutuamente exclusivos.')

        def _validate_type_vAcresSubtot_W21(self, field, value):
            if 'vDescSubtot' in self.document:
                self._error(field,
                        u'vAcresSubtot (W21) e vDescSubtot (W20) são mutuamente exclusivos.')


    def __init__(self, **kwargs):
        super(DescAcrEntr, self).__init__(schema={
                'vDescSubtot': {
                        'type': 'vDescSubtot_W20',
                        'required': False},
                'vAcresSubtot': {
                        'type': 'vAcresSubtot_W21',
                        'required': False},
            }, validator_class=DescAcrEntr._Validator, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        grupo = ET.Element(self.__class__.__name__)

        if hasattr(self, 'vDescSubtot'):
            ET.SubElement(grupo, 'vDescSubtot').text = \
                    str(self.vDescSubtot)

        if hasattr(self, 'vAcresSubtot'):
            ET.SubElement(grupo, 'vAcresSubtot').text = \
                    str(self.vAcresSubtot)

        return grupo


class MeioPagamento(Entidade):
    """Meio de pagamento (``MP``, grupo ``WA02``).

    :param str cMP:
    :param Decimal vMP:
    :param str cAdmC: *Opcional*

    .. sourcecode:: python

        >>> mp = MeioPagamento(cMP='01', vMP=Decimal('10.00'))
        >>> ET.tostring(mp._xml())
        '<MP><cMP>01</cMP><vMP>10.00</vMP></MP>'

        >>> mp = MeioPagamento(cMP='01', vMP=Decimal('10.00'), cAdmC='999')
        >>> ET.tostring(mp._xml())
        '<MP><cMP>01</cMP><vMP>10.00</vMP><cAdmC>999</cAdmC></MP>'

    """

    def __init__(self, **kwargs):
        super(MeioPagamento, self).__init__(schema={
                'cMP': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in constantes.WA03_CMP_MP]},
                'vMP': {
                        'type': 'decimal',
                        'required': True},
                'cAdmC': {
                        'type': 'string',
                        'required': False,
                        'allowed':
                                [a for a,b,c in constantes.CREDENCIADORAS_CARTAO]},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        mp = ET.Element('MP')
        ET.SubElement(mp, 'cMP').text = self.cMP
        ET.SubElement(mp, 'vMP').text = str(self.vMP)
        if hasattr(self, 'cAdmC'):
            ET.SubElement(mp, 'cAdmC').text = self.cAdmC
        return mp


class InformacoesAdicionais(Entidade):
    """Grupo de informações adicionais (``infAdic``, grupo ``Z01``).

    :param str infCpl: *Opcional*

    .. sourcecode:: python

        >>> grupo = InformacoesAdicionais()
        >>> ET.tostring(grupo._xml())
        '<infAdic />'

        >>> grupo = InformacoesAdicionais(infCpl='Teste')
        >>> ET.tostring(grupo._xml())
        '<infAdic><infCpl>Teste</infCpl></infAdic>'

    """

    def __init__(self, **kwargs):
        super(InformacoesAdicionais, self).__init__(schema={
                'infCpl': {
                        'type': 'string',
                        'required': False,
                        'minlength': 1, 'maxlength': 5000},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        grupo = ET.Element('infAdic')
        if hasattr(self, 'infCpl'):
            ET.SubElement(grupo, 'infCpl').text = self.infCpl
        return grupo


class CFeVenda(Entidade):
    """Representa um CF-e de venda.

    :param Emitente emitente: Identificação do emitente do CF-e.

    :param Destinatario destinatario: *Opcional*. Identificação do destinatário.

    :param LocalEntrega entrega: *Opcional*. Informações do local de entrega.

    :param list detalhamentos: Uma lista de objetos :class:`ProdutoServico` que
        representam os produtos/serviços participantes do CF-e de venda.

    :param DescAcrEntr descontos_acrescimos_subtotal: *Opcional*. Se informado,
        deverá ser um objeto :class:`DescAcrEntr` que contenha o valor de
        desconto ou acréscimo sobre o subtotal.

    :param list pagamentos: Uma lista de objetos :class:`MeioPagamento` que
        descrevem cada um dos meios de pagamentos usados no CF-e de venda.

    :param InformacoesAdicionais informacoes_adicionais: *Opcional*.

    :param str versaoDadosEnt: *Opcional*. String contendo a versão do layout
        do arquivo de dados do aplicativo comercial. Se não informado será
        utilizado o valor da constante ``VERSAO_LAYOUT_ARQUIVO_DADOS_AC`` do
        módulo ``constantes`` do `projeto ``satcomum`` <https://github.com/base4sistemas/satcomum/>`_

    :param str CNPJ:  CNPJ da software house, desenvolvedora do aplicativo
        comercial, contendo apenas os dígitos do número e incluindo zeros não
        significativos, se for o caso (14 dígitos).

    :param str signAC:  Assinatura do aplicativo comercial (344 dígitos).

    :param int numeroCaixa: Número do caixa ao qual o SAT está conectado.
        Normalmente este será o número do caixa de onde parte a solicitação de
        cancelamento. Deverá ser um número inteiro entre ``0`` e ``999``.

    :param Decimal vCFeLei12741: *Opcional*. Se informado deve representar a
        soma total dos valores aproximados dos tributos, em cumprimento à Lei
        nº 12.741/2012.

    Note que não há uma classe específica para representar o elemento ``ide``
    do grupo ``B01``, já que todos os seus atributos são esperados nesta classe.

    .. sourcecode:: python

        >>> cfe = CFeVenda(
        ...         CNPJ='08427847000169',
        ...         signAC=constantes.ASSINATURA_AC_TESTE,
        ...         numeroCaixa=1,
        ...         emitente=Emitente(
        ...                 CNPJ='61099008000141',
        ...                 IE='111111111111',
        ...                 IM='12345',
        ...                 cRegTribISSQN=constantes.C15_SOCIEDADE_PROFISSIONAIS,
        ...                 indRatISSQN=constantes.C16_NAO_RATEADO))
        >>> ET.tostring(cfe._xml())
        '<CFe><infCFe versaoDadosEnt="0.07"><ide><CNPJ>08427847000169</CNPJ><signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC><numeroCaixa>001</numeroCaixa></ide><emit><CNPJ>61099008000141</CNPJ><IE>111111111111</IE><IM>12345</IM><cRegTribISSQN>3</cRegTribISSQN><indRatISSQN>N</indRatISSQN></emit><dest /><total /><pgto /></infCFe></CFe>'

    """

    def __init__(self, emitente=None, destinatario=None, entrega=None,
            detalhamentos=[], descontos_acrescimos_subtotal=None,
            pagamentos=[], informacoes_adicionais=None, **kwargs):

        self._emitente = emitente
        self._destinatario = destinatario
        self._entrega = entrega
        self._detalhamentos = detalhamentos
        self._descontos_acrescimos_subtotal = descontos_acrescimos_subtotal
        self._pagamentos = pagamentos
        self._informacoes_adicionais = informacoes_adicionais

        super(CFeVenda, self).__init__(
                versaoDadosEnt=constantes.VERSAO_LAYOUT_ARQUIVO_DADOS_AC,
                schema={
                        'versaoDadosEnt': {
                                'type': 'string',
                                'required': True,
                                'regex': r'^\d{1}\.\d{2}$'},
                        'CNPJ': {
                                'type': 'cnpj',
                                'required': True},
                        'signAC': {
                                'type': 'assinatura_ac',
                                'required': True},
                        'numeroCaixa': {
                                'type': 'integer',
                                'required': True,
                                'min': 0, 'max': 999},
                        'vCFeLei12741': {
                                'type': 'decimal',
                                'required': False},
                    }, **kwargs)


    @property
    def emitente(self):
        """O :class:`Emitente` do CF-e."""
        return self._emitente


    @property
    def destinatario(self):
        """O :class:`Destinatario` do CF-e ou ``None``."""
        return self._destinatario


    @property
    def entrega(self):
        """O Local de entrega (:class:`LocalEntrega`) ou ``None``."""
        return self._entrega


    @property
    def detalhamentos(self):
        """Lista de objetos :class:`Detalhamento`, descrevendo os produtos e
        serviços do CF-e.
        """
        return self._detalhamentos


    @property
    def descontos_acrescimos_subtotal(self):
        """Os descontos e acréscimos no subtotal do CF-e (:class:`DescAcrEntr`)
        ou ``None``.
        """
        return self._descontos_acrescimos_subtotal


    @property
    def pagamentos(self):
        """Lista de objetos :class`MeioPagamento`, descrevendo os meios de
        pagamento empregados na quitação do CF-e.
        """
        return self._pagamentos


    @property
    def informacoes_adicionais(self):
        """Informações adicionais do CF-e (:class:`InformacoesAdicionais`)
        ou ``None``.
        """
        return self._informacoes_adicionais


    def _xml(self, *args, **kwargs):
        Entidade._erros.clear()
        return super(CFeVenda, self)._xml(*args, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):

        cfe = ET.Element('CFe')
        infCFe = ET.SubElement(cfe, 'infCFe')
        infCFe.attrib['versaoDadosEnt'] = self.versaoDadosEnt

        ide = ET.SubElement(infCFe, 'ide')
        ET.SubElement(ide, 'CNPJ').text = self.CNPJ
        ET.SubElement(ide, 'signAC').text = self.signAC
        ET.SubElement(ide, 'numeroCaixa').text = \
                '{:03d}'.format(self.numeroCaixa)

        infCFe.append(self.emitente._xml())

        dest = self.destinatario or Destinatario()
        infCFe.append(dest._xml())

        if self.entrega is not None:
            infCFe.append(self.entrega._xml())

        for n, det in enumerate(self.detalhamentos):
            infCFe.append(det._xml(nItem=n+1))

        total = ET.SubElement(infCFe, 'total')

        if hasattr(self, 'vCFeLei12741'):
            ET.SubElement(total, 'vCFeLei12741').text = str(self.vCFeLei12741)

        if self.descontos_acrescimos_subtotal is not None:
            total.append(self.descontos_acrescimos_subtotal._xml())

        pgto = ET.SubElement(infCFe, 'pgto')
        for pg in self.pagamentos:
            pgto.append(pg._xml())

        if self.informacoes_adicionais is not None:
            infCFe.append(self.informacoes_adicionais._xml())

        return cfe


class CFeCancelamento(Entidade):
    """Representa um CF-e de cancelamento.

    :param Destinatario destinatario: *Opcional*. Uma instância de
        :class:`Destinatario` contendo apenas os dados exigidos para a operação
        de cancelamento (ie. ``CPF`` ou ``CNPJ`` do destinatário).

    :param str chCanc: Chave de acesso do CF-e a ser cancelado. Deve ser
        precedido do literal ``CFe`` seguido dos quarenta e quatro dígitos
        que compõem a chave de acesso.

    :param str CNPJ: CNPJ da software house, desenvolvedora do aplicativo
        comercial, contendo apenas os dígitos do número e incluindo zeros não
        significativos, se for o caso (14 dígitos).

    :param str signAC: Assinatura do aplicativo comercial (344 dígitos).

    :param int numeroCaixa: Número do caixa ao qual o SAT está conectado.
        Normalmente este será o número do caixa de onde parte a solicitação de
        cancelamento. Deverá ser um número inteiro entre ``0`` e ``999``.

    .. sourcecode:: python

        >>> cfecanc = CFeCancelamento(
        ...         chCanc='CFe01234567890123456789012345678901234567890123',
        ...         CNPJ='08427847000169',
        ...         signAC=constantes.ASSINATURA_AC_TESTE,
        ...         numeroCaixa=1)
        >>> ET.tostring(cfecanc._xml())
        '<CFeCanc><infCFe chCanc="CFe01234567890123456789012345678901234567890123"><ide><CNPJ>08427847000169</CNPJ><signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC><numeroCaixa>001</numeroCaixa></ide><emit /><dest /><total /></infCFe></CFeCanc>'

    """

    def __init__(self, destinatario=None, **kwargs):
        self._destinatario = destinatario
        super(CFeCancelamento, self).__init__(schema={
                'chCanc': {
                        'type': 'string',
                        'required': True,
                        'regex': r'^CFe\d{44}$'},
                'CNPJ': {
                        'type': 'cnpj',
                        'required': True},
                'signAC': {
                        'type': 'assinatura_ac',
                        'required': True},
                'numeroCaixa': {
                        'type': 'integer',
                        'required': True,
                        'min': 0, 'max': 999},
            }, **kwargs)


    @property
    def destinatario(self):
        """O :class:`Destinatario` ou ``None``."""
        return self._destinatario


    def _xml(self, *args, **kwargs):
        Entidade._erros.clear()
        return super(CFeCancelamento, self)._xml(*args, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):

        cfecanc = ET.Element('CFeCanc')

        infCFe = ET.SubElement(cfecanc, 'infCFe')
        infCFe.attrib['chCanc'] = self.chCanc

        ide = ET.SubElement(infCFe, 'ide')
        ET.SubElement(ide, 'CNPJ').text = self.CNPJ
        ET.SubElement(ide, 'signAC').text = self.signAC
        ET.SubElement(ide, 'numeroCaixa').text = \
                '{:03d}'.format(self.numeroCaixa)

        ET.SubElement(infCFe, 'emit')

        dest = self.destinatario or Destinatario()
        infCFe.append(dest._xml(cancelamento=True))

        ET.SubElement(infCFe, 'total')

        return cfecanc
