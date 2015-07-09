
Anatomia do CF-e
================

O *Cupom Fiscal eletrônico*, CF-e, é um documento fiscal com validade jurídica
que não existe fisicamente, mas apenas de forma eletrônica, em formato `XML`_,
que descreve todos os aspectos práticos de uma operação de venda ou do
cancelamento de uma venda. A figura abaixo ilustra a anatomia de um CF-e de
venda, destacando todos os seus elementos de mais alto nível.

.. image:: _static/images/anatomia-cfe.png
    :alt: Anatomia de CF-e de venda
    :align: center

Um documento CF-e que se compare com a ilustração, grosseiramente se traduz para
o seguinte fragmento XML:

.. sourcecode:: xml

    <CFe>
      <infCFe>
        <ide/>
        <emit/>
        <dest/>
        <det nItem="1">
          <prod/>
          <imposto/>
        </det>
        <total/>
        <pgto/>
      </infCFe>
      <Signature/>
    </CFe>

O ponto central da tecnologia SAT-CF-e, do ponto de vista do desenvolvedor do
aplicativo comercial, é o modelo através do qual um CF-e é construído até se
transformar em um documento com validade jurídica.

#. O aplicativo comercial inicia o CF-e construindo a maior parte dos elementos
   a partir dos dados da venda e o envia para o equipamento SAT através da
   função ``EnviarDadosVenda``;

#. O equipamento SAT complementa o CF-e, calculando e incluindo outras
   informações que são de sua responsabilidade e assinando digitalmente o
   documento, e o transmite para a SEFAZ;

#. A SEFAZ valida o documento e o retorna para o equipamento SAT que,
   finalmente, retorna a resposta para o aplicativo comercial.

Para compor um CF-e o desenvolvedor do aplicativo comercial deverá observar a
coluna **Origem** da tabela que descreve os elementos do CF-e nos itens
**4.2.2** (*layout do arquivo de venda*) e **4.2.3** (*layout do arquivo de
cancelamento*). Os elementos onde a coluna **Origem** indicar ``AC`` são os
elementos que o aplicativo comercial deverá incluir no XML. Os elementos
indicados com ``SAT`` são os elementos que o equipamento SAT deverá incluir.

.. image:: _static/images/ersat-col-origem.png
    :alt: Detalhe da coluna "Origem" indicando a origem dos elementos do CF-e
    :align: center


Entidades
=========

No contexto deste projeto as **Entidades** são as classes que são utilizadas
para descrever uma venda ou um cancelamento. A documentação da API contém uma
tabela que relaciona as classes de entidades aos elementos XML descritos na ER
SAT, em :ref:`api-modulo-satcfe-entidades`.

Lidar com API de entidades não é difícil. O exemplo abaixo mostra uma sessão do
interpretador onde é criado uma instância de
:class:`~satcfe.entidades.LocalEntrega` totalmente inválida:

.. sourcecode:: python

    >>> from satcfe.entidades import LocalEntrega
    >>> entrega = LocalEntrega()
    >>> entrega.validar()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "satcfe/entidades.py", line 298, in validar
        'atributos invalidos.'.format(self.__class__.__name__))
    cerberus.cerberus.ValidationError: Entidade "LocalEntrega" possui atributos invalidos.
    >>> entrega.erros
    {'xBairro': 'required field', 'nro': 'required field', 'UF': 'required field', 'xMun': 'required field', 'xLgr': 'required field'}

Para obter o fragmento XML de uma entidade, faça:

.. sourcecode:: python

    >>> entrega = LocalEntrega(
    ...         xLgr='Rua Armando Gulim',
    ...         nro='65',
    ...         xBairro=u'Parque Glória III',
    ...         xMun='Catanduva',
    ...         UF='SP')
    >>> entrega.documento(incluir_xml_decl=False)
    '<entrega><xLgr>Rua Armando Gulim</xLgr><nro>65</nro><xBairro>Parque Gloria III</xBairro><xMun>Catanduva</xMun><UF>SP</UF></entrega>'


Criando um CF-e de Venda
------------------------

Criar um CF-e de venda é simples no que diz respeito á composição dos elementos.
Obviamente no contexto da aplicação comercial inúmeras outras complexidades se
apresentam. Mas este exemplo simples é capaz de produzir um XML que poderá ser
enviado para o equipamento SAT, desde que você adapte certos valores para o seu
equipamento SAT e seus dados.

.. sourcecode:: python

    from satcomum import constantes
    from satcfe.entidades import Destinatario
    from satcfe.entidades import LocalEntrega
    from satcfe.entidades import Detalhamento
    from satcfe.entidades import ProdutoServico
    from satcfe.entidades import Imposto
    from satcfe.entidades import ICMSSN102
    from satcfe.entidades import PISSN
    from satcfe.entidades import COFINSSN
    from satcfe.entidades import MeioPagamento

    cfe = CFeVenda(
            CNPJ='08427847000169',
            signAC=constantes.ASSINATURA_AC_TESTE,
            numeroCaixa=1,
            destinatario=Destinatario(
                    CPF='11122233396',
                    xNome=u'João de Teste'),
            entrega=LocalEntrega(
                    xLgr='Rua Armando Gulim',
                    nro='65',
                    xBairro=u'Parque Glória III',
                    xMun='Catanduva',
                    UF='SP'),
            detalhamentos=[
                    Detalhamento(
                            produto=ProdutoServico(
                                    cProd='123456',
                                    xProd='BORRACHA STAEDTLER pvc-free',
                                    CFOP='5102',
                                    uCom='UN',
                                    qCom=Decimal('1.0000'),
                                    vUnCom=Decimal('5.75'),
                                    indRegra='A'),
                            imposto=Imposto(
                                    icms=ICMSSN102(Orig='2', CSOSN='500'),
                                    pis=PISSN(CST='49'),
                                    cofins=COFINSSN(CST='49'))),
                ],
            pagamentos=[
                    MeioPagamento(
                            cMP=constantes.WA03_DINHEIRO,
                            vMP=Decimal('10.00')),
                ])

O XML produzido por este código é um documento CF-e ainda incompleto, que deverá
ser enviado ao equipamento SAT pra que seja completado, assinado e transmitido
para a SEFAZ. Você poderá vê-lo em (INCLUIR REF AQUI).

Para submeter o documento ao equipamento SAT:

.. sourcecode:: python

    resposta = cliente.enviar_dados_venda(cfe)

A resposta...


Criando um CF-e de Cancelamento
-------------------------------

.. todo: Escrever este tópico


.. _`XML`: http://www.w3.org/XML/
