
Projeto SATCFe
==============

.. image:: https://img.shields.io/pypi/status/satcfe.svg
    :target: https://pypi.python.org/pypi/satcfe/
    :alt: Development status

.. image:: https://img.shields.io/pypi/v/satcfe.svg
    :target: https://pypi.python.org/pypi/satcfe/
    :alt: PyPI - Latest version

.. image:: https://img.shields.io/pypi/pyversions/satcfe.svg
    :target: https://pypi.python.org/pypi/satcfe/
    :alt: PyPI - Python version

.. image:: https://img.shields.io/pypi/l/satcfe.svg
    :target: https://pypi.python.org/pypi/satcfe/
    :alt: PyPI - License

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/base4sistemas/satcfe?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
   :alt: Join chat on Gitter

-------

    This project is about `SAT-CF-e`_, a system for autorization and
    transmission for fiscal documents, developed by the Secretariat of Finance
    from state of São Paulo, Brazil. The entire project, variables, methods and
    class names, as well as documentation, are written in brazilian portuguese.

    Refer to the
    `oficial web site <https://portal.fazenda.sp.gov.br/servicos/sat/>`_ for
    more information (in brazilian portuguese only).

-------

.. image:: https://travis-ci.org/base4sistemas/satcfe.svg?branch=master
    :target: https://travis-ci.org/base4sistemas/satcfe
    :alt: Travis-CI - Build status

.. image:: https://img.shields.io/badge/docs-latest-green.svg
    :target: http://satcfe.readthedocs.io/
    :alt: Latest documentation

-------

Este projeto refere-se à tecnologia `SAT-CF-e`_ desenvolvida pela Secretaria da
Fazenda do Estado de São Paulo e faz parte de um grupo de cinco projetos que
resolvem problemas específicos, mas relacionados.

Especificamente, este projeto é uma abstração para acesso às funções da
biblioteca SAT que é fornecida pelos fabricantes dos equipamentos. Para
maiores informações, consulte a `documentação do projeto <http://satcfe.readthedocs.io/>`_.

Se estiver procurando meios para emitir um extrato do CF-e-SAT, o
`Projeto SATExtrato`_ pode ajudar.


Exemplo de Uso
--------------

Este é um exemplo básico de uso, sobre como consultar o equipamento SAT
conectado e configurado no computador local:

.. sourcecode:: Python

    >>> from satcfe import BibliotecaSAT
    >>> from satcfe import ClienteSATLocal
    >>> cliente = ClienteSATLocal(
    ...         BibliotecaSAT('/caminho/para/libsat.so'),  # ou DLL no Windows
    ...         codigo_ativacao='12345678')
    ...
    >>> resposta = cliente.consultar_sat()
    >>> print(resposta.mensagem)
    'SAT em Operação'

Para conectar e configurar o equipamento SAT você deverá seguir as orientações
do fabricante. Normalmente utiliza-se um equipamento SAT fabricado
especificamente para desenvolvimento. Para aprender mais sobre a utilização
desta biblioteca, `consulte a documentação <http://satcfe.readthedocs.io/>`_.
Se precisar de ajuda, você pode recorrer à sala de *chat* do projeto
no `Gitter <https://gitter.im/base4sistemas/satcfe>`_.


Execução dos Testes
-------------------

Este é um tópico voltado para aquelas pessoas interessadas no desenvolvimento
deste projeto em si ou para aqueles que queiram experimentar algum *setup*
alternativo, como outras versões de Python ou das dependências do projeto.

Para facilitar a execução dos testes e não correr riscos de executar certos
comandos em um equipamento real (mesmo que seja um equipamento para
desenvolvimento), os testes podem ser executados contra uma biblioteca de
simulação, chamada de **mockuplib**, que acompanha o projeto.

Portanto, a maneira mais prática é usando `Pipenv`_ com `tox`_, contra a
biblioteca de simulação. Primeiro compile a biblioteca de simulação (você irá
precisar das ferramentas `GNU Make`_ e `GNU GCC`_) e então execute ``tox`` via
``Pipenv``:

.. sourcecode:: text

    $ git clone git@github.com:base4sistemas/satcfe.git
    $ cd satcfe
    $ make mockuplib
    $ pipenv install --dev --clear
    $ pipenv run tox

Dê uma olhada no arquivo ``tox.ini`` e procure pela propriedade ``envlist``,
que relaciona as versões de Python que serão usadas nos testes. Se você quiser
executar os testes contra uma versão específica de Python, utilize a
opção ``-e``. Por exemplo, para executar os testes com a versão 3.6 de Python:

.. sourcecode:: text

    $ pipenv run tox -e py36

Existem muitas outras configurações e opções avançadas de testes para
desenvolvimento desta biblioteca, caso esteja interessado neste tópico, na
`documentação do projeto <http://satcfe.readthedocs.io/>`_.

.. _`SAT-CF-e`: https://portal.fazenda.sp.gov.br/servicos/sat/
.. _`Projeto SATExtrato`: https://github.com/base4sistemas/satextrato
.. _`SATComum`: https://github.com/base4sistemas/satcomum
.. _`Pipenv`: https://pipenv.readthedocs.io/
.. _`tox`: https://tox.readthedocs.io/
.. _`GNU Make`: https://www.gnu.org/software/make/
.. _`GNU GCC`: https://gcc.gnu.org/
