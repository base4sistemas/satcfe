
.. _infraestrutura-alertas:

Infraestrutura de Alertas
=========================

Implementa uma infraestrutura simplificada para checagem de alertas baseados
nas informações do status operacional do equipamanto SAT. O objetivo é alertar
o operador sobre situações potencialmente problemáticas a fim de que ele tome
providências a respeito. Esta infraestrutura permite que os problemas sejam
identificados de forma robusta, isolada e extensível. Assim, é possível que com
uma única consulta ao status operacional, um número variado de problemas possam
ser detectados e explanados com detalhes para o operador do sistema.

Cada alerta é implementado como uma subclasse de
:class:`~satcfe.alertas.AlertaOperacao` que sobrescreve os métodos
:meth:`~satcfe.alertas.AlertaOperacao.checar` e
:meth:`~satcfe.alertas.AlertaOperacao.mensagem`, responsáveis por identificar se
o alerta está ativo ou não e em contruir uma mensagem que descreva o status
daquele alerta da forma mais clara e detalhada possível, respectivamente.

A intenção é que a checagem dos alertas seja feita de forma automática, quando o
sistema (ponto-de-venda) for iniciado, no intuito de que o operador possa
resolver a tempo os alertas ativos. Para realizar uma checagem de alertas, basta
invocar a função :func:`~satcfe.alertas.checar`, passando como parâmetro uma
instância de um cliente SAT (:class:`~satcfe.clientelocal.ClienteSATLocal` ou
:class:`~satcfe.clientesathub.ClienteSATHub`):

.. sourcecode:: python

    sat = ClienteSATHub('10.0.0.200', port=5000)
    alertas = checar(sat)
    if alertas:
        # existem alertas ativos...
        faz_algo_a_respeito()

Este módulo fornece os seguintes alertas:

* **Documentos Pendentes** Detecta a existência de um ou mais CF-e-SAT
  pendentes de transmissão para a SEFAZ. Fornecido pela classe
  :class:`~satcfe.alertas.AlertaCFePendentes`.

* **Vencimento do Certificado** Detecta se o vencimento do certificado
  instalado no equipamento SAT está se aproximando (ou se já venceu). Fornecido
  pela classe :class:`~satcfe.alertas.AlertaVencimentoCertificado`.

* **Divergência de Horários** Detecta se a diferença entre o horário do sistema
  e do equipamento SAT é superior ao tolerado. Fornecido pela classe
  :class:`~satcfe.alertas.AlertaDivergenciaHorarios`.

É fácil implementar outros alertas se necessário, bastando implementar uma
subclasse de :class:`~satcfe.alertas.AlertaOperacao` e registrando a classe
através da função :func:`~satcfe.alertas.registrar`:

.. sourcecode:: python

    from satcfe.alertas import AlertaOperacao
    from satcfe.alertas import registrar

    class OutroAlerta(AlertaOperacao):

        def checar(self):
            if condicao:
                self._ativo = True
            return self._ativo

        def mensagem(self):
            if self._ativo:
                return 'Este alerta está ativo por uma razão.'
            return 'Este alerta não está ativo.'

    registrar(OutroAlerta)

Se você desenvolver algum alerta, considere compartilhar a sua implementação.
Caso você note que algum equipamento tenha resultado informações inesperadas,
fazendo com que algum alerta não funcione conforme o esperado, avise-nos,
preenchendo um
`relatório do problema <https://github.com/base4sistemas/satcfe/issues>`_.

Veja também a documentação da :ref:`api-infraestrutura-alertas`.
