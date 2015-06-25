
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


.. _lidando-com-as-respostas:

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


Sobre os Nomes das Funções
--------------------------

Os nomes das funções SAT neste projeto foram modificados dos nomes originais
para ficarem compatíveis com o estilo de código Python para nomes de métodos,
funções, etc. Mas a modificação é simples e segue uma regra fácil de converter
de cabeça. Por exemplo:

.. sourcecode:: text

    ComunicarCertificadoICPBRASIL  ->  comunicar_certificado_icpbrasil
    TesteFimAFim                   ->  teste_fim_a_fim

As palavras são separadas por um caracter de sublinha e o nome é todo convertido
para letras minúsculas.


Funções Básicas
===============

Estas são provavelmente as funções mais básicas da biblioteca SAT. São aquelas
funções que normalmente são as primeiras a serem invocadas quando se está
iniciando o procedimento de integração do SAT com o aplicativo comercial. Os
exemplos dizem respeito a qualquer cliente SAT, local ou via SATHub.

A maioria das funções SAT resulta em uma resposta padrão no estilo:

.. sourcecode:: text

    numeroSessao|EEEEE|mensagem|cod|mensagemSEFAZ

Portanto, os atributos ``numeroSessao``, ``EEEEE``, ``mensagem``, ``cod`` e
``mensagemSEFAZ`` estarão disponíveis na maioria das respostas, conforme visto
em :ref:`lidando-com-as-respostas`:


ConsutarSAT
-----------

A função ``ConsultarSAT`` (ER item 6.1.5) é usada para testar a comunicação com
o equipamento SAT. Se uso é simples e direto e se nenhuma exceção for lançada é
seguro acessar os atributos da resposta conforme esperado.

.. sourcecode:: python

    >>> resp = cliente.consultar_sat()
    >>> resp.mensagem
    u'SAT em Opera\xe7\xe3o'


ConsultarStatusOperacional
--------------------------

A função ``ConsultarStatusOperacional`` (ER item 6.1.7) retorna atributos que
mostram diversas informações a respeito do equipamento SAT. A resposta para
esta função é direta e simples, mas se você verificar a documentação da ER SAT
pode ficar confuso quanto aos atributos da resposta. A ER SAT diz que o retorno
da função é:

.. sourcecode:: text

    numeroSessao|EEEEE|mensagem|cod|mensagemSEFAZ|ConteudoRetorno

Entretando, a resposta **não possui** um atributo ``ConteudoRetorno``, por que
ele se expande em outros atributos que são documentados na ER SAT em uma tabela
separada. É como se o retorno fosse:

.. sourcecode:: text

    numeroSessao|EEEEE|mensagem|cod|mensagemSEFAZ|NSERIE|TIPO_LAN|LAN_IP|...

Por exemplo:

.. sourcecode:: python

    >>> resp = cliente.consultar_status_operacional()
    >>> resp.mensagem
    u'Resposta com Sucesso'

    >>> resp.NSERIE
    320008889

    >>> resp.STATUS_LAN
    u'CONECTADO'

    >>> resp.DH_ATUAL
    datetime.datetime(2015, 6, 25, 15, 26, 37)

ExtrairLogs
-----------

A função ``ExtrairLogs`` (ER item 6.1.12) retorna os registros de log do
equipamento SAT. A resposta para esta função possui duas particularidades:
primeiro que os registros de log podem ser automaticamente decodificados através
do método :meth:`~satcfe.resposta.extrairlogs.RespostaExtrairLogs.conteudo`;
segundo que o nome dado para este campo pela ER SAT fica muito longo e,
portanto, foi chamado apenas de ``arquivoLog``.

.. sourcecode:: python

    >>> resp = cliente.extrair_logs()
    >>> resp.mensagem
    u'Transfer\xeancia completa'

    >>> resp.arquivoLog
    u'MjAxNTA2MTIxNTAzNTB...jaGF2ZXMgZW5jb250cmFkbyBubyB0b2tlbg=='

    >>> print(resp.conteudo())
    20150612150350|SAT|info|nvl 2:token inicializado
    20150612150350|SAT|info|nvl 2:par de chaves encontrado no token
    20150612150350|SAT|info|nvl 2:certificado encontrado no token
    20150612150350|SAT-SEFAZ|info|nvl 2:(CFeStatus) acessado o webservice
    20150612150351|SAT|erro|nvl 0:(no error) marca inicio dos logs (01.00.00:48)
    20150612150351|SAT|info|nvl 1:Equipamento inicializado
    20150612150352|SEFAZ-SAT|info|nvl 2:(CFeStatus) status do equipamento recebido pela SEFAZ
    20150612150356|SAT|info|nvl 1:relogio sincronizado com sucesso
    20150612150356|SAT-SEFAZ|info|nvl 2:(CFeComandos) acessado o webservice
    20150612153407|SEFAZ-SAT|info|nvl 2:(CFeComandos) não existem comandos pendentes
    20150612153544|AC-SAT|info|nvl 2:recebida mensagem referente a função ConsultarSAT
    20150612153544|SAT-AC|info|nvl 2:enviando mensagem referente a função ConsultarSAT
    20150612153544|AC-SAT|info|nvl 2:recebida mensagem referente a função ConsultarStatusOperacional

Também é possível salvar o conteúdo decodificado dos registros de log através do
método :meth:`~satcfe.resposta.extrairlogs.RespostaExtrairLogs.salvar`:

.. sourcecode:: python

    >>> resp = cliente.extrair_logs()
    >>> resp.salvar()
    '/tmp/tmpNhVSHi-sat.log'


Numeração de Sessões
====================

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
escrever um e passar como argumento durante a criação do cliente local. Um
numerador de sessão é apenas um *callable* que, quando invocado, resulta no
próximo número de sessão a ser usado em uma função SAT. Por exemplo:

.. sourcecode:: python

    def meu_numerador():
        numero = ... # lógica diferente
        return numero

    cliente = ClienteSATLocal(
            DLLSAT(caminho='caminho/para/sat.dll',
                   convencao=constantes.WINDOWS_STDCALL),
            numerador_sessao=meu_numerador)

Para os clientes SATHub há um esquema de numeração de sessão mais robusto, já
que as requisições tem origem em caixas (pontos-de-venda) diferentes, o
requisito é resolvido de maneira a evitar colisões de numeração ou repetição de
numeração mesmo atendendo requisições concorrentes. Consulte a documentação do
`projeto SATHub <https://github.com/base4sistemas/sathub>`_ para os detalhes.
