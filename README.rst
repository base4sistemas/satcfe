
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


-------

    This project is about `SAT-CF-e`_ which is a system for autorization and
    transmission of fiscal documents, developed by Finance Secretary of
    state of São Paulo, Brazil. This entire project, variables, methods and
    class names, as well as documentation, are written in brazilian
    portuguese.

    Refer to the `oficial web site <http://www.fazenda.sp.gov.br/sat/>`_ for
    more information (in brazilian portuguese only).

Este projeto refere-se à tecnologia `SAT-CF-e`_ desenvolvida pela Secretaria da
Fazenda do Estado de São Paulo e faz parte de um grupo de cinco projetos que
resolvem problemas específicos, mas relacionados.

Especificamente, este projeto é uma abstração que fornece acesso às funções da
biblioteca SAT, que é fornecida pelos fabricantes de equipamentos SAT. Para
maiores informações, consulte a `documentação do projeto
<http://satcfe.readthedocs.org/>`_.

Se estiver procurando meios para emitir um extrato do CF-e-SAT, o
`Projeto SATExtrato`_ pode ajudar.

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/base4sistemas/satcfe
   :target: https://gitter.im/base4sistemas/satcfe?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


Utilização
----------

Este é um exemplo básico de uso, para consultar o equipamento SAT:

.. sourcecode:: Python

    >>> from satcomum import constantes
    >>> from satcfe import DLLSAT
    >>> from satcfe import ClienteSATLocal
    >>> from satcfe import conf

    >>> conf.codigo_ativacao = '123456789'

    >>> cliente = ClienteSATLocal(DLLSAT(
    ...        caminho='/caminho/para/sat.dll',
    ...        convencao=constantes.WINDOWS_STDCALL))

    >>> resposta = cliente.consultar_sat()
    >>> resposta.mensagem
    u'SAT em Opera\xe7\xe3o'


Executando os Testes
--------------------

Para executar os testes faça:

.. sourcecode:: shell

    $ python setup.py test

Em ambientes Microsoft |reg| Windows |trade|, é possível executar uma série de
testes contra o equipamento SAT. Atualmente estão implementados testes apenas o
equipamento SAT D-Sat |trade| da `Dimep`_ |reg|. Como a implementação em si
independe do fabricante do equipamento SAT é fácil alterar os testes para
executar contra quaisquer outros equipamentos SAT disponíveis.

.. sourcecode:: shell

    > python setup.py test -a "--cnpj-ac=01234567000199 --codigo-ativacao=123"


..
    Sphinx Documentation: Substitutions at
    http://sphinx-doc.org/rest.html#substitutions
    Codes copied from reStructuredText Standard Definition Files at
    http://docutils.sourceforge.net/docutils/parsers/rst/include/isonum.txt

.. |copy| unicode:: U+00A9 .. COPYRIGHT SIGN
    :ltrim:

.. |reg|  unicode:: U+00AE .. REGISTERED SIGN
    :ltrim:

.. |trade|  unicode:: U+2122 .. TRADE MARK SIGN
    :ltrim:


.. _`SAT-CF-e`: http://www.fazenda.sp.gov.br/sat/
.. _`Projeto SATExtrato`: https://github.com/base4sistemas/satextrato
.. _`Dimep`: http://www.dimep.com.br/
