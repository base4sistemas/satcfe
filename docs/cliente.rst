
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
uma DLL (*dinamic-link library*, ``.dll``) ou *shared library* (``.so``), de
modo que é necessário indicar o caminho completo para a biblioteca.

.. sourcecode:: python

    from satcfe import BibliotecaSAT
    from satcfe import ClienteSATLocal

    cliente = ClienteSATLocal(BibliotecaSAT('/opt/fabricante/libsat.so'),
            codigo_ativacao='12345678')

    resposta = cliente.consultar_sat()


Cliente SATHub
--------------

Em um cliente SATHub o acesso ao equipamento SAT é compartilhado e feito através
de uma requisição HTTP para endereço onde o servidor `SATHub`_ responde. Em
ambos os casos a chamada à função é exatamente a mesma, com exceção da
instanciação do cliente:

.. sourcecode:: python

    from satcfe import ClienteSATHub

    cliente = ClienteSATHub('192.168.0.101', 8088, numero_caixa=7)
    resposta = cliente.consultar_sat()

Via de regra o código que acessa as funções da biblioteca SAT não deveria se
importar se o cliente é um cliente local ou remoto, de modo que o aplicativo
comercial precisa apenas implementar um *factory* que resulte no cliente SAT
adequadamente configurado.


Numeração de Sessões
--------------------

Um outro aspecto relevante é a questão da numeração de sessões, que conforme a
ER SAT, item 6, alínea "d", diz o seguinte:

    O SAT deverá responder às requisições do AC de acordo com o número de sessão
    recebido. O aplicativo comercial deverá gerar um número de sessão aleatório
    de 6 dígitos que não se repita nas últimas 100 comunicações.

Para um cliente SAT local, é fornecida uma implementação básica de numeração de
sessão que é encontrada na classe :class:`satcfe.base.NumeroSessaoMemoria`, que
é capaz de atender o requisito conforme descrito na ER SAT. Entretando, essa
implementação básica não é capaz (ainda) de persistir os números gerados.

Se for necessário utilizar um esquema de numeração de sessão diferente, basta
escrever um e passá-lo como argumento durante a criação do cliente local. Um
numerador de sessão é apenas um *callable* que, quando invocado, resulta no
próximo número de sessão a ser usado em uma função SAT. Por exemplo:

.. sourcecode:: python

    def meu_numerador():
        numero = ... # lógica diferente
        return numero

    cliente = ClienteSATLocal(
            BibliotecaSAT('/opt/fabricante/libsat.so'),
            codigo_ativacao='12345678'
            numerador_sessao=meu_numerador)

Para os clientes SATHub há um esquema de numeração de sessão mais robusto, já
que as requisições tem origem em caixas (pontos-de-venda) diferentes, o
requisito é resolvido de maneira a evitar colisões de numeração ou repetição de
numeração mesmo atendendo requisições concorrentes. Consulte a documentação do
`projeto SATHub <https://github.com/base4sistemas/sathub>`_ para os detalhes.

.. include:: references.rst
