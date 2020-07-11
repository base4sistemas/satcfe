
Projeto SATCFe
==============

.. image:: https://travis-ci.org/base4sistemas/satcfe.svg?branch=master
    :target: https://travis-ci.org/base4sistemas/satcfe
    :alt: Build status

.. image:: https://img.shields.io/pypi/status/satcfe.svg
    :target: https://pypi.python.org/pypi/satcfe/
    :alt: Development status

.. image:: https://img.shields.io/badge/docs-latest-green.svg
    :target: https://satcfe.readthedocs.io/
    :alt: Latest documentation

.. image:: https://img.shields.io/badge/python%20version-2.7-blue.svg
    :target: https://pypi.python.org/pypi/satcfe/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/l/satcfe.svg
    :target: https://pypi.python.org/pypi/satcfe/
    :alt: License

.. image:: https://img.shields.io/pypi/v/satcfe.svg
    :target: https://pypi.python.org/pypi/satcfe/
    :alt: Latest version

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/base4sistemas/satcfe
   :target: https://gitter.im/base4sistemas/satcfe?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

-------

    This project is about `SAT-CF-e`_, a system for autorization and
    transmission for fiscal documents, developed by the Secretariat of Finance
    from state of São Paulo, Brazil. The entire project, variables, methods and
    class names, as well as documentation, are written in brazilian portuguese.

    Refer to the
    `oficial web site <https://portal.fazenda.sp.gov.br/servicos/sat/>`_ for
    more information (in brazilian portuguese only).

-------

Este projeto refere-se à tecnologia `SAT-CF-e`_ desenvolvida pela Secretaria da
Fazenda do Estado de São Paulo e faz parte de um grupo de cinco projetos que
resolvem problemas específicos, mas relacionados.

Especificamente, este projeto é uma abstração para acesso às funções da
biblioteca SAT que é fornecida pelos fabricantes dos equipamentos. Para
maiores informações, consulte a `documentação do projeto <http://satcfe.readthedocs.io/>`_.

Se estiver procurando meios para imprimir um extrato do CF-e-SAT, o
`Projeto SATExtrato`_ pode ajudar.


Exemplo de Uso
==============

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


Desenvolvimento e Testes
========================

Configure o ambiente de desenvolvimento:

.. sourcecode:: shell

    $ git clone git@github.com:base4sistemas/satcfe.git
    $ cd satcfe
    $ python -m venv .env
    $ source .env/bin/activate
    (.env) $ pip install -r requirements/dev.txt

Para facilitar a execução dos testes e não correr riscos de executar certos
comandos em um equipamento real (mesmo que seja um equipamento para
desenvolvimento), os testes podem ser executados contra uma biblioteca de
simulação, chamada de **mockuplib**, que acompanha o projeto.

Primeiro compile a biblioteca de simulação (você irá precisar das
ferramentas `GNU Make`_ e `GNU GCC`_) e então execute ``tox`` contra as
versões de interpretadores disponíveis no seu ambiente:

.. sourcecode:: shell

    (.env) $ make mockuplib
    (.env) $ tox

Ou apenas execute ``pytest`` diretamente, para executar apenas os testes que
não invocam a biblioteca do fabricante:

.. sourcecode:: shell

    (.env) $ pytest

Um outra maneira, é executar ``pytest`` diretamente contra a biblioteca de
simulação, que será compilada imediatamente antes de invocar os testes:

.. sourcecode:: shell

    (.env) $ make testall

Existem muitas outras configurações e opções avançadas de testes para
desenvolvimento desta biblioteca, caso esteja interessado neste tópico no
`Wiki`_ ou na `documentação do projeto <http://satcfe.readthedocs.io/>`_.


.. _`SAT-CF-e`: https://portal.fazenda.sp.gov.br/servicos/sat/
.. _`Projeto SATExtrato`: https://github.com/base4sistemas/satextrato
.. _`SATComum`: https://github.com/base4sistemas/satcomum
.. _`Wiki`: https://github.com/base4sistemas/satcfe/wiki
.. _`tox`: https://tox.readthedocs.io/
.. _`GNU Make`: https://www.gnu.org/software/make/
.. _`GNU GCC`: https://gcc.gnu.org/
