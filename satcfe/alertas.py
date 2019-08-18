# -*- coding: utf-8 -*-
#
# satcfe/alertas.py
#
# Copyright 2015 Base4 Sistemas Ltda ME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from datetime import date
from datetime import datetime

from satcomum.ersat import ChaveCFeSAT

from .util import hms_humanizado

#
# (!) As funções `_get_now` e `_get_today` existem para possibilitar o
#     monkeypatch dos valores de data/hora, uma vez que pytest não pode definir
#     atributos de built-ins e tipos de extensão como `datetime.datetime`.
#


def _get_now():
    return datetime.now()


def _get_today():
    return date.today()


class AlertaOperacao(object):
    """Classe base para os alertas de operação."""

    alertas_registrados = []

    def __init__(self, resposta):
        self.resposta = resposta
        self._ativo = False

    @property
    def ativo(self):
        """Indica se o alerta está ou não ativo."""
        return self._ativo

    def checar(self):
        """Efetivamente checa se o alerta deve ou não ser ativado em função dos
        dados da resposta e de outras condições. As classes de alertas devem
        sobrescrever este método.

        :returns: Retorna ``True`` se o resultado da checagem indicar que este
            alerta está ativo (o mesmo que :attr:`ativo`).

        :rtype: bool
        """
        raise NotImplementedError()

    def mensagem(self):
        """Retorna uma mensagem amigável ao usuário, descrevendo da melhor
        forma possível a condição do alerta. As classes de alertas devem
        sobrescrever este método.

        :rtype: unicode
        """
        raise NotImplementedError()


class AlertaCFePendentes(AlertaOperacao):
    """Checa a existência de documentos CF-e-SAT pendentes no equipamento SAT,
    aguardando serem enviados à SEFAZ. Este alerta estará ativo se houver ao
    menos um documento CF-e-SAT pendente de transmissão no equipamento SAT.
    """

    def __init__(self, resposta):
        super(AlertaCFePendentes, self).__init__(resposta)
        self._pendentes = 0

    @property
    def pendentes(self):
        """Retorna o número de cupons pendentes de transmissão para a SEFAZ.

        :rtype: int
        """
        return self._pendentes

    def checar(self):
        if self._vazio(self.resposta.LISTA_INICIAL) \
                and self._vazio(self.resposta.LISTA_FINAL):
            # as chaves estão vazias (ou totalmente zeradas) o que significa
            # que não existem cupons pendentes;
            self._pendentes = 0
            self._ativo = False
        else:
            a = self._nCF(self.resposta.LISTA_INICIAL)
            b = self._nCF(self.resposta.LISTA_FINAL)
            self._pendentes = (a - b) + 1
            self._ativo = self._pendentes > 0

        return self._ativo

    def mensagem(self):
        if self.ativo:
            if self.pendentes == 1:
                frase = (
                        'Existe 1 cupom CF-e-SAT pendente, que ainda não foi '
                        'transmitido para a SEFAZ.'
                    )
            else:
                frase = (
                        'Existem {:d} cupons CF-e-SAT pendentes, que ainda '
                        'não foram transmitidos para a SEFAZ.'
                    ).format(self.pendentes)
        else:
            frase = 'Nenhum CF-e-SAT pendente de transmissão.'

        return '{} {}'.format(frase, self._ultima_comunicacao())

    def _vazio(self, chave_cfe):
        chave = chave_cfe.strip().strip('0')
        return len(chave) == 0

    def _nCF(self, chave_cfe):
        chave = ChaveCFeSAT('CFe{}'.format(chave_cfe))
        return int(chave.numero_cupom_fiscal)

    def _momento(self):
        if self.resposta.DH_ULTIMA.date() == _get_today():
            # a data da última comunicação com a SEFAZ foi hoje, resulta texto
            # contendo apenas horas e minutos
            texto = 'às {}'.format(self.resposta.DH_ULTIMA.strftime('%H:%M'))
        else:
            # resulta texto contendo a data e horário
            texto = (
                    'em {}'
                ).format(self.resposta.DH_ULTIMA.strftime('%d/%m/%Y %H:%M'))
        return texto

    def _ultima_comunicacao(self):
        return (
                'A data da última comunicação com a SEFAZ foi {}.'
            ).format(self._momento())


class AlertaVencimentoCertificado(AlertaOperacao):
    """Checa a data de vencimento do certificado instalado, ativando o alerta
    caso o vencimento esteja próximo. Para alterar o limite de proximidade do
    vencimento que ativa este alerta, modifique o atributo
    :attr:`vencimento_em_dias`, cujo padrão é de 60 dias.
    """

    vencimento_em_dias = 60
    """Determina o número de dias até o vencimento do certificado que irá
    ativar o alarte.
    """

    def __init__(self, resposta):
        super(AlertaVencimentoCertificado, self).__init__(resposta)
        self._delta = None  # datetime.timedelta

    @property
    def vencido(self):
        """Indica se o certificado instalado no equipamento está vencido.

        :rtype: bool
        """
        return self._delta.days < 0

    @property
    def dias_para_vencimento(self):
        """O número de dias que restam até o vencimento do certificado
        instalado. Se o certificado já estiver vencido, retornará zero.

        :rtype: int
        """
        if self.vencido:
            return 0
        return self._delta.days

    def checar(self):
        self._delta = self.resposta.CERT_VENCIMENTO - _get_today()
        self._ativo = self.dias_para_vencimento <= self.vencimento_em_dias
        return self._ativo

    def mensagem(self):
        if self.vencido:
            return 'O certificado instalado venceu!'

        num_dias = self.dias_para_vencimento
        if num_dias == 0:
            texto = 'O certificado instalado vence hoje!'
        else:
            palavra_dia = 'dia' if num_dias == 1 else 'dias'
            texto = (
                    'O certificado instalado está a {} {} do vencimento.'
                ).format(num_dias, palavra_dia)
        return texto


class AlertaDivergenciaHorarios(AlertaOperacao):
    """Checa o horário do equipamento SAT em relação ao horário atual, emitindo
    um alerta caso exista uma divergência entre os horáros superior a 3600
    segundos (1 hora). Para alterar o limite de tolerância que ativará este
    alerta, modifique o atributo :attr:`tolerancia_em_segundos`.

    .. note::

        O limite de tolerância para este alerta, de uma hora, é uma herança
        do **Requisito XVII** do PAF-ECF, *Sincronismo entre data e hora do
        registro com data e hora do Cupom Fiscal*, embora SAT-CF-e não tenha
        qualquer relação com o PAF-ECF.

    """

    tolerancia_em_segundos = 3600  # 1h
    """Limite de tolerância, em segundos, para ativar o alerta."""

    def __init__(self, resposta):
        super(AlertaDivergenciaHorarios, self).__init__(resposta)
        self._dataref = _get_now()
        self._delta = None  # datetime.timedelta

    @property
    def divergencia(self):
        """Divergência em segundos entre o horário local (do computador) e o
        horário do equipamento SAT, segundo a resposta de consulta ao status
        operacional. Precisão de microsegundos é desprezada.

        Uma **divergência negativa** indica que o horário local (do computador)
        está atrasado em relação ao relógio do equipamento SAT. Para saber se a
        divergência de horarários ultrapassou o limite de tolerância, consulte
        o atributo :attr:`~AlertaOperacao.ativo`.

        :rtype: int
        """
        return int(self._delta.total_seconds())

    def checar(self):
        self._delta = self._dataref - self.resposta.DH_ATUAL
        self._ativo = abs(self.divergencia) > self.tolerancia_em_segundos
        return self._ativo

    def mensagem(self):
        if self.divergencia == 0:
            frase = 'Os horários são idênticos (sem divergência).'
        else:
            if self.ativo:
                fmt = '%d/%m/%Y %H:%M'
                frase = (
                        'Há uma divergência entre o horário do sistema e do '
                        'equipamento SAT superior ao limite tolerável. O '
                        'horário do sistema é {0} e do equipamento SAT é {1} '
                        '(tolerância de {2}, divergência de {3}).'
                    ).format(
                        self._dataref.strftime(fmt),
                        self.resposta.DH_ATUAL.strftime(fmt),
                        hms_humanizado(self.tolerancia_em_segundos),
                        hms_humanizado(abs(self.divergencia)))
            else:
                situacao = 'atrasado' if self.divergencia < 0 else 'adiantado'
                frase = (
                        'O horário do computador está {0} em relação ao '
                        'horário do equipamento SAT em {1}, dentro do limite '
                        'de tolerância de {2}.'
                    ).format(
                        situacao,
                        hms_humanizado(abs(self.divergencia)),
                        hms_humanizado(self.tolerancia_em_segundos))
        return frase


def registrar(classe_alerta):
    """Registra uma classe de alerta (subclasse de :class:`AlertaOperacao`).
    Para mais detalhes, veja :func:`checar`.
    """
    if classe_alerta not in AlertaOperacao.alertas_registrados:
        AlertaOperacao.alertas_registrados.append(classe_alerta)


def checar(cliente_sat):
    """Checa em sequência os alertas registrados (veja :func:`registrar`)
    contra os dados da consulta ao status operacional do equipamento SAT. Este
    método irá então resultar em uma lista dos alertas ativos.

    :param cliente_sat: Uma instância de
        :class:`satcfe.clientelocal.ClienteSATLocal` ou
        :class:`satcfe.clientesathub.ClienteSATHub` onde será invocado o
        método para consulta ao status operacional do equipamento SAT.

    :rtype: list
    """
    resposta = cliente_sat.consultar_status_operacional()
    alertas = []
    for classe_alerta in AlertaOperacao.alertas_registrados:
        alerta = classe_alerta(resposta)
        if alerta.checar():
            alertas.append(alerta)
    return alertas


registrar(AlertaCFePendentes)
registrar(AlertaVencimentoCertificado)
registrar(AlertaDivergenciaHorarios)
