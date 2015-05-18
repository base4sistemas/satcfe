
Projeto SAT-CF-e
================

.. image:: https://img.shields.io/badge/status-planning-red.svg
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

-------

    This project is about `SAT-CF-e`_ which is a system for autorization and
    transmission of fiscal documents, developed by Finance Secretary of
    state of São Paulo, Brazil. This entire project, variables, methods and
    class names, as well as documentation, are written in brazilian
    portuguese.

    Refer to the `oficial web site <http://www.fazenda.sp.gov.br/sat/>`_ for
    more information (in brazilian portuguese only).


Este projeto implementa uma abstração para acesso às funções da DLL do
`SAT-CF-e`_ para acesso ao equipamento SAT. Por exemplo:

.. sourcecode:: Python

    >>> from satcomum import constantes
    >>> from satcfe import DLLSAT
    >>> from satcfe import ClienteSATLocal
    >>> from satcfe import conf

    >>> conf.codigo_ativacao = '123456789'

    >>> cliente = ClienteSATLocal(DLLSAT(
    ...        caminho='/caminho/para/sat.dll',
    ...        convecao=constantes.WINDOWS_STDCALL))

    >>> resposta = cliente.consultar_sat()
    >>> resposta.mensagem
    u'SAT em Opera\xe7\xe3o'


Extratos do CF-e-SAT
====================

Para gerar os extratos do CF-e de venda e/ou cancelamento, consulte o
projeto `satextrato`_.


Executando os Testes
====================

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


Possíveis Questões
==================

Talvez você esteja se perguntando:

**Nas entidades, por que vocês não usaram o schema XSD?**
    O governo de São Paulo não disponibilizou os *schemas XSD* para o documento
    CF-e que é gerado pela AC. Existem *schemas XSD* apenas para serem usados
    pelo software do equipamento SAT, que completa o CF-e gerado pela e o envia
    para autorização pela SEFAZ.

    Tenho visto algumas pessoas muito bem intencionadas pela internet editando
    os *schemas XSD* à mão, mas isso não é prático porque, primeiro os schemas
    XSD normalmente são gerados automaticamente por softwares como Apache AXIS
    ou seja lá qual ferramenta estejam usando para manter as regras de negócio e
    os *web-services*; segundo porque editar um arquivo desses à mão é
    totalmente suscetível à erros e, afinal, quem vai testar o XSD que irá
    validar o seu XML?

    A escolha de implementar as entidades usando `Cerberus`_ permite uma
    abordagem simples e leve, fácil de manter e de testar e, no futuro, caso o
    governo resolva publicar *schemas XSD* para a AC usar, então modificaremos a
    abordagem **mantendo os nomes dos atributos atuais**, tornando (espero) a
    modificação o mais simples possível para a aplicação cliente.

    Além disso, a especificação do XML do CF-e é simples e bem documentada.
    Veja na Especificação de Requisitos do SAT-CF-e os itens 4.2.2 e 4.2.3, nas
    tabelas de atributos, onde a primeira coluna "Origem" indica "SAT" ou "AC".
    Os elementos e atributos com origem na "AC" são aqueles em que a Automação
    Comercial (o aplicativo cliente) deverá incluir no XML de venda ou de
    cancelamento que será enviado ao equipamento SAT.


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
.. _`Cerberus`: https://cerberus.readthedocs.org/
.. _`satextrato`: https://github.com/base4sistemas/satextrato
.. _`Dimep`: http://www.dimep.com.br/
