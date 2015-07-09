
Respostas
=========

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
:ref:`basico-funcoes-basicas` e :ref:`basico-lidando-com-excecoes`.


Módulo ``satcfe.resposta.padrao``
=================================

.. automodule:: satcfe.resposta.padrao
    :members:
    :undoc-members:


Módulo ``satcfe.resposta.cancelarultimavenda``
==============================================

.. automodule:: satcfe.resposta.cancelarultimavenda
    :members:
    :undoc-members:


Módulo ``satcfe.resposta.consultarstatusoperacional``
=====================================================

.. automodule:: satcfe.resposta.consultarstatusoperacional
    :members:
    :undoc-members:


Módulo ``satcfe.resposta.enviardadosvenda``
===========================================

.. automodule:: satcfe.resposta.enviardadosvenda
    :members:
    :undoc-members:


Módulo ``satcfe.resposta.extrairlogs``
======================================

.. automodule:: satcfe.resposta.extrairlogs
    :members:
    :undoc-members:


Módulo ``satcfe.resposta.testefimafim``
=======================================

.. automodule:: satcfe.resposta.testefimafim
    :members:
    :undoc-members:


.. _`pipe`: http://unicode-table.com/en/007C/
