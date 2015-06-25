
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

No segundo cenário, basta configurar ao acesso ao SATHub:

.. sourcecode:: python

    from satcfe import conf

    conf.numero_caixa = 15
    conf.sathub.host = '192.168.0.101'
    conf.sathub.port = 8088

A maneira como essas configurações serão persistidas pela aplicação comercial e
como elas serão atribuídas na iniciação da aplicação está fora do escopo deste
projeto.


Instanciando um Cliente SAT
===========================

Para ter acesso às funções SAT é preciso instanciar um *cliente* SAT, que pode
ser um **Cliente Local**, no cenário em que o equipamento SAT está conectado ao
mesmo computador em que está instalado o aplicativo comercial, ou um **Cliente
SATHub**, quando o acesso ao equipamento SAT é compartilhado.


Cliente Local
-------------

Em um cliente local o acesso ao equipamento SAT é feito através da biblioteca
SAT que é fornecida pelo fabricante do equipamento, distribuída normalmente como
uma DLL (*dinamic-link library*, ``.dll``) ou SO (*shared object*, ``.so``), de
modo que é necessário indicar o caminho completo para a biblioteca e a convenção
de chamada:

.. sourcecode:: python

    from satcomum import constantes
    from satcfe import DLLSAT
    from satcfe import ClienteSATLocal

    cliente = ClienteSATLocal(DLLSAT(
            caminho='caminho/para/sat.dll',
            convencao=constantes.WINDOWS_STDCALL))

    resposta = cliente.consultar_sat()


Cliente SATHub
--------------

Em um cliente SATHub o acesso ao equipamento SAT é compartilhado e feito através
de uma requisição HTTP para endereço onde o servidor SATHub responde. Em ambos
os casos a chamada à função é exatamente a mesma, com exceção da instanciação
do cliente:

.. sourcecode:: python

    from satcfe import ClienteSATHub
    from satcfe import conf

    conf.sathub.numero_caixa = 7
    conf.sathub.host = '192.168.0.101'
    conf.sathub.port = 8088

    cliente = ClienteSATHub()

    resposta = cliente.consultar_sat()

Via de regra o código que acessa as funções da biblioteca SAT não deveria se
importar se o cliente é um cliente local ou remoto, de modo que o aplicativo
comercial precisa apenas implementar um *factory* que resulte no cliente SAT
adequadamente configurado.


Lidando com as Respostas
------------------------

As respostas contém os atributos que são descritos na ER SAT com nomes que sejam
o mais próximo possível da descrição oficial. Por exemplo, a função
``ConsultarSAT`` está descrita na ER SAT no item 6.1.5 e os detalhes da resposta
à esta função estão descritos no item 6.1.5.2 e diz o seguinte:

    **Retorno** ``"numeroSessao|EEEEE|mensagem|cod|mensagemSEFAZ"``

Dessa forma, a resposta à função ``ConsultarSAT`` deverá conter atributos com os
mesmos nomes descritos na ER SAT:

.. sourcecode:: python

    resposta = cliente.consultar_sat()
    print(resposta.numeroSessao)  # resulta em 'int'
    print(resposta.EEEEE)  # resulta em 'unicode'
    print(resposta.mensagem)
    print(resposta.cod)
    print(resposta.mensagemSEFAZ)

Caso ocorra um erro ao invocar o método ``consultar_sat()`` será lançada uma
exceção ``ExcecaoRespostaSAT`` contendo os detalhes do problema.


Funções Básicas
===============

.. todo: Escrever este tópico


ConsutarSAT
-----------

.. todo: Escrever este tópico


ConsultarStatusOperacional
--------------------------

.. todo: Escrever este tópico


ExtrairLogs
-----------

.. todo: Escrever este tópico


Numeração de Sessões
====================

Um outro aspecto importante
