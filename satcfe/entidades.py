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

"""
    A documentação oficial para os atributos que as classes de entidades
    referenciam, estão na Especificação Técnica de Requisitos (ER) do SAT,
    Item 4.2.2, Layout do Arquivo de Venda (CF-e-SAT) que pode ser obtido
    no `site oficial <http://www.fazenda.sp.gov.br/sat/>`_.

    Nem todas as classes que representam os grupos de informações do CF-e
    possuem o mesmo nome usado no item 4.2.2 do layout do arquivo de venda ou
    no item 4.2.3 do layout do arquivo de cancelamento. **Entretanto, todos os
    elementos e atributos, possuem exatamente o mesmo nome usado na ER SAT**.

    A tabela abaixo, relaciona as classes de entidades com os grupos que elas
    representam:

    +--------------------------------+------------------+------+
    | Classe de Entidade             | Grupo            | ID   |
    +================================+==================+======+
    | :class:`CFeVenda`              | ``infCFe``       | A01  |
    +--------------------------------+------------------+------+
    | :class:`Emitente`              | ``emit``         | C01  |
    +--------------------------------+------------------+------+
    | :class:`Destinatario`          | ``dest``         | E01  |
    +--------------------------------+------------------+------+
    | :class:`LocalEntrega`          | ``entrega``      | G01  |
    +--------------------------------+------------------+------+
    | :class:`Detalhamento`          | ``det``          | H01  |
    +--------------------------------+------------------+------+
    | :class:`ProdutoServico`        | ``prod``         | I01  |
    +--------------------------------+------------------+------+
    | :class:`ObsFiscoDet`           | ``obsFiscoDet``  | I17  |
    +--------------------------------+------------------+------+
    | :class:`ICMS00`                | ``ICMS00``       | N02  |
    +--------------------------------+------------------+------+
    | :class:`ICMS40`                | ``ICMS40``       | N03  |
    +--------------------------------+------------------+------+
    | :class:`ICMSSN102`             | ``ICMSSN102``    | N04  |
    +--------------------------------+------------------+------+
    | :class:`ICMSSN900`             | ``ICMSSN900``    | N05  |
    +--------------------------------+------------------+------+
    | :class:`PISAliq`               | ``PISAliq``      | Q02  |
    +--------------------------------+------------------+------+
    | :class:`PISQtde`               | ``PISQtde``      | Q03  |
    +--------------------------------+------------------+------+
    | :class:`PISNT`                 | ``PISNT``        | Q04  |
    +--------------------------------+------------------+------+
    | :class:`PISSN`                 | ``PISSN``        | Q05  |
    +--------------------------------+------------------+------+
    | :class:`PISOutr`               | ``PISOutr``      | Q06  |
    +--------------------------------+------------------+------+
    | :class:`PISST`                 | ``PISST``        | R01  |
    +--------------------------------+------------------+------+
    | :class:`COFINSAliq`            | ``COFINSAliq``   | S02  |
    +--------------------------------+------------------+------+
    | :class:`COFINSQtde`            | ``COFINSQtde``   | S03  |
    +--------------------------------+------------------+------+
    | :class:`COFINSNT`              | ``COFINSNT``     | S04  |
    +--------------------------------+------------------+------+
    | :class:`COFINSSN`              | ``COFINSSN``     | S05  |
    +--------------------------------+------------------+------+
    | :class:`COFINSOutr`            | ``COFINSOutr``   | S06  |
    +--------------------------------+------------------+------+
    | :class:`COFINSST`              | ``COFINSST``     | T01  |
    +--------------------------------+------------------+------+
    | :class:`ISSQN`                 | ``ISSQN``        | U01  |
    +--------------------------------+------------------+------+
    | :class:`Imposto`               | ``imposto``      | M01  |
    +--------------------------------+------------------+------+
    | :class:`DescAcrEntr`           | ``DescAcrEntr``  | W19  |
    +--------------------------------+------------------+------+
    | :class:`MeioPagamento`         | ``MP``           | WA02 |
    +--------------------------------+------------------+------+
    | :class:`InformacoesAdicionais` | ``infAdic``      | Z01  |
    +--------------------------------+------------------+------+

    Hierarquia dos elementos XML do layout do CF-e, Item 4.2.2 da ER.


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
                  |    |         > ICMS 40, 41, 50, 60
                  |    |
                  |    +--- ICMSSN102 (N04, 0..1)
                  |    |         > cRegTrib = 1, Simples Nacional
                  |    |         > CSOSN 102, 300, 500
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
             |
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


class Entity(object):
    """
    Classe base para todas as classes que representem as entidades da
    implementação do SAT-CF-e. Aqui, chamaremos de "entidade" as classes que
    representem os grupos de dados que são usados para formar o XML da venda
    e/ou do cancelamento.

    Basicamente, as subclasses precisam sobre-escrever a implementação do
    método :meth:`_build_xml_element`, definir o :attr:`_schema` de validação e,
    quando necessário, implementar uma especialização do validador *Cerberus*
    no atributo :attr:`_validator_class`.
    """

    _schema = {}

    _validator_class = ExtendedValidator


    def __init__(self, **kwargs):
        super(Entity, self).__init__()
        self._validator = self._validator_class(self._schema)
        self._validator.allow_unknown = True
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def errors(self):
        return self._validator.errors


    def validate(self):
        if not self._validator.validate(self.__dict__):
            raise cerberus.ValidationError('Entidade "%s" possui '
                    'atributos invalidos.' % self.__class__.__name__)


    def xml(self, *args, **kwargs):
        self.validate()
        return self._build_xml_element(*args, **kwargs)


    def _build_xml_element(self, *args, **kwargs):
        raise NotImplementedError()


class Emitente(Entity):
    """
    Grupo de identificação do emitente do CF-e.
    Representa o grupo C01 ``emit``.

    .. sourcecode:: python

        >>> emit = Emitente(CNPJ='08427847000169', IE='111222333444', indRatISSQN='S')
        >>> ET.tostring(emit.xml())
        '<emit><CNPJ>08427847000169</CNPJ><IE>111222333444</IE><indRatISSQN>S</indRatISSQN></emit>'

        >>> emit = Emitente(
        ...         CNPJ='08427847000169',
        ...         IE='111222333444',
        ...         IM='123456789012345',
        ...         cRegTribISSQN='1',
        ...         indRatISSQN='S')
        >>> ET.tostring(emit.xml())
        '<emit><CNPJ>08427847000169</CNPJ><IE>111222333444</IE><IM>123456789012345</IM><cRegTribISSQN>1</cRegTribISSQN><indRatISSQN>S</indRatISSQN></emit>'

    """

    _schema = {
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
        }


    def _build_xml_element(self, *args, **kwargs):

        emit = ET.Element('emit')
        ET.SubElement(emit, 'CNPJ').text = self.CNPJ
        ET.SubElement(emit, 'IE').text = self.IE

        if hasattr(self, 'IM'):
            ET.SubElement(emit, 'IM').text = self.IM

        if hasattr(self, 'cRegTribISSQN'):
            ET.SubElement(emit, 'cRegTribISSQN').text = self.cRegTribISSQN

        ET.SubElement(emit, 'indRatISSQN').text = self.indRatISSQN

        return emit


class Destinatario(Entity):
    """
    Identificação do Destinatário do CF-e, item "E" da ER, grupo ``E01``,
    ``dest``.

    .. sourcecode:: python

        >>> dest = Destinatario()
        >>> ET.tostring(dest.xml(), encoding='utf-8')
        '<dest />'
        >>> dest = Destinatario(CNPJ='08427847000169')
        >>> ET.tostring(dest.xml(), encoding='utf-8')
        '<dest><CNPJ>08427847000169</CNPJ></dest>'
        >>> dest = Destinatario(CPF='11122233396', xNome=u'Fulano Beltrano')
        >>> ET.tostring(dest.xml(), encoding='utf-8')
        '<dest><CPF>11122233396</CPF><xNome>Fulano Beltrano</xNome></dest>'
        >>> dest = Destinatario(CPF='11122233396', CNPJ='08427847000169')
        >>> dest.xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

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

    _schema = {
            'CNPJ': {'type': 'CNPJ_E02'}, # E02
            'CPF': {'type': 'CPF_E03'}, # E03
            'xNome': { # E04
                    'type': 'string',
                    'required': False,
                    'minlength': 2, 'maxlength': 60}
        }

    _validator_class = _Validator


    def _build_xml_element(self, *args, **kwargs):

        is_cancelamento = kwargs.pop('cancelamento', False)

        dest = ET.Element('dest')

        if hasattr(self, 'CNPJ'):
            ET.SubElement(dest, 'CNPJ').text = self.CNPJ

        if hasattr(self, 'CPF'):
            ET.SubElement(dest, 'CPF').text = self.CPF

        if hasattr(self, 'xNome') and not is_cancelamento:
            ET.SubElement(dest, 'xNome').text = self.xNome

        return dest


class LocalEntrega(Entity):
    """
    Identificação do Local de Entrega, item "G" da ER, grupo ``G01``,
    ``entrega``.

    .. sourcecode:: python

        >>> entrega = LocalEntrega()
        >>> ET.tostring(entrega.xml(), encoding='utf-8')
        Traceback (most recent call last):
         ...
        ValidationError: ...
        >>> entrega.xLgr = 'Rua Armando Gulim'
        >>> entrega.nro = '65'
        >>> entrega.xBairro = 'Parque Gloria III'
        >>> entrega.xMun = 'Catanduva'
        >>> entrega.UF = 'SP'
        >>> ET.tostring(entrega.xml(), encoding='utf-8')
        '<entrega><xLgr>Rua Armando Gulim</xLgr><nro>65</nro><xBairro>Parque Gloria III</xBairro><xMun>Catanduva</xMun><UF>SP</UF></entrega>'
    """

    class _Validator(ExtendedValidator):
        def _validate_type_UF_G07(self, field, value):
            if not br.is_uf(value):
                self._error(field, u'UF (G07) do Local de Entrega, '
                        u'não é válido: "%s"' % value)

    _schema = {
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
        }

    _validator_class = _Validator


    def _build_xml_element(self, *args, **kwargs):

        entrega = ET.Element('entrega')
        ET.SubElement(entrega, 'xLgr').text = self.xLgr
        ET.SubElement(entrega, 'nro').text = self.nro

        if hasattr(self, 'xCpl'):
            ET.SubElement(entrega, 'xCpl').text = self.xCpl

        ET.SubElement(entrega, 'xBairro').text = self.xBairro
        ET.SubElement(entrega, 'xMun').text = self.xMun
        ET.SubElement(entrega, 'UF').text = self.UF

        return entrega


class Detalhamento(Entity):
    """
    Grupo de detalhamento do produto ou serviço do CF-e-SAT.

    Note que, neste detalhamento, o atributo XML ``nItem`` não é determinado
    aqui mas em :class:`CFeVenda`, que mantém uma lista dos detalhamentos, de
    modo que o número do item será atribuído automaticamente, conforme a sua
    posição na lista.

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
        >>> ET.tostring(det.xml(nItem=1))
        '<det nItem="1"><prod><cProd>123456</cProd><xProd>BORRACHA STAEDTLER</xProd><CFOP>5102</CFOP><uCom>UN</uCom><qCom>1.0000</qCom><vUnCom>5.75</vUnCom><indRegra>A</indRegra></prod><imposto><ICMSSN102><Orig>2</Orig><CSOSN>500</CSOSN></ICMSSN102><PISSN><CST>49</CST></PISSN><COFINSSN><CST>49</CST></COFINSSN></imposto><infAdProd>Teste</infAdProd></det>'

    """

    produto = None
    """
    Aponta para um produto ou serviço, uma instância de :class:`ProdutoServico`
    ao qual este detalhamento se refere.
    """

    imposto = None
    """
    Aponta para o grupo de tributos incidentes no produto ou serviço ao qual
    este detalhamento se refere, como uma instância de :class:`Imposto`.
    """

    _schema = {
            'infAdProd': {
                    'type': 'string',
                    'required': False,
                    'minlength': 1, 'maxlength': 500},
        }


    def _build_xml_element(self, *args, **kwargs):

        det = ET.Element('det')
        det.attrib['nItem'] = str(kwargs.pop('nItem'))

        det.append(self.produto.xml())
        det.append(self.imposto.xml())

        if hasattr(self, 'infAdProd'):
            ET.SubElement(det, 'infAdProd').text = self.infAdProd

        return det


class ProdutoServico(Entity):
    """
    Grupo do produto ou serviço do CF-e-SAT.
    Representa o grupo I01 ``prod``.

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
        >>> ET.tostring(prod.xml())
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
        >>> ET.tostring(prod.xml())
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
        >>> ET.tostring(prod.xml())
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
        >>> prod.xml()
        Traceback (most recent call last):
         ...
        ValidationError: 'ProdutoServico' (grupo H01 'prod') atributos 'vDesc' e 'vOutro' sao mutuamente exclusivos

    """

    observacoes_fisco = []
    """
    Cada produto, pode opcionalmente, conter uma lista de campos de uso livre
    do fico, cujos campos e valores são representados por instâncias da
    classe :class:`ObsFiscoDet`.
    """

    _schema = {
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
        }


    def _build_xml_element(self, *args, **kwargs):

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
        ET.SubElement(prod, 'qCom').text = '{:n}'.format(self.qCom)
        ET.SubElement(prod, 'vUnCom').text = '{:n}'.format(self.vUnCom)
        ET.SubElement(prod, 'indRegra').text = self.indRegra

        if hasattr(self, 'vDesc'):
            ET.SubElement(prod, 'vDesc').text = '{:n}'.format(self.vDesc)

        if hasattr(self, 'vOutro'):
            ET.SubElement(prod, 'vOutro').text = '{:n}'.format(self.vOutro)

        if self.observacoes_fisco:
            for obs in self.observacoes_fisco:
                prod.append(obs.xml())

        return prod


class ObsFiscoDet(Entity):
    """
    Grupo do campo de uso livre do Fisco.
    Representa o elemento I17 ``obsFiscoDet``.

    .. sourcecode:: python

        >>> obs = ObsFiscoDet(xCampoDet='Cod. Produto ANP', xTextoDet='320101001')
        >>> ET.tostring(obs.xml())
        '<obsFiscoDet xCampoDet="Cod. Produto ANP"><xTextoDet>320101001</xTextoDet></obsFiscoDet>'

    """

    _schema = {
            'xCampoDet': {
                    'type': 'string',
                    'required': True,
                    'minlength': 1, 'maxlength': 20},
            'xTextoDet': {
                    'type': 'string',
                    'required': True,
                    'minlength': 1, 'maxlength': 60},
        }


    def _build_xml_element(self, *args, **kwargs):
        obs = ET.Element('obsFiscoDet')
        obs.attrib['xCampoDet'] = self.xCampoDet
        ET.SubElement(obs, 'xTextoDet').text = self.xTextoDet
        return obs


class ICMS00(Entity):
    """
    Grupo de tributação do ICMS 00, 20 e 90. Representa o grupo N02 ``ICMS00``.

    >>> icms = ICMS00(Orig='0', CST='00', pICMS=Decimal('18.00'))
    >>> ET.tostring(icms.xml())
    '<ICMS00><Orig>0</Orig><CST>00</CST><pICMS>18.00</pICMS></ICMS00>'
    """

    _schema = {
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
        }


    def _build_xml_element(self, *args, **kwargs):
        icms00 = ET.Element(self.__class__.__name__)
        ET.SubElement(icms00, 'Orig').text = self.Orig
        ET.SubElement(icms00, 'CST').text = self.CST
        ET.SubElement(icms00, 'pICMS').text = '{:n}'.format(self.pICMS)
        return icms00


class ICMS40(Entity):
    """
    Grupo de tributação do ICMS 40, 41, 50 e 60.
    Representa o grupo N03 ``ICMS40``.

    >>> icms = ICMS40(Orig='0', CST='60')
    >>> ET.tostring(icms.xml())
    '<ICMS40><Orig>0</Orig><CST>60</CST></ICMS40>'
    """

    _schema = {
            'Orig': { # N06
                    'type': 'string',
                    'required': True,
                    'allowed': [v for v,s in constantes.N06_ORIG]},
            'CST': { # N07
                    'type': 'string',
                    'required': True,
                    'allowed': [v for v,s in constantes.N07_CST_ICMS40]},
        }


    def _build_xml_element(self, *args, **kwargs):
        icms40 = ET.Element('ICMS40')
        ET.SubElement(icms40, 'Orig').text = self.Orig
        ET.SubElement(icms40, 'CST').text = self.CST
        return icms40


class ICMSSN102(Entity):
    """
    Grupo de tributação do ICMS Simples Nacional, CSOSN 102, 300 e 500.
    Representa o grupo N04 ``ICMSSN102``.

    >>> icms = ICMSSN102(Orig='0', CSOSN='500')
    >>> ET.tostring(icms.xml())
    '<ICMSSN102><Orig>0</Orig><CSOSN>500</CSOSN></ICMSSN102>'
    """

    _schema = {
            'Orig': { # N06
                    'type': 'string',
                    'required': True,
                    'allowed': [v for v,s in constantes.N06_ORIG]},
            'CSOSN': { # N10
                    'type': 'string',
                    'required': True,
                    'allowed': [v for v,s in constantes.N10_CSOSN_ICMSSN102]},
        }


    def _build_xml_element(self, *args, **kwargs):
        icmssn102 = ET.Element('ICMSSN102')
        ET.SubElement(icmssn102, 'Orig').text = self.Orig
        ET.SubElement(icmssn102, 'CSOSN').text = self.CSOSN
        return icmssn102


class ICMSSN900(Entity):
    """
    Grupo de tributação do ICMS Simples Nacional, CSOSN 900.
    Representa o grupo N05 ``ICMSSN900``.

    >>> icms = ICMSSN900(Orig='0', CSOSN='900', pICMS=Decimal('18.00'))
    >>> ET.tostring(icms.xml())
    '<ICMSSN900><Orig>0</Orig><CSOSN>900</CSOSN><pICMS>18.00</pICMS></ICMSSN900>'
    """

    _schema = {
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
        }

    def _build_xml_element(self, *args, **kwargs):
        icmssn900 = ET.Element('ICMSSN900')
        ET.SubElement(icmssn900, 'Orig').text = self.Orig
        ET.SubElement(icmssn900, 'CSOSN').text = self.CSOSN
        ET.SubElement(icmssn900, 'pICMS').text = '{:n}'.format(self.pICMS)
        return icmssn900


class PISAliq(Entity):
    """
    Grupo de PIS tributado pela alíquota, CST 01, 02 ou 05.
    Representa o grupo Q02 ``PISAliq``.

    >>> pis = PISAliq(CST='01', vBC=Decimal('1.00'), pPIS=Decimal('0.0065'))
    >>> ET.tostring(pis.xml())
    '<PISAliq><CST>01</CST><vBC>1.00</vBC><pPIS>0.0065</pPIS></PISAliq>'
    """

    _schema = {
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
        }


    def _build_xml_element(self, *args, **kwargs):
        pisaliq = ET.Element('PISAliq')
        ET.SubElement(pisaliq, 'CST').text = self.CST
        ET.SubElement(pisaliq, 'vBC').text = '{:n}'.format(self.vBC)
        ET.SubElement(pisaliq, 'pPIS').text = '{:n}'.format(self.pPIS)
        return pisaliq


class PISQtde(Entity):
    """
    Grupo de PIS tributado por quantidade, CST 03.
    Representa o grupo Q03 ``PISQtde``.

    >>> pis = PISQtde(CST='03', qBCProd=Decimal('100.0000'), vAliqProd=Decimal('0.6500'))
    >>> ET.tostring(pis.xml())
    '<PISQtde><CST>03</CST><qBCProd>100.0000</qBCProd><vAliqProd>0.6500</vAliqProd></PISQtde>'
    """

    _schema = {
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
        }


    def _build_xml_element(self, *args, **kwargs):
        pisqtde = ET.Element('PISQtde')
        ET.SubElement(pisqtde, 'CST').text = self.CST
        ET.SubElement(pisqtde, 'qBCProd').text = '{:n}'.format(self.qBCProd)
        ET.SubElement(pisqtde, 'vAliqProd').text = '{:n}'.format(self.vAliqProd)
        return pisqtde


class PISNT(Entity):
    """
    Grupo de PIS não tributado, CST 04, 06, 07 08 ou 09.
    Representa o grupo Q04 ``PISNT``.

    >>> pis = PISNT(CST='04')
    >>> ET.tostring(pis.xml())
    '<PISNT><CST>04</CST></PISNT>'
    """

    _schema = {
            'CST': {
                    'type': 'string',
                    'required': True,
                    'allowed': [v for v,s in constantes.Q07_CST_PISNT]},
        }


    def _build_xml_element(self, *args, **kwargs):
        pisnt = ET.Element('PISNT')
        ET.SubElement(pisnt, 'CST').text = self.CST
        return pisnt


class PISSN(Entity):
    """
    Grupo de PIS para contribuíntes do Simples Nacional, CST 49.
    Representa o grupo Q05 ``PISSN``.

    >>> pis = PISSN(CST='49')
    >>> ET.tostring(pis.xml())
    '<PISSN><CST>49</CST></PISSN>'
    """

    _schema = {
            'CST': {
                    'type': 'string',
                    'required': True,
                    'allowed': [v for v,s in constantes.Q07_CST_PISSN]},
        }


    def _build_xml_element(self, *args, **kwargs):
        pissn = ET.Element('PISSN')
        ET.SubElement(pissn, 'CST').text = self.CST
        return pissn


class PISOutr(Entity):
    """
    Grupo de PIS para outras operações, CST 99.
    Representa o grupo Q06 ``PISOutr``.

    .. sourcecode:: python

        >>> pis = PISOutr(CST='99', vBC=Decimal('1.00'), pPIS=Decimal('0.0065'))
        >>> ET.tostring(pis.xml())
        '<PISOutr><CST>99</CST><vBC>1.00</vBC><pPIS>0.0065</pPIS></PISOutr>'
        >>> pis = PISOutr(CST='99', qBCProd=Decimal('100.0000'), vAliqProd=Decimal('0.6500'))
        >>> ET.tostring(pis.xml())
        '<PISOutr><CST>99</CST><qBCProd>100.0000</qBCProd><vAliqProd>0.6500</vAliqProd></PISOutr>'

        # atributo vBC depende de pPIS que não foi informado
        >>> pis = PISOutr(CST='99', vBC=Decimal('1.00')) # vBC depende de pPIS
        >>> pis.xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # atributo qBCProd depende de vAliqProd que não foi informado
        >>> pis = PISOutr(CST='99', qBCProd=Decimal('100.0000'))
        >>> pis.xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # neste caso, deve falhar pois vBC ou qBCProd não foram informados
        >>> pis = PISOutr(CST='99')
        >>> pis.xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'PISOutr' requer exclusivamente 'vBC' ou 'qBCProd' (nenhum informado)

        # neste caso, deve falhar pois apenas um ou outro grupo pode ser informado:
        # ou informa-se vBC e pPIS ou informa-se qBCProd e vAliqProd
        >>> pis = PISOutr(CST='99', vBC=Decimal('1.00'), pPIS=Decimal('1.00'), qBCProd=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> pis.xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'PISOutr' requer exclusivamente 'vBC' ou 'qBCProd' (ambos informados)

        # neste caso as falhara pela ausencia das dependencias:
        # pPIS depende de vBC e vAliqProd depende de qBCProd
        >>> pis = PISOutr(CST='99', pPIS=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> pis.xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

    """

    _schema = {
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
        }


    def _build_xml_element(self, *args, **kwargs):

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
            ET.SubElement(pisoutr, 'vBC').text = '{:n}'.format(self.vBC)
            ET.SubElement(pisoutr, 'pPIS').text = '{:n}'.format(self.pPIS)

        elif hasattr(self, 'qBCProd'):
            ET.SubElement(pisoutr, 'qBCProd').text = '{:n}'.format(self.qBCProd)
            ET.SubElement(pisoutr, 'vAliqProd').text = \
                    '{:n}'.format(self.vAliqProd)

        return pisoutr


class PISST(Entity):
    """
    Grupo de PIS substituição tributária.
    Representa o grupo R01 ``PISST``.

    .. sourcecode:: python

        >>> pis = PISST(vBC=Decimal('1.00'), pPIS=Decimal('0.0065'))
        >>> ET.tostring(pis.xml())
        '<PISST><vBC>1.00</vBC><pPIS>0.0065</pPIS></PISST>'
        >>> pis = PISST(qBCProd=Decimal('100.0000'), vAliqProd=Decimal('0.6500'))
        >>> ET.tostring(pis.xml())
        '<PISST><qBCProd>100.0000</qBCProd><vAliqProd>0.6500</vAliqProd></PISST>'

        # atributo vBC depende de pPIS que não foi informado
        >>> pis = PISST(vBC=Decimal('1.00')) # vBC depende de pPIS
        >>> pis.xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # atributo qBCProd depende de vAliqProd que não foi informado
        >>> pis = PISST(qBCProd=Decimal('100.0000'))
        >>> pis.xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # neste caso, deve falhar pois vBC ou qBCProd não foram informados
        >>> pis = PISST()
        >>> pis.xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'PISST' requer exclusivamente 'vBC' ou 'qBCProd' (nenhum informado)

        # neste caso, deve falhar pois apenas um ou outro grupo pode ser informado:
        # ou informa-se vBC e pPIS ou informa-se qBCProd e vAliqProd
        >>> pis = PISST(vBC=Decimal('1.00'), pPIS=Decimal('1.00'), qBCProd=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> pis.xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'PISST' requer exclusivamente 'vBC' ou 'qBCProd' (ambos informados)

        # neste caso as falhara pela ausencia das dependencias:
        # pPIS depende de vBC e vAliqProd depende de qBCProd
        >>> pis = PISST(pPIS=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> pis.xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

    """

    _schema = {
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
        }


    def _build_xml_element(self, *args, **kwargs):

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
            ET.SubElement(pisst, 'vBC').text = '{:n}'.format(self.vBC)
            ET.SubElement(pisst, 'pPIS').text = '{:n}'.format(self.pPIS)

        elif hasattr(self, 'qBCProd'):
            ET.SubElement(pisst, 'qBCProd').text = '{:n}'.format(self.qBCProd)
            ET.SubElement(pisst, 'vAliqProd').text = \
                    '{:n}'.format(self.vAliqProd)

        return pisst


class COFINSAliq(Entity):
    """
    Grupo de COFINS tributado pela alíquota, CST 01, 02 ou 05.
    Representa o grupo S02 ``COFINSAliq``.

    >>> cofins = COFINSAliq(CST='01', vBC=Decimal('1.00'), pCOFINS=Decimal('0.0065'))
    >>> ET.tostring(cofins.xml())
    '<COFINSAliq><CST>01</CST><vBC>1.00</vBC><pCOFINS>0.0065</pCOFINS></COFINSAliq>'
    """

    _schema = {
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
        }


    def _build_xml_element(self, *args, **kwargs):
        cofinsaliq = ET.Element(self.__class__.__name__)
        ET.SubElement(cofinsaliq, 'CST').text = self.CST
        ET.SubElement(cofinsaliq, 'vBC').text = '{:n}'.format(self.vBC)
        ET.SubElement(cofinsaliq, 'pCOFINS').text = '{:n}'.format(self.pCOFINS)
        return cofinsaliq


class COFINSQtde(Entity):
    """
    Grupo de COFINS tributado por quantidade, CST 03.
    Representa o grupo S03 ``COFINSQtde``.

    >>> cofins = COFINSQtde(CST='03', qBCProd=Decimal('100.0000'), vAliqProd=Decimal('0.6500'))
    >>> ET.tostring(cofins.xml())
    '<COFINSQtde><CST>03</CST><qBCProd>100.0000</qBCProd><vAliqProd>0.6500</vAliqProd></COFINSQtde>'
    """

    _schema = {
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
        }


    def _build_xml_element(self, *args, **kwargs):
        cofinsqtde = ET.Element(self.__class__.__name__)
        ET.SubElement(cofinsqtde, 'CST').text = self.CST
        ET.SubElement(cofinsqtde, 'qBCProd').text = '{:n}'.format(self.qBCProd)
        ET.SubElement(cofinsqtde, 'vAliqProd').text = \
                '{:n}'.format(self.vAliqProd)
        return cofinsqtde


class COFINSNT(Entity):
    """
    Grupo de COFINS não tributado, CST 04, 06, 07 08 ou 09.
    Representa o grupo S04 ``COFINSNT``.

    >>> cofins = COFINSNT(CST='04')
    >>> ET.tostring(cofins.xml())
    '<COFINSNT><CST>04</CST></COFINSNT>'
    """

    _schema = {
            'CST': {
                    'type': 'string',
                    'required': True,
                    'allowed': [v for v,s in constantes.S07_CST_COFINSNT]},
        }


    def _build_xml_element(self, *args, **kwargs):
        cofinsnt = ET.Element(self.__class__.__name__)
        ET.SubElement(cofinsnt, 'CST').text = self.CST
        return cofinsnt


class COFINSSN(Entity):
    """
    Grupo de COFINS para contribuíntes do Simples Nacional, CST 49.
    Representa o grupo S05 ``COFINSSN``.

    >>> cofins = COFINSSN(CST='49')
    >>> ET.tostring(cofins.xml())
    '<COFINSSN><CST>49</CST></COFINSSN>'
    """

    _schema = {
            'CST': {
                    'type': 'string',
                    'required': True,
                    'allowed': [v for v,s in constantes.S07_CST_COFINSSN]},
        }


    def _build_xml_element(self, *args, **kwargs):
        cofinssn = ET.Element(self.__class__.__name__)
        ET.SubElement(cofinssn, 'CST').text = self.CST
        return cofinssn


class COFINSOutr(Entity):
    """
    Grupo de COFINS para outras operações, CST 99.
    Representa o grupo S06 ``COFINSOutr``.

    .. sourcecode:: python

        >>> cofins = COFINSOutr(CST='99', vBC=Decimal('1.00'), pCOFINS=Decimal('0.0065'))
        >>> ET.tostring(cofins.xml())
        '<COFINSOutr><CST>99</CST><vBC>1.00</vBC><pCOFINS>0.0065</pCOFINS></COFINSOutr>'
        >>> cofins = COFINSOutr(CST='99', qBCProd=Decimal('100.0000'), vAliqProd=Decimal('0.6500'))
        >>> ET.tostring(cofins.xml())
        '<COFINSOutr><CST>99</CST><qBCProd>100.0000</qBCProd><vAliqProd>0.6500</vAliqProd></COFINSOutr>'

        # atributo vBC depende de pCOFINS que não foi informado
        >>> cofins = COFINSOutr(CST='99', vBC=Decimal('1.00')) # vBC depende de pCOFINS
        >>> cofins.xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # atributo qBCProd depende de vAliqProd que não foi informado
        >>> cofins = COFINSOutr(CST='99', qBCProd=Decimal('100.0000'))
        >>> cofins.xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # neste caso, deve falhar pois vBC ou qBCProd não foram informados
        >>> cofins = COFINSOutr(CST='99')
        >>> cofins.xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'COFINSOutr' requer exclusivamente 'vBC' ou 'qBCProd' (nenhum informado)

        # neste caso, deve falhar pois apenas um ou outro grupo pode ser informado:
        # ou informa-se vBC e pCOFINS ou informa-se qBCProd e vAliqProd
        >>> cofins = COFINSOutr(CST='99', vBC=Decimal('1.00'), pCOFINS=Decimal('1.00'), qBCProd=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> cofins.xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'COFINSOutr' requer exclusivamente 'vBC' ou 'qBCProd' (ambos informados)

        # neste caso as falhara pela ausencia das dependencias:
        # pCOFINS depende de vBC e vAliqProd depende de qBCProd
        >>> cofins = COFINSOutr(CST='99', pCOFINS=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> cofins.xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

    """

    _schema = {
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
        }


    def _build_xml_element(self, *args, **kwargs):

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
            ET.SubElement(cofinsoutr, 'vBC').text = '{:n}'.format(self.vBC)
            ET.SubElement(cofinsoutr, 'pCOFINS').text = \
                    '{:n}'.format(self.pCOFINS)

        elif hasattr(self, 'qBCProd'):
            ET.SubElement(cofinsoutr, 'qBCProd').text = \
                    '{:n}'.format(self.qBCProd)
            ET.SubElement(cofinsoutr, 'vAliqProd').text = \
                    '{:n}'.format(self.vAliqProd)

        return cofinsoutr


class COFINSST(Entity):
    """
    Grupo de COFINS substituição tributária.
    Representa o grupo T01 ``COFINSST``.

    .. sourcecode:: python

        >>> cofins = COFINSST(vBC=Decimal('1.00'), pCOFINS=Decimal('0.0065'))
        >>> ET.tostring(cofins.xml())
        '<COFINSST><vBC>1.00</vBC><pCOFINS>0.0065</pCOFINS></COFINSST>'
        >>> cofins = COFINSST(qBCProd=Decimal('100.0000'), vAliqProd=Decimal('0.6500'))
        >>> ET.tostring(cofins.xml())
        '<COFINSST><qBCProd>100.0000</qBCProd><vAliqProd>0.6500</vAliqProd></COFINSST>'

        # atributo vBC depende de pCOFINS que não foi informado
        >>> cofins = COFINSST(vBC=Decimal('1.00')) # vBC depende de pCOFINS
        >>> cofins.xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # atributo qBCProd depende de vAliqProd que não foi informado
        >>> cofins = COFINSST(qBCProd=Decimal('100.0000'))
        >>> cofins.xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

        # neste caso, deve falhar pois vBC ou qBCProd não foram informados
        >>> cofins = COFINSST()
        >>> cofins.xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'COFINSST' requer exclusivamente 'vBC' ou 'qBCProd' (nenhum informado)

        # neste caso, deve falhar pois apenas um ou outro grupo pode ser informado:
        # ou informa-se vBC e pCOFINS ou informa-se qBCProd e vAliqProd
        >>> cofins = COFINSST(vBC=Decimal('1.00'), pCOFINS=Decimal('1.00'), qBCProd=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> cofins.xml()
        Traceback (most recent call last):
         ...
        ValidationError: Grupo 'COFINSST' requer exclusivamente 'vBC' ou 'qBCProd' (ambos informados)

        # neste caso as falhara pela ausencia das dependencias:
        # pCOFINS depende de vBC e vAliqProd depende de qBCProd
        >>> cofins = COFINSST(pCOFINS=Decimal('1.00'), vAliqProd=Decimal('1.00'))
        >>> cofins.xml()
        Traceback (most recent call last):
         ...
        ValidationError: ...

    """

    _schema = {
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
        }


    def _build_xml_element(self, *args, **kwargs):

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
            ET.SubElement(pisst, 'vBC').text = '{:n}'.format(self.vBC)
            ET.SubElement(pisst, 'pCOFINS').text = '{:n}'.format(self.pCOFINS)

        elif hasattr(self, 'qBCProd'):
            ET.SubElement(pisst, 'qBCProd').text = '{:n}'.format(self.qBCProd)
            ET.SubElement(pisst, 'vAliqProd').text = \
                    '{:n}'.format(self.vAliqProd)

        return pisst


class ISSQN(Entity):
    """
    Grupo do ISSQN. Representa o grupo U01 ``ISSQN``.

    .. sourcecode:: python

        >>> issqn = ISSQN(vDeducISSQN=Decimal('10.00'), vAliq=Decimal('7.00'), cNatOp='01', indIncFisc='2')
        >>> ET.tostring(issqn.xml())
        '<ISSQN><vDeducISSQN>10.00</vDeducISSQN><vAliq>7.00</vAliq><cNatOp>01</cNatOp><indIncFisc>2</indIncFisc></ISSQN>'

        >>> issqn = ISSQN(vDeducISSQN=Decimal('10.00'), vAliq=Decimal('7.00'), cNatOp='01', indIncFisc='2', cMunFG='3511102', cListServ='01.01', cServTribMun='01234567890123456789')
        >>> ET.tostring(issqn.xml())
        '<ISSQN><vDeducISSQN>10.00</vDeducISSQN><vAliq>7.00</vAliq><cMunFG>3511102</cMunFG><cListServ>01.01</cListServ><cServTribMun>01234567890123456789</cServTribMun><cNatOp>01</cNatOp><indIncFisc>2</indIncFisc></ISSQN>'
    """

    _schema = {
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
        }

    def _build_xml_element(self, *args, **kwargs):

        issqn = ET.Element(self.__class__.__name__)

        ET.SubElement(issqn, 'vDeducISSQN').text = \
                '{:n}'.format(self.vDeducISSQN)

        ET.SubElement(issqn, 'vAliq').text = '{:n}'.format(self.vAliq)

        if hasattr(self, 'cMunFG'):
            ET.SubElement(issqn, 'cMunFG').text = self.cMunFG

        if hasattr(self, 'cListServ'):
            ET.SubElement(issqn, 'cListServ').text = self.cListServ

        if hasattr(self, 'cServTribMun'):
            ET.SubElement(issqn, 'cServTribMun').text = self.cServTribMun

        ET.SubElement(issqn, 'cNatOp').text = self.cNatOp
        ET.SubElement(issqn, 'indIncFisc').text = self.indIncFisc

        return issqn


class Imposto(Entity):
    """
    Grupo de tributos incidentes no produto ou serviço.
    Representa o grupo M01 ``imposto``.

    .. sourcecode:: python

        >>> imposto = Imposto(
        ...         vItem12741=Decimal('0.10'),
        ...         icms=ICMS00(Orig='0', CST='00', pICMS=Decimal('18.00')),
        ...         pis=PISSN(CST='49'),
        ...         cofins=COFINSSN(CST='49'))
        >>> ET.tostring(imposto.xml())
        '<imposto><vItem12741>0.10</vItem12741><ICMS00><Orig>0</Orig><CST>00</CST><pICMS>18.00</pICMS></ICMS00><PISSN><CST>49</CST></PISSN><COFINSSN><CST>49</CST></COFINSSN></imposto>'

        # sem pis
        >>> imposto = Imposto(cofins=COFINSSN(CST='49'))
        >>> imposto.xml()
        Traceback (most recent call last):
         ...
        ValidationError: 'Imposto' (grupo M01 'imposto') atributo 'pis' nao pode ser 'None'

        # sem cofins
        >>> imposto = Imposto(pis=PISSN(CST='49'))
        >>> imposto.xml()
        Traceback (most recent call last):
         ...
        ValidationError: 'Imposto' (grupo M01 'imposto') atributo 'cofins' nao pode ser 'None'

    """

    icms = None
    """
    Opcionalmente, aponta para um dos grupos de ICMS (:class:`ICMS00`,
    :class:`ICMS40`, :class:`ICMSSN102` ou :class:`ICMSSN900`) se o item
    for um produto tributado pelo ICMS ou ``None`` em caso contrário.
    """

    pis = None
    """
    Obrigatoriamente aponta para um dos grupos de PIS (:class:`PISAliq`,
    :class:`PISQtde`, :class:`PISNT`, :class:`PISSN` ou :class:`PISOutr`).
    """

    pisst = None
    """
    Aponta para o grupo do PIS Substituição Tributária :class:`PISST` se
    for o caso, ou ``None``.
    """

    cofins = None
    """
    Obrigatoriamente aponta para um dos grupos de COFINS (:class:`COFINSAliq`,
    :class:`COFINSQtde`, :class:`COFINSNT`, :class:`COFINSSN` ou
    :class:`COFINSOutr`).
    """

    cofinsst = None
    """
    Aponta para o grupo do COFINS Substituição Tributária :class:`COFINSST`
    se for o caso, ou ``None``.
    """

    issqn = None
    """
    Opcionalmente, aponta para o grupo de ISSQN (:class:`ISSQN`) se o item
    for um serviço tributado pelo ISSQN ou ``None`` em caso contrário.
    """

    _schema = {
            'vItem12741': { # M02
                    'type': 'decimal',
                    'required': False}
        }


    def _build_xml_element(self, *args, **kwargs):

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
                    '{:n}'.format(self.vItem12741)

        if self.icms is not None:
            imposto.append(self.icms.xml())

        imposto.append(self.pis.xml())

        if self.pisst is not None:
            imposto.append(self.pisst.xml())

        imposto.append(self.cofins.xml())

        if self.cofinsst is not None:
            imposto.append(self.cofinsst.xml())

        if self.issqn is not None:
            imposto.append(self.issqn.xml())

        return imposto


class DescAcrEntr(Entity):
    """
    Grupo de valores de entrada de desconto/acréscimo sobre subtotal.
    Representa o grupo W19 ``DescAcrEntr``.

    .. sourcecode:: python

        >>> grupo = DescAcrEntr()
        >>> ET.tostring(grupo.xml())
        '<DescAcrEntr />'

        >>> grupo = DescAcrEntr(
        ...         vDescSubtot=Decimal('0.01'),
        ...         vAcresSubtot=Decimal('0.02'),
        ...         vCFeLei12741=Decimal('0.03'))
        >>> ET.tostring(grupo.xml())
        '<DescAcrEntr><vDescSubtot>0.01</vDescSubtot><vAcresSubtot>0.02</vAcresSubtot><vCFeLei12741>0.03</vCFeLei12741></DescAcrEntr>'

    """

    _schema = {
            'vDescSubtot': {
                    'type': 'decimal',
                    'required': False},
            'vAcresSubtot': {
                    'type': 'decimal',
                    'required': False},
            'vCFeLei12741': {
                    'type': 'decimal',
                    'required': False},
        }


    def _build_xml_element(self, *args, **kwargs):
        grupo = ET.Element(self.__class__.__name__)

        if hasattr(self, 'vDescSubtot'):
            ET.SubElement(grupo, 'vDescSubtot').text = \
                    '{:n}'.format(self.vDescSubtot)

        if hasattr(self, 'vAcresSubtot'):
            ET.SubElement(grupo, 'vAcresSubtot').text = \
                    '{:n}'.format(self.vAcresSubtot)

        if hasattr(self, 'vCFeLei12741'):
            ET.SubElement(grupo, 'vCFeLei12741').text = \
                    '{:n}'.format(self.vCFeLei12741)

        return grupo


class MeioPagamento(Entity):
    """
    Grupo de informação do meio de pagamento.
    Representa o grupo WA02 ``MP``.

    .. sourcecode:: python

        >>> mp = MeioPagamento(cMP='01', vMP=Decimal('10.00'))
        >>> ET.tostring(mp.xml())
        '<MP><cMP>01</cMP><vMP>10.00</vMP></MP>'

        >>> mp = MeioPagamento(cMP='01', vMP=Decimal('10.00'), cAdmC='999')
        >>> ET.tostring(mp.xml())
        '<MP><cMP>01</cMP><vMP>10.00</vMP><cAdmC>999</cAdmC></MP>'

    """

    _schema = {
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
        }


    def _build_xml_element(self, *args, **kwargs):
        mp = ET.Element('MP')
        ET.SubElement(mp, 'cMP').text = self.cMP
        ET.SubElement(mp, 'vMP').text = '{:n}'.format(self.vMP)
        if hasattr(self, 'cAdmC'):
            ET.SubElement(mp, 'cAdmC').text = self.cAdmC
        return mp


class InformacoesAdicionais(Entity):
    """
    Grupo de informações adicionais. Representa o grupo Z01 ``infAdic``.

    .. sourcecode:: python

        >>> grupo = InformacoesAdicionais()
        >>> ET.tostring(grupo.xml())
        '<infAdic />'

        >>> grupo = InformacoesAdicionais(infCpl='Teste')
        >>> ET.tostring(grupo.xml())
        '<infAdic><infCpl>Teste</infCpl></infAdic>'

    """

    _schema = {
            'infCpl': {
                    'type': 'string',
                    'required': False,
                    'minlength': 1, 'maxlength': 5000},
        }


    def _build_xml_element(self, *args, **kwargs):
        grupo = ET.Element('infAdic')
        if hasattr(self, 'infCpl'):
            ET.SubElement(grupo, 'infCpl').text = self.infCpl
        return grupo


class CFeVenda(Entity):
    """
    Representa o CF-e-SAT de venda.

    Note que não há uma classe específica para representar o grupo ``ide`` B01,
    já que todos os seus atributos são esperados nesta classe.

    .. sourcecode:: python

        >>> cfe = CFeVenda(
        ...         CNPJ='08427847000169',
        ...         signAC=constantes.ASSINATURA_AC_TESTE,
        ...         numeroCaixa=1)
        >>> ET.tostring(cfe.xml())
        '<CFe><infCFe versaoDadosEnt="0.06"><ide><CNPJ>08427847000169</CNPJ><signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC><numeroCaixa>001</numeroCaixa></ide><dest /><total /><pagto /><infAdic /></infCFe></CFe>'

    """

    destinatario = None
    """
    Instância de :class:`Destinatario` ou ``None``
    """

    entrega = None
    """
    Instância de :class:`LocalEntrega` ou ``None``
    """

    detalhamentos = []
    """
    Lista de objetos :class:`Detalhamento`, descrevendo os produtos/serviços.
    """

    descontos_acrescimos_subtotal = None
    """
    Instância de :class:`DescAcrEntr` ou ``None``.
    """

    pagamentos = []
    """
    Lista de objetos :class`MeioPagamento`, descrevendo os meios de pagamento
    empregados na quitação do CF-e.
    """

    informacoes_adicionais = None
    """
    Instância de :class:`InformacoesAdicionais` ou ``None``.
    """

    _schema = {
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
        }


    def __init__(self, **kwargs):
        super(CFeVenda, self).__init__(
                versaoDadosEnt=constantes.VERSAO_LAYOUT_ARQUIVO_DADOS_AC,
                **kwargs)


    def _build_xml_element(self, *args, **kwargs):

        cfe = ET.Element('CFe')
        infCFe = ET.SubElement(cfe, 'infCFe')
        infCFe.attrib['versaoDadosEnt'] = self.versaoDadosEnt

        ide = ET.SubElement(infCFe, 'ide')
        ET.SubElement(ide, 'CNPJ').text = self.CNPJ
        ET.SubElement(ide, 'signAC').text = self.signAC
        ET.SubElement(ide, 'numeroCaixa').text = \
                '{:03d}'.format(self.numeroCaixa)

        dest = self.destinatario or Destinatario()
        infCFe.append(dest.xml())

        if self.entrega is not None:
            infCFe.append(self.entrega.xml())

        for n, det in enumerate(self.detalhamentos):
            infCFe.append(det.xml(nItem=n+1))

        total = ET.SubElement(infCFe, 'total')

        if self.descontos_acrescimos_subtotal is not None:
            total.append(self.descontos_acrescimos_subtotal.xml())

        pagto = ET.SubElement(infCFe, 'pagto')
        for pg in self.pagamentos:
            pagto.append(pg.xml())

        infAdic = self.informacoes_adicionais or InformacoesAdicionais()
        infCFe.append(infAdic.xml())

        return cfe


    def documento(self, as_unicode=False, incluir_decl_xml=True):
        doc = ET.tostring(self.xml(), encoding='utf-8').decode('utf-8')
        if as_unicode:
            if incluir_decl_xml:
                doc = u'{}\n{}'.format(constantes.XML_DECL_UNICODE, doc)
        else:
            if incluir_decl_xml:
                doc = '{}\n{}'.format(constantes.XML_DECL, unidecode(doc))
            else:
                doc = unidecode(doc)
        return doc
