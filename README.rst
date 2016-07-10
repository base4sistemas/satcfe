
Projeto SATCFe
==============

.. image:: https://img.shields.io/pypi/status/satcfe.svg
    :target: https://pypi.python.org/pypi/satcfe/
    :alt: Development status

.. image:: https://img.shields.io/badge/python%20version-2.7-blue.svg
    :target: https://pypi.python.org/pypi/satcfe/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/l/satcfe.svg
    :target: https://pypi.python.org/pypi/satcfe/
    :alt: License

.. image:: https://img.shields.io/pypi/v/satcfe.svg
    :target: https://pypi.python.org/pypi/satcfe/
    :alt: Latest version

.. image:: https://img.shields.io/badge/docs-latest-green.svg
    :target: http://satcfe.readthedocs.org/
    :alt: Latest Documentation

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/base4sistemas/satcfe
   :target: https://gitter.im/base4sistemas/satcfe?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

-------

    This project is about `SAT-CF-e`_ which is a system for autorization and
    transmission of fiscal documents, developed by Finance Secretary of
    state of São Paulo, Brazil. This entire project, variables, methods and
    class names, as well as documentation, are written in brazilian
    portuguese.

    Refer to the `oficial web site <http://www.fazenda.sp.gov.br/sat/>`_ for
    more information (in brazilian portuguese only).

-------

.. image:: https://drone.io/github.com/base4sistemas/satcfe/status.png
    :target: https://drone.io/github.com/base4sistemas/satcfe/latest
    :alt: Build status

-------

Este projeto refere-se à tecnologia `SAT-CF-e`_ desenvolvida pela Secretaria da
Fazenda do Estado de São Paulo e faz parte de um grupo de cinco projetos que
resolvem problemas específicos, mas relacionados.

Especificamente, este projeto é uma abstração que fornece acesso às funções da
biblioteca SAT, que é fornecida pelos fabricantes de equipamentos SAT. Para
maiores informações, consulte a `documentação do projeto
<http://satcfe.readthedocs.org/>`_.

Se estiver procurando meios para emitir um extrato do CF-e-SAT, o
`Projeto SATExtrato`_ pode ajudar.


Utilização
----------

Este é um exemplo básico de uso, para consultar o equipamento SAT:

.. sourcecode:: Python

    >>> from satcfe import BibliotecaSAT
    >>> from satcfe import ClienteSATLocal
    >>> cliente = ClienteSATLocal(BibliotecaSAT('/caminho/para/sat.dll'),
    ...         codigo_ativacao='12345678')
    ...
    >>> resposta = cliente.consultar_sat()
    >>> resposta.mensagem
    u'SAT em Opera\xe7\xe3o'


Executando os Testes
--------------------

É possível executar os testes contra qualquer equipamento SAT, em qualquer
plataforma ou arquitetura, desde que você possua um kit de desenvolvimento,
contendo o equipamento SAT e as bibliotecas do fabricante.

Para executar os testes em um ambiente Linux é preciso definir algumas variáveis
de ambiente para configurar o acesso à biblioteca SAT fornecida pelo fabricante
do equipamento, o código de ativação e o Estado do domicílio fiscal em que o
equipamento SAT está registrado.

.. sourcecode:: shell

    $ export SATCFE_TEST_LIB=/opt/fabricante/libsat.so
    $ export SATCFE_TEST_LIB_CONVENCAO=1
    $ export SATCFE_TEST_CODIGO_ATIVACAO=12345678
    $ export SATCFE_TEST_UF=SP

Antes de executar os testes propriamente, é conveniente revisar a parametrização
no script ``runtests.sh`` que, dependendo do seu equipamento SAT, os valores
para configuração dos dados do emitente e outros dados podem variar.

.. sourcecode:: shell

    $ ./runtests.sh tanca


Parametrização
~~~~~~~~~~~~~~

As opções de parametrização dos testes são:

``--codigo-ativacao``
    | Código de ativação configurado no equipamento SAT.

``--numero-caixa``
    | Número do caixa de origem.

``--assinatura-ac``
    | Conteúdo da assinatura da AC.

``--cnpj-ac``
    | CNPJ da empresa desenvolvedora da AC (apenas dígitos).

``--emitente-cnpj``
    | CNPJ do estabelecimento emitente (apenas dígitos).

``--emitente-ie``
    | Inscrição estadual do emitente (apenas dígitos).

``--emitente-im``
    | Inscrição municipal do emitente (apenas dígitos).

``--emitente-uf``
    | Sigla da unidade federativa do estabelecimento emitente.

``--emitente-issqn-regime``
    | Regime especial de tributação do ISSQN do emitente, em casos de
    | testes de emissão de venda e/ou cancelamento.

``--emitente-issqn-rateio``
    | Indicador de rateio do desconto sobre o subtotal para produtos
    | tributados no ISSQN do emitente, em casos de testes de emissão de
    | venda e/ou cancelamento.

``--lib-caminho``
    | Caminho para a biblioteca SAT.

``--lib-convencao``
    | Convenção de chamada para a biblioteca SAT.

``--skip-funcoes-sat``
    | Ignora testes de todas as funções SAT evitando qualquer acesso ao
    | equipamento.

``--skip-[funcao]``
    | Permite evitar a execução de testes para uma função em particular,
    | substituindo ``[funcao]`` pelo nome da função SAT em letras minúsculas,
    | por exemplo, para evitar a execução da função ``ConsultarSAT`` use
    | ``--skip-consultarsat``.


Executando Testes Manualmente
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se não quiser usar o script ``runtests.sh`` ou se estiver usando um ambiente
Windows, poderá invocar a execução dos testes manualmente, por exemplo:

.. sourcecode:: ps1con

    C> python setup.py test -a "--cnpj-ac=01234567000199 ..."

Ou para apenas executar os testes unitários que não interagem com o equipamento
SAT de nenhuma maneira:

.. sourcecode:: shell

    $ python setup.py test -a "-rs --skip-funcoes-sat"

.. _`SAT-CF-e`: http://www.fazenda.sp.gov.br/sat/
.. _`Projeto SATExtrato`: https://github.com/base4sistemas/satextrato
