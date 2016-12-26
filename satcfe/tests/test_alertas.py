# -*- coding: utf-8 -*-
#
# satcfe/tests/test_alertas.py
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

from datetime import date
from datetime import datetime

import pytest

from satcfe import alertas as modulo_alertas
from satcfe.alertas import AlertaOperacao
from satcfe.alertas import AlertaCFePendentes
from satcfe.alertas import AlertaVencimentoCertificado
from satcfe.alertas import AlertaDivergenciaHorarios
from satcfe.alertas import checar
from satcfe.alertas import registrar

from satcfe.resposta import RespostaConsultarStatusOperacional


@pytest.fixture(scope='module')
def resposta_normal():
    return RespostaConsultarStatusOperacional.analisar(
            u'061407|10000|Resposta com sucesso|||900004019|DHCP|'\
            u'010.000.000.108|30:40:03:19:19:40|255.255.255.000|'\
            u'010.000.000.001|010.000.000.001|010.000.000.001|'\
            u'CONECTADO|ALTO|4 GB|260 MB|20150912113321|01.00.00|00.06|'\
            u'35150908723218000186599000040190000723645630|'\
            u'00000000000000000000000000000000000000000000|'\
            u'00000000000000000000000000000000000000000000|'\
            u'20150912104828|20150912113039|20150708|20200708|0')


def test_registrar():
    class FooBar(AlertaOperacao):
        pass

    registrar(FooBar)
    assert FooBar in AlertaOperacao.alertas_registrados

    registrar(FooBar) # deve evitar que seja registrado duas vezes
    n = len([e for e in AlertaOperacao.alertas_registrados if e is FooBar])
    assert n == 1

    AlertaOperacao.alertas_registrados.remove(FooBar)


def test_checar_nenhum_alerta(resposta_normal, monkeypatch):

    class ClienteSATFalso(object):
        def consultar_status_operacional(self):
            return resposta_normal

    def mockreturn_today():
        return date(2015, 9, 12)

    def mockreturn_now():
        return datetime(2015, 9, 12, 11, 33, 21)

    monkeypatch.setattr(modulo_alertas, '_get_today', mockreturn_today)
    monkeypatch.setattr(modulo_alertas, '_get_now', mockreturn_now)

    alertas = checar(ClienteSATFalso())
    assert len(alertas) == 0


def test_alertaoperacao(resposta_normal):
    alerta = AlertaOperacao(resposta_normal)
    assert alerta.ativo == False

    with pytest.raises(NotImplementedError):
        alerta.checar()

    with pytest.raises(NotImplementedError):
        alerta.mensagem()


def test_alertacfependentes_nenhum_cfe_pendente(resposta_normal):
    alerta = AlertaCFePendentes(resposta_normal)
    assert alerta.checar() == False
    assert alerta.ativo == False
    assert alerta.pendentes == 0
    assert alerta.mensagem() == u'Nenhum CF-e-SAT pendente de transmissão. '\
            u'A data da última comunicação com a SEFAZ foi em 12/09/2015 11:30.'


def test_alertacfependentes_onze_cfe_pendentes():
    alerta = AlertaCFePendentes(RespostaConsultarStatusOperacional.analisar(
            u'061407|10000|Resposta com sucesso|||900004019|DHCP|'\
            u'010.000.000.108|30:40:03:19:19:40|255.255.255.000|'\
            u'010.000.000.001|010.000.000.001|010.000.000.001|'\
            u'CONECTADO|ALTO|4 GB|260 MB|20150912113321|01.00.00|00.06|'\
            u'35150908723218000186599000040190000723645630|'\
            u'35150908723218000186599000040190000723645630|'\
            u'35150908723218000186599000040190000628917342|'\
            u'20150912104828|20150912113039|20150708|20200708|0'))

    assert alerta.checar() == True
    assert alerta.ativo == True
    assert alerta.pendentes == 11
    assert alerta.mensagem() == u'Existem 11 cupons CF-e-SAT pendentes, '\
            u'que ainda não foram transmitidos para a SEFAZ. '\
            u'A data da última comunicação com a SEFAZ foi em 12/09/2015 11:30.'


def test_alertacfependentes_um_cfe_pendente():
    alerta = AlertaCFePendentes(RespostaConsultarStatusOperacional.analisar(
            u'061407|10000|Resposta com sucesso|||900004019|DHCP|'\
            u'010.000.000.108|30:40:03:19:19:40|255.255.255.000|'\
            u'010.000.000.001|010.000.000.001|010.000.000.001|'\
            u'CONECTADO|ALTO|4 GB|260 MB|20150912113321|01.00.00|00.06|'\
            u'35150908723218000186599000040190000723645630|'\
            u'35150908723218000186599000040190000723645630|'\
            u'35150908723218000186599000040190000723645630|'\
            u'20150912104828|20150912113039|20150708|20200708|0'))

    assert alerta.checar() == True
    assert alerta.ativo == True
    assert alerta.pendentes == 1
    assert alerta.mensagem() == u'Existe 1 cupom CF-e-SAT pendente, que ainda '\
            u'não foi transmitido para a SEFAZ. '\
            u'A data da última comunicação com a SEFAZ foi em 12/09/2015 11:30.'


def test_alertavencimentocertificado_normal(resposta_normal, monkeypatch):
    def mockreturn():
        return date(2016, 7, 20)

    monkeypatch.setattr(modulo_alertas, '_get_today', mockreturn)

    alerta = AlertaVencimentoCertificado(resposta_normal)
    assert alerta.checar() == False  # alerta não foi ativado
    assert alerta.ativo == False     # idem
    assert alerta.vencido == False
    assert alerta.dias_para_vencimento == 1449
    assert alerta.mensagem() == u'O certificado instalado está a 1449 dias do vencimento.'


def test_alertavencimentocertificado_prestes_a_vencer(resposta_normal, monkeypatch):
    def mockreturn():
        return date(2020, 5, 9)

    monkeypatch.setattr(modulo_alertas, '_get_today', mockreturn)

    alerta = AlertaVencimentoCertificado(resposta_normal)
    assert alerta.checar() == True  # alerta foi ativado
    assert alerta.ativo == True     # idem
    assert alerta.vencido == False  # próximo do vencimento, mas ainda não venceu
    assert alerta.dias_para_vencimento == 60
    assert alerta.mensagem() == u'O certificado instalado está a 60 dias do vencimento.'


def test_alertavencimentocertificado_vence_amanha(resposta_normal, monkeypatch):
    def mockreturn():
        return date(2020, 7, 7)

    monkeypatch.setattr(modulo_alertas, '_get_today', mockreturn)

    alerta = AlertaVencimentoCertificado(resposta_normal)
    assert alerta.checar() == True  # alerta foi ativado
    assert alerta.ativo == True     # idem
    assert alerta.vencido == False  # vence hoje, mas ainda não venceu
    assert alerta.dias_para_vencimento == 1
    assert alerta.mensagem() == u'O certificado instalado está a 1 dia do vencimento.'


def test_alertavencimentocertificado_vence_hoje(resposta_normal, monkeypatch):
    def mockreturn():
        return date(2020, 7, 8)

    monkeypatch.setattr(modulo_alertas, '_get_today', mockreturn)

    alerta = AlertaVencimentoCertificado(resposta_normal)
    assert alerta.checar() == True  # alerta foi ativado
    assert alerta.ativo == True     # idem
    assert alerta.vencido == False  # vence hoje, mas ainda não venceu
    assert alerta.dias_para_vencimento == 0
    assert alerta.mensagem() == u'O certificado instalado vence hoje!'


def test_alertavencimentocertificado_vencido(resposta_normal, monkeypatch):
    def mockreturn():
        return date(2020, 7, 9)

    monkeypatch.setattr(modulo_alertas, '_get_today', mockreturn)

    alerta = AlertaVencimentoCertificado(resposta_normal)
    assert alerta.checar() == True  # alerta foi ativado
    assert alerta.ativo == True     # idem
    assert alerta.vencido == True   # venceu
    assert alerta.dias_para_vencimento == 0
    assert alerta.mensagem() == u'O certificado instalado venceu!'


def test_alertadivergenciahorarios_sem_divergencia(resposta_normal, monkeypatch):
    def mockreturn():
        return datetime(2015, 9, 12, 11, 33, 21)

    monkeypatch.setattr(modulo_alertas, '_get_now', mockreturn)

    alerta = AlertaDivergenciaHorarios(resposta_normal)
    assert alerta.checar() == False  # alerta desativado
    assert alerta.ativo == False     # idem
    assert alerta.divergencia == 0   # horários idênticos
    assert alerta.mensagem() == u'Os horários são idênticos (sem divergência).'


def test_alertadivergenciahorarios_divergencia_negativa(resposta_normal, monkeypatch):
    def mockreturn():
        return datetime(2015, 9, 12, 11, 33) # note: desprezando segundos

    monkeypatch.setattr(modulo_alertas, '_get_now', mockreturn)

    alerta = AlertaDivergenciaHorarios(resposta_normal)
    assert alerta.checar() == False  # alerta desativado
    assert alerta.ativo == False     # idem
    assert alerta.divergencia == -21
    # (!) divergência negativa, computador atrasado em relação ao equip. SAT
    assert alerta.mensagem() == u'O horário do computador está atrasado em '\
            u'relação ao horário do equipamento SAT em 21 segundos, dentro '\
            u'do limite de tolerância de 1 hora.'


def test_alertadivergenciahorarios_divergencia_positiva(resposta_normal, monkeypatch):
    def mockreturn():
        return datetime(2015, 9, 12, 11, 33, 47)

    monkeypatch.setattr(modulo_alertas, '_get_now', mockreturn)

    alerta = AlertaDivergenciaHorarios(resposta_normal)
    assert alerta.checar() == False  # alerta desativado
    assert alerta.ativo == False     # idem
    assert alerta.divergencia == 26
    # (!) divergência negativa, computador atrasado em relação ao equip. SAT
    assert alerta.mensagem() == u'O horário do computador está adiantado em '\
            u'relação ao horário do equipamento SAT em 26 segundos, dentro '\
            u'do limite de tolerância de 1 hora.'


def test_alertadivergenciahorarios_divergencia_intoleravel(resposta_normal, monkeypatch):
    def mockreturn():
        # horário do computador adiantado em 1 hora e 1 segundo em relação
        # ao horário na resposta de consulta do status operacional
        return datetime(2015, 9, 12, 12, 33, 22)

    monkeypatch.setattr(modulo_alertas, '_get_now', mockreturn)

    alerta = AlertaDivergenciaHorarios(resposta_normal)
    assert alerta.checar() == True    # alerta ativado
    assert alerta.ativo == True       # idem
    assert alerta.divergencia == 3601 # 1 hora e 1 segundo de diferença
    assert alerta.mensagem() == u'Há uma divergência entre o horário do '\
            u'sistema e do equipamento SAT superior ao limite tolerável. '\
            u'O horário do sistema é 12/09/2015 12:33 e do equipamento SAT é '\
            u'12/09/2015 11:33 (tolerância de 1 hora, divergência de 1 hora e '\
            u'1 segundo).'


def test_alertadivergenciahorarios_divergencia_negativa_intoleravel(resposta_normal, monkeypatch):
    def mockreturn():
        # horário do computador atrasado em 1 hora e 1 segundo em relação
        # ao horário na resposta de consulta do status operacional
        return datetime(2015, 9, 12, 10, 33, 20)

    monkeypatch.setattr(modulo_alertas, '_get_now', mockreturn)

    alerta = AlertaDivergenciaHorarios(resposta_normal)
    assert alerta.checar() == True     # alerta ativado
    assert alerta.ativo == True        # idem
    assert alerta.divergencia == -3601 # 1 hora e 1 segundo de diferença (neg)
    assert alerta.mensagem() == u'Há uma divergência entre o horário do '\
            u'sistema e do equipamento SAT superior ao limite tolerável. '\
            u'O horário do sistema é 12/09/2015 10:33 e do equipamento SAT é '\
            u'12/09/2015 11:33 (tolerância de 1 hora, divergência de 1 hora e '\
            u'1 segundo).'
