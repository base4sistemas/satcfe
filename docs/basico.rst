
.. _configuracao-basica:

Configuração Básica
===================

Existem dois cenários para configuração de um Cliente SAT. No primeiro, o
equipamento SAT está conectado diretamente ao computador em que o aplicativo
comercial está instalado. No segundo, o aplicativo comercial compartilha o
equipamento SAT com outros aplicativos através de uma rede local.

No primeiro cenário, basta instanciar um :class:`~satcfe.clientelocal.ClienteSATLocal`
e configurar o acesso à biblioteca SAT e o código de ativação:

.. sourcecode:: python

    from satcfe import BibliotecaSAT
    from satcfe import ClienteSATLocal

    cliente = ClienteSATLocal(BibliotecaSAT('/opt/fabricante/libsat.so'),
            codigo_ativacao='12345678')


No segundo cenário, basta instanciar um :class:`~satcfe.clientesathub.ClienteSATHub`
e apontá-lo para o servidor `SATHub`_. Note que neste caso, será necessário
informar o **número do caixa**, para que o SATHub possa determinar a origem das
solicitações.

.. sourcecode:: python

    from satcfe import ClienteSATHub

    cliente = ClienteSATHub('192.168.0.101', 8088, numero_caixa=15)


Em qualquer cenário, depois de instanciado o cliente, o acesso às funções SAT é
absolutamente idêntico:

.. sourcecode:: python

    resposta = cliente.consultar_sat()


.. note::

    A maneira como essas configurações serão persistidas pela aplicação
    comercial e como elas serão atribuídas na iniciação da aplicação está fora
    do escopo deste projeto.

.. include:: references.rst
