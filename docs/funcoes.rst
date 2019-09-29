
Funções SAT
===========

O acesso às funções SAT se dá através de uma biblioteca que é fornecida pelo
fabricante do equipamento SAT. Este projeto abstrai o acesso à essa biblioteca
tornando possível acessar um equipamento SAT conectado no computador local ou
compartilhar um equipamento SAT entre dois ou mais computadores, acessando-o
remotamente via API RESTful.

Se você estiver acessando um equipamento SAT conectado ao computador local,
então deverá usar um :class:`~satcfe.clientelocal.ClienteSATLocal`, cuja
configuração já foi discutida em :ref:`configuracao-basica`.

Se estiver compartilhando um equipamento SAT, então deverá usar
um :class:`~satcfe.clientesathub.ClienteSATHub`, cuja configuração também já
foi demonstrada.

.. note::

    Instalar um servidor `SATHub`_ está fora do escopo desta documentação.
    Consulte a `documentação do projeto SATHub <http://sathub.readthedocs.io/>`_
    para saber como instalar e configurar um servidor SATHub em desenvolvimento
    ou em produção.

Uma vez configurado o cliente SAT, basta invocar os métodos correspodentes às
funções SAT, que serão demonstradas mais adiante nesta documentação.

.. note::

    **Sobre os nomes dos métodos** Os nomes das funções SAT neste projeto foram
    modificados dos nomes originais para ficarem compatíveis com o estilo de
    código Python para nomes de métodos, funções, etc. Mas a modificação é
    simples e segue uma regra fácil de converter de cabeça. Por exemplo::

        ComunicarCertificadoICPBRASIL  ->  comunicar_certificado_icpbrasil
        TesteFimAFim                   ->  teste_fim_a_fim

    As palavras são separadas por um caracter de sublinha e o nome é todo
    convertido para letras minúsculas.


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


.. _lidando-com-excecoes:

Lidando com Exceções
--------------------

Quando uma função é invocada, seja através de um
:class:`~satcfe.clientelocal.ClienteSATLocal` ou
:class:`~satcfe.clientesathub.ClienteSATHub`, existem duas exceções principais
que podem ocorrer: :exc:`~satcfe.excecoes.ErroRespostaSATInvalida` ou
:exc:`~satcfe.excecoes.ExcecaoRespostaSAT`.

Quando a exceção ``ErroRespostaSATInvalida`` é levantada, significa que a
resposta retornada pelo equipamento SAT não está em conformidade com a ER SAT,
geralmente por que a biblioteca resultou em uma sequência que não possui os
elementos que deveriam estar presentes, seja uma resposta de sucesso na execução
da função ou não.

Por outro lado será comum lidar com ``ExcecaoRespostaSAT``. Esta exceção indica
que a comunicação entre a AC e o equipamento correu bem mas execução da função
não obteve êxito. É o caso quando invocar a função ``ConsultarSAT`` e o
equipamento estiver ocupado processando uma outra coisa; a exceção poderá
indicar o erro, já que ela contém uma resposta:

.. sourcecode:: python

    >>> # suponha que o equipamento SAT está ocupado
    >>> import sys
    >>> resposta = cliente.consultar_sat()
    Traceback (most recent call last):
     ...
    ExcecaoRespostaSAT: ConsultarSAT, numeroSessao=567192, EEEEE='08098', mensagem="SAT em processamento. Tente novamente.", cod="", mensagemSEFAZ=""

    >>> resposta = sys.last_value
    >>> resposta.mensagem
    'SAT em processamento. Tente novamente.'

    >>> resposta.EEEEE
    '08098'

    >>> resposta.numeroSessao
    567192

O truque acima foi obter o objeto da exceção levantada de ``sys.last_value``,
que é similar ao que deveria fazer no bloco de tratamento da exceção
``ExcecaoRespostaSAT``, por exemplo:

.. sourcecode:: python

    try:
        resposta = cliente.consultar_sat()
        # faz algo com a resposta...

    except ErroRespostaSATInvalida as ex_resp_invalida:
        # exibe o erro para o operador...
        break

    except ExcecaoRespostaSAT as ex_resposta:
        resposta = ex_resposta.resposta
        if resposta.EEEEE == '08098':
            # o equipamento SAT está ocupado
            # pergunta ao operador de caixa se quer tentar novamente...
            pass

Obviamente, muita coisa pode dar errado entre o aplicativo comercial e a SEFAZ,
então utilize a regra básica de tratamento de exceções recomendada, mantendo uma
cláusula ``except`` de *fallback*, por exemplo:

.. sourcecode:: python

    try:
        resposta = cliente.enviar_dados_venda(cfe)
        # faz algo com a resposta aqui

    except ErroRespostaSATInvalida as ex_sat_invalida:
        # o equipamento retornou uma resposta que não faz sentido;
        # loga, e lança novamente ou lida de alguma maneira
        pass

    except ExcecaoRespostaSAT as ex_resposta:
        # o equipamento retornou mas a função não foi bem sucedida;
        # analise 'EEEEE' para decidir o que pode ser feito
        pass

    except Exception as ex:
        # uma outra coisa aconteceu
        pass


.. warning::

    Evite silenciar (ignorar) exceções. Se não sabe o porquê, veja o tópico
    sobre `Tratamento de Exceções`_ no tutorial de Python.


.. _funcoes-basicas-e-de-consulta:

Funções Básicas e de Consulta
-----------------------------

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


ConsultarSAT
~~~~~~~~~~~~

A função ``ConsultarSAT`` (ER item 6.1.5, método
:meth:`~satcfe.clientelocal.ClienteSATLocal.consultar_sat`) é usada para testar
a comunicação com o equipamento SAT. Seu uso é simples e direto e, se nenhuma
exceção for lançada, é seguro acessar os atributos da resposta conforme
esperado.

.. sourcecode:: python

    >>> resp = cliente.consultar_sat()
    >>> resp.mensagem
    'SAT em Operação'


ConsultarStatusOperacional
~~~~~~~~~~~~~~~~~~~~~~~~~~

A função ``ConsultarStatusOperacional`` (ER item 6.1.7, método
:meth:`~satcfe.clientelocal.ClienteSATLocal.consultar_status_operacional`)
retorna atributos que mostram diversas informações a respeito do equipamento
SAT. A resposta para esta função é direta e simples, mas se você verificar a
documentação da ER SAT pode ficar confuso quanto aos atributos da resposta. A ER
SAT diz que o retorno da função é:

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
    'Resposta com Sucesso'

    >>> resp.NSERIE
    320008889

    >>> resp.STATUS_LAN
    'CONECTADO'

    >>> resp.DH_ATUAL
    datetime.datetime(2015, 6, 25, 15, 26, 37)


ConsultarNumeroSessao
~~~~~~~~~~~~~~~~~~~~~

A função ``ConsultarNumeroSessao`` (ER item 6.1.8, método
:meth:`~satcfe.clientelocal.ClienteSATLocal.consultar_numero_sessao`) permite
consultar a resposta para sessão executada anteriormente. Essa função é especial
no sentido de que sua resposta será a resposta para a função executada na sessão
que está sendo consultada.

Por exemplo, suponha que a última sessão executada seja um cancelamento, com
número de sessão ``555810``. Se este número de sessão for consultado, a resposta
será a resposta de um cancelamento, resultando em uma instância de
:class:`~satcfe.resposta.cancelarultimavenda.RespostaCancelarUltimaVenda`.

.. sourcecode:: python

    >>> resp = cliente.consultar_numero_sessao(555810)
    >>> resp
    <satcfe.resposta.cancelarultimavenda.RespostaCancelarUltimaVenda at 0x7ffb171e02d0>

.. note::

    A documentação não deixa claro, mas os testes executados contra três
    equipamentos SAT de fabricantes diferentes se comportaram da seguinte
    maneira:

    * Apenas a sessão executada imediatamente antes é que será considerada, ou
      seja, não adianta especificar uma sessão que tenha sido processada há
      duas ou mais sessões anteriores;

    * Se a última sessão executada for de uma função de consulta de número de
      sessão (algo como uma *meta consulta*), a função também irá falhar.


ConsultarUltimaSessaoFiscal
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A função ``ConsultarUltimaSessaoFiscal`` (ER item 6.1.16, método
:meth:`~satcfe.clientelocal.ClienteSATLocal.consultar_ultima_sessao_fiscal`),
como o nome sugere, resulta na resposta da última sessão fiscal executada pelo
equipamento SAT. É considerada uma "sessão fiscal" um comando de venda ou de
cancelamento de venda, respectivamente
:meth:`~satcfe.clientelocal.ClienteSATLocal.enviar_dados_venda` ou
:meth:`~satcfe.clientelocal.ClienteSATLocal.cancelar_ultima_venda`, e suas
respostas,
:class:`~satcfe.resposta.enviardadosvenda.RespostaEnviarDadosVenda` ou
:class:`~satcfe.resposta.cancelarultimavenda.RespostaCancelarUltimaVenda`.

Por exemplo, suponha que a última sessão fiscal executada pelo equipamento SAT
tenha sido um comando de venda:

.. sourcecode:: python

    >>> resp = cliente.consultar_ultima_sessao_fiscal()
    >>> resp
    <satcfe.resposta.enviardadosvenda.RespostaEnviarDadosVenda at 0x7f1817971950>

Conforme descrito na especificação de requisitos do SAT, se o equipamento ainda
não tiver executado nenhum comando fiscal (venda ou cancelamento), a resposta
deverá indicar o código de retorno ``EEEEE`` igual a ``19003`` que significa
"Não existe sessão fiscal".

.. sourcecode:: python

    >>> try:
    ...     # suponha que o equipamento nunca tenha executado um comando fiscal
    ...     resp = cliente.consultar_ultima_sessao_fiscal()
    ... except ExcecaoRespostaSAT as err:
    ...     pass
    ...

    >>> err.resposta.EEEEE
    '19003'

    >>> err.resposta.mensagem
    'Não existe sessão fiscal'

Veja mais detalhes em :ref:`venda-e-cancelamento`.

.. versionadded:: 2.0


ExtrairLogs
~~~~~~~~~~~

A função ``ExtrairLogs`` (ER item 6.1.12, método
:meth:`~satcfe.clientelocal.ClienteSATLocal.extrair_logs`) retorna os registros
de log do equipamento SAT. A resposta para esta função possui duas
particularidades: primeiro que os registros de log podem ser automaticamente
decodificados através do método
:meth:`~satcfe.resposta.extrairlogs.RespostaExtrairLogs.conteudo`; segundo que o
nome dado para este campo pela ER SAT fica muito longo e, portanto, foi chamado
apenas de ``arquivoLog``.

.. sourcecode:: python

    >>> resp = cliente.extrair_logs()
    >>> resp.mensagem
    'Transferência completa'

    >>> resp.arquivoLog
    'MjAxNTA2MTIxNTAzNTB...jaGF2ZXMgZW5jb250cmFkbyBubyB0b2tlbg=='

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


.. _funcoes-de-configuracao-modificacao:

Funções de Configuração/Modificação
-----------------------------------

As funções a seguir são utilizadas para configurar o equipamento SAT ou acabam
por modificar certos registros de informações que ficam permanentemente gravadas
no equipamento.


.. _funcao-ativarsat:

AtivarSAT
~~~~~~~~~

A função ``AtivarSAT`` (ER item 6.1.1, método
:meth:`~satcfe.clientelocal.ClienteSATLocal.ativar_sat`) é usada para realizar a
ativação do equipamento SAT tornando-o apto para realizar vendas e
cancelamentos. Para maiores detalhes consulte o item 2.1.1 da ER SAT.

.. sourcecode:: python

    >>> from satcomum import constantes
    >>> from satcomum import br
    >>> cnpj_contribuinte = '12345678000199'
    >>> resp = cliente.ativar_sat(constantes.CERTIFICADO_ACSAT_SEFAZ,
    ...         cnpj_contribuinte, br.codigo_ibge_uf('SP'))
    ...
    >>> resp.csr()
    '-----BEGIN CERTIFICATE REQUEST-----
    MIIBnTCCAQYCAQAwXTELMAkGA1UEBhMCU0cxETAPBgNVBAoTCE0yQ3J5cHRvMRIw
     ...
    9rsQkRc9Urv9mRBIsredGnYECNeRaK5R1yzpOowninXC
    -----END CERTIFICATE REQUEST-----

.. attention::

    É nesta função que é definido o **Código de Ativação** do equipamento SAT.

    Este código é uma senha que é enviada ao equipamento a cada função
    executada. **Se o equipamento ainda não estiver ativo**, esta deverá ser a
    primeira função a ser executada e o código de ativação
    :ref:`informado ao instanciar o cliente SAT <configuracao-basica>` é o
    código que será usado para definir o código de ativação do equipamento.

    Veja :ref:`funcao-trocarcodigodeativacao` para outros detalhes.


ComunicarCertificadoICPBRASIL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A função ``ComunicarCertificadoICPBRASIL`` (ER item 6.1.2, método
:meth:`~satcfe.clientelocal.ClienteSATLocal.comunicar_certificado_icpbrasil`) é
complementar à função ``AtivarSAT`` e é usada para enviar à SEFAZ o conteúdo do
certificado emitido pela `ICP Brasil`_.

.. sourcecode:: python

    >>> with open('certificado.pem', 'r') as f:
    ...     certificado = f.read()
    ...
    >>> resp = cliente.comunicar_certificado_icpbrasil(certificado)
    >>> resp.mensagem
    'Certificado transmitido com sucesso'


ConfigurarInterfaceDeRede
~~~~~~~~~~~~~~~~~~~~~~~~~

A função ``ConfigurarInterfaceDeRede`` (ER item 6.1.9, método
:meth:`~satcfe.clientelocal.ClienteSATLocal.configurar_interface_de_rede`) é
utilizada para configurar o acesso à rede para que o equipamento SAT possa ter
acesso à internet. Os parâmetros de configuração são informados através de uma
instância da classe :class:`~satcfe.rede.ConfiguracaoRede`.

.. note::

    Se o equipamento ainda não tiver sido ativado, o código de ativação ao
    invocar esta função deverá ser ``00000000`` (oito dígitos zero).

.. sourcecode:: python

    >>> from satcomum import constantes
    >>> from satcfe.rede import ConfiguracaoRede
    >>> rede = ConfiguracaoRede(
    ...         tipoInter=constantes.REDE_TIPOINTER_ETHE,
    ...         tipoLan=constantes.REDE_TIPOLAN_DHCP)
    ...
    >>> resp = cliente.configurar_interface_de_rede(rede)
    >>> resp.mensagem
    'Rede configurada com sucesso'


.. _funcao-associarassinatura:

AssociarAssinatura
~~~~~~~~~~~~~~~~~~

A função ``AssociarAssinatura`` (ER item 6.1.10, método
:meth:`~satcfe.clientelocal.ClienteSATLocal.associar_assinatura`) é usada para
vincular a assinatura do aplicativo comercial ao equipamento SAT. Essa mesma
assinatura é utilizada no atributo ``signAC`` ao realizar
:ref:`vendas <criando-um-cfe-de-venda>` e
`cancelamentos <criando-um-cfe-de-cancelamento>`_.

.. sourcecode:: python

    >>> resp = cliente.associar_assinatura(
    ...         '1111111111111122222222222222',
    ...         'RVlHYkYzcytsZFdiekM4SExmNFVLaXlaZF...')
    ...
    >>> resp.mensagem
    'Assinatura do AC registrada'

O primeiro argumento, ``sequencia_cnpj``, deve ser uma string de 28 digitos
contendo o CNPJ da software house e o CNPJ do estabelecimento contribuinte.

O segundo argumento, ``assinatura_ac``, deve ser uma sequência de 344
caracteres, contendo o `hash SHA256 <https://pt.wikipedia.org/wiki/SHA-2>`_
codificado em `Base64 <https://pt.wikipedia.org/wiki/Base64>`_.

.. admonition:: Gerando a Assinatura  AC

    Este exemplo demonstra como gerar a assinatura em um terminal Linux,
    usando `OpenSSL <https://www.openssl.org/>`_ e a parte privada da sua
    chave RSA (assumindo que a chave privada tenha sido extraída do e-CNPJ ou
    arquivo ``pfx`` do certificado digital da software house em um arquivo
    chamado ``~/.keys/private.pem``):

    .. sourcecode:: shell

        $ echo -n 1111111111111122222222222222 | \
            openssl dgst -sha256 -sign ~/.keys/private.pem | \
            openssl enc -base64 -e

    A saída desse comando é o valor que deverá ser informado no argumento
    ``assinatura_ac``.

.. tip::

    Consulte o item 2.1.3 da ER SAT para conhecer a especificação.


AtualizarSoftwareSAT
~~~~~~~~~~~~~~~~~~~~

A função ``AtualizarSoftwareSAT`` (ER item 6.1.11, método
:meth:`~satcfe.clientelocal.ClienteSATLocal.atualizar_software_sat`) é usada
para atualização do software básico do equipamento SAT.

.. sourcecode:: python

    >>> resp = cliente.atualizar_software_sat()
    >>> resp.mensagem
    'Software atualizado com sucesso'


BloquearSAT
~~~~~~~~~~~

A função ``BloquearSAT`` (ER item 6.1.13, método
:meth:`~satcfe.clientelocal.ClienteSATLocal.bloquear_sat`) é usada para
realizar o bloqueio operacional do equipamento SAT.

.. sourcecode:: python

    >>> resp = cliente.bloquear_sat()
    >>> resp.mensagem
    'Equipamento SAT bloqueado com sucesso'


DesbloquearSAT
~~~~~~~~~~~~~~

A função ``DesbloquearSAT`` (ER item 6.1.14, método
:meth:`~satcfe.clientelocal.ClienteSATLocal.desbloquear_sat`) é usada para
realizar o desbloqueio operacional do equipamento SAT.

.. sourcecode:: python

    >>> resp = cliente.desbloquear_sat()
    >>> resp.mensagem
    'Equipamento SAT desbloqueado com sucesso'


.. _funcao-trocarcodigodeativacao:

TrocarCodigoDeAtivacao
~~~~~~~~~~~~~~~~~~~~~~

A função ``TrocarCodigoDeAtivacao`` (ER item 6.1.15, método
:meth:`~satcfe.clientelocal.ClienteSATLocal.trocar_codigo_de_ativacao`) é
usada, como o nome sugere, para trocar o código de ativação do equipamento SAT
que, na prática, é uma senha que é enviada ao equipamento SAT a cada comando.

.. sourcecode:: python

    >>> novo_codigo = 's3cr3t0'
    >>> resp = cliente.trocar_codigo_de_ativacao(novo_codigo)
    >>> resp.mensagem
    'Código de ativação alterado com sucesso'

Todo equipamento SAT possui um **código de ativação de emergência**, que
acompanha o produto (pode estar escrito no manual do usuário ou em alguma
etiqueta na embalagem ou no próprio equipamento). Caso o código de ativação seja
perdido, é possível trocar o código de ativação usando o código de ativação de
emergência:

.. sourcecode:: python

    >>> from satcomum import constantes
    >>> novo_codigo = 's3cr3t0'
    >>> resp = cliente.trocar_codigo_de_ativacao(
    ...         novo_codigo,
    ...         opcao=constantes.CODIGO_ATIVACAO_EMERGENCIA,
    ...         codigo_emergencia='d35c0nh3c1d0')
    ...
    >>> resp.mensagem
    'Código de ativação alterado com sucesso'

Veja :ref:`funcao-ativarsat` para mais informações.


.. include:: references.rst
