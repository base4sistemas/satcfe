
.. _documentacao-da-api:

Documentação da API
===================

Os módulos :mod:`satcfe.base`, :mod:`satcfe.clientelocal` e
:mod:`satcfe.clientesathub` são a fundação para comunicação com o equipamento
SAT conectado à máquina local ou à um equipamento SAT compartilhado através
de um servidor `SATHub`_.

.. toctree::
    :maxdepth: 1

    apidoc/base.rst
    apidoc/clientelocal
    apidoc/clientesathub
    apidoc/entidades
    apidoc/excecoes
    apidoc/rede
    apidoc/util


Respostas das Funções SAT
-------------------------

As funções da biblioteca SAT retornam sequências de texto que contém os
atributos da resposta. Os atributos estão separados entre si por um caracter
de *linha vertical*, ou `pipe`_.

.. sourcecode:: text

    567102|09000|Emitido com sucesso||

As classes :class:`~satcfe.clientelocal.ClienteSATLocal` e
:class:`~satcfe.clientesathub.ClienteSATHub` resultam em respostas que são
objetos Python que facilitam o acesso à esses atributos, mesmo quando a
comunicação com o equipamento foi bem sucedida mas a resposta indica um erro.
Veja como lidar com algumas das respostas mais básicas em
:ref:`funcoes-basicas-e-de-consulta` e :ref:`lidando-com-excecoes`.

.. toctree::
    :maxdepth: 1

    apidoc/resposta/padrao
    apidoc/resposta/ativarsat
    apidoc/resposta/cancelarultimavenda
    apidoc/resposta/consultarnumerosessao
    apidoc/resposta/consultarstatusoperacional
    apidoc/resposta/enviardadosvenda
    apidoc/resposta/extrairlogs
    apidoc/resposta/testefimafim

.. include:: references.rst


Infraestrutura de Alertas
-------------------------

Fornece um mecanismo simples e robusto para checagem de potenciais problemas de
operação com base no status operacional do equipamento SAT.

.. toctree::
    :maxdepth: 1

    apidoc/alertas
