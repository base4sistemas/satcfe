
Executando Testes
=================

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
para configuração dos dados do emitente e outros dados podem variar. Isto irá
executar os testes invocando as funções ``ConsultarSAT`` e
``ConsultarStatusOperacional`` (revise o script para adicionar ou remover
funções a serem invocadas):

.. sourcecode:: shell

    $ ./runtests.sh tanca


Parametrização
--------------

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

``--acessa-sat``
    | Permite que sejam executados os testes que acessem a biblioteca SAT,
    | eventualmente acessando o equipamento SAT real

``--invoca-[funcao]``
    | Permite que sejam executados os testes que acessem a biblioteca SAT,
    | eventualmente acessando o equipamento SAT real, para acesso à função
    | especificada (``funcao``). Por exemplo, ``--invoca-consultarsat``.


Executando Testes Manualmente
-----------------------------

Você poderá executar os testes unitários contra uma biblioteca de simulação que
acompanha o projeto, chamada **mockuplib**. Isso facilita a execução dos testes
unitários sem correr riscos de executar comandos sensíveis (como troca de código
de ativação) em um equipamento real, mesmo que seja um equipamento específico
para desenvolvimento.

Você irá precisar das ferramentas `GNU Make`_ e `GNU GCC`_ para compilar a
biblioteca de simulação e então usar `Pipenv`_ e `tox`_ para executar os testes
unitários:

.. sourcecode:: shell

    $ make mockuplib
    $ pipenv install --dev --clear
    $ pipenv run tox

Dê uma olhada no arquivo ``tox.ini`` e procure pela propriedade ``envlist``,
que relaciona as versões de Python que serão usadas nos testes. Se você quiser
executar os testes contra uma versão específica de Python, utilize a
opção ``-e``. Por exemplo, para executar os testes com a versão 3.6 de Python:

.. sourcecode:: text

    $ pipenv run tox -e py36


Testando Funções Específicas
----------------------------

Se não quiser (ou não puder) usar o script ``runtests.sh`` por alguma razão,
você poderá comandar a execução dos testes unitários e dos testes que acessam a
biblioteca SAT e invocam funções específicas (você terá que especificar uma por
uma). Por exemplo, para executar o teste da função ``ConsultarSAT`` faça:

.. sourcecode:: shell

    $ pipenv run python setup.py test -a "--acessa-sat --invoca-consultarsat"


Executando Testes usando GNU Make
---------------------------------

Também é possível executar os testes (e outras tarefas) usando o ``Makefile``
que acompanha o projeto. Por exemplo para executar os testes que **não**
acessam as funções da biblioteca SAT, faça:

.. sourcecode:: shell

    $ pipenv shell
    $ make test

Para executar todos os testes, **inclusive os testes contra a biblioteca SAT**,
use o alvo ``testall``. Esse alvo irá também compilar a biblioteca SAT *mockup*
que acompanha o projeto justamente para execução completa dos testes, sem o
risco de acessar um equipamento SAT. De qualquer maneira, mesmo utilizando a
biblioteca *mockup* ou qualquer outra biblioteca SAT, é preciso definir a
variável de ambiente ``SATCFE_TEST_LIB`` que deve apontar para a biblioteca SAT
que será utilizada nos testes, por exemplo:

.. sourcecode:: shell

    $ export SATCFE_TEST_LIB=satcfe/tests/mockup/libmockupsat.so
    $ make testall


Variáveis de Ambiente para os Testes
------------------------------------

Estas são todas as variáveis de ambiente utilizadas no script ``runtests.sh`` e
usadas como valor padrão quando os testes são invocados manualmente (e seus
valores padrão):

+---------------------------------------+---------------------------+
| Variável                              | Valor Padrão              |
+=======================================+===========================+
| ``SATCFE_TEST_LIB``                   | ``libsat.so``             |
+---------------------------------------+---------------------------+
| ``SATCFE_TEST_LIB_CONVENCAO``         | ``1`` [1]_                |
+---------------------------------------+---------------------------+
| ``SATCFE_TEST_CODIGO_ATIVACAO``       | ``12345678`` [2]_         |
+---------------------------------------+---------------------------+
| ``SATCFE_TEST_EMITENTE_UF``           | ``SP`` [2]_               |
+---------------------------------------+---------------------------+
| ``SATCFE_TEST_CNPJ_AC``               | ``16716114000172`` [2]_   |
+---------------------------------------+---------------------------+
| ``SATCFE_TEST_EMITENTE_CNPJ``         | ``08723218000186`` [2]_   |
+---------------------------------------+---------------------------+
| ``SATCFE_TEST_EMITENTE_IE``           | ``149626224113`` [2]_     |
+---------------------------------------+---------------------------+
| ``SATCFE_TEST_EMITENTE_IM``           | ``123123`` [2]_           |
+---------------------------------------+---------------------------+
| ``SATCFE_TEST_EMITENTE_ISSQN_REGIME`` | ``3`` [3]_                |
+---------------------------------------+---------------------------+
| ``SATCFE_TEST_EMITENTE_ISSQN_RATEIO`` | ``N`` [4]_                |
+---------------------------------------+---------------------------+

.. [1] Veja constante ``CONVENCOES_CHAMADA`` no projeto `SATComum`_ para
    conhecer os valores possíveis.

.. [2] Os valores padrão são para equipamentos SAT de desenvolvimento
    fabricados pela Tanca. Se o seu equipamento for de um fabricante diferente
    substitua pelos valores indicados no manual. O script ``runtests.sh`` tem
    os valores padrão para alguns outros fabricantes, mas observe que esses
    valores podem mudar entre os modelos de um mesmo fabricante.

.. [3] Veja constante ``C15_CREGTRIBISSQN_EMIT`` no projeto `SATComum`_ para
    conhecer os valores possíveis.

.. [4] Veja constante ``C16_INDRATISSQN_EMIT`` no projeto `SATComum`_ para
    conhecer os valores possíveis.


.. include:: references.rst
