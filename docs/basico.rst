
.. _configuracao-basica:

Configuração Básica
===================

Existem dois cenários para configuração de um Cliente SAT. No primeiro, o
equipamento SAT está conectado diretamente ao computador em que o aplicativo
comercial está instalado. No segundo, o aplicativo comercial compartilha o
equipamento SAT com outros aplicativos através de uma rede local.

No primeiro cenário, basta configurar o *código de ativação* e o *número do
caixa* de modo que esses dados não precisarão ser informados sempre que uma
função for invocada:

.. sourcecode:: python

    from satcfe import conf

    conf.codigo_ativacao = '123123123'
    conf.numero_caixa = 1

No segundo cenário, basta configurar ao acesso ao `SATHub`_:

.. sourcecode:: python

    from satcfe import conf

    conf.numero_caixa = 15
    conf.sathub.host = '192.168.0.101'
    conf.sathub.port = 8088

A maneira como essas configurações serão persistidas pela aplicação comercial e
como elas serão atribuídas na iniciação da aplicação está fora do escopo deste
projeto.

.. include:: references.rst