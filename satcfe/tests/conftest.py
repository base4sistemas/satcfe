# -*- coding: utf-8 -*-
#
# satcfe/test/ft/conftest.py
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

from decimal import Decimal

import pytest

from satcomum import constantes

from satcfe import DLLSAT
from satcfe.clientelocal import ClienteSATLocal
from satcfe.entidades import CFeCancelamento
from satcfe.entidades import CFeVenda
from satcfe.entidades import Destinatario
from satcfe.entidades import LocalEntrega
from satcfe.entidades import Detalhamento
from satcfe.entidades import ProdutoServico
from satcfe.entidades import Imposto
from satcfe.entidades import ICMSSN102
from satcfe.entidades import PISSN
from satcfe.entidades import COFINSSN
from satcfe.entidades import MeioPagamento


def pytest_addoption(parser):

    parser.addoption('--cnpj-ac', action='store', default='08427847000169',
            help='CNPJ da empresa desenvolvedora da AC')

    parser.addoption('--codigo-ativacao', action='store', default='123456789',
            help='Codigo de ativacao configurado no equipamento SAT')

    parser.addoption('--assinatura-ac', action='store',
            default=constantes.ASSINATURA_AC_TESTE,
            help='Conteudo da assinatura da AC')

    parser.addoption('--numero-caixa', action='store', default='1',
            help='Numero do caixa de origem')

    parser.addoption('--ch-canc', action='store',
            default='CFe{}'.format('0' * 44),
            help='Chave do CF-e de venda que foi/sera cancelado')


@pytest.fixture(scope='module')
def clientesatlocal(request):
    caminho_dll = getattr(request.module, 'caminho_dll')
    convencao = getattr(request.module, 'convencao')
    funcoes = ClienteSATLocal(DLLSAT(caminho=caminho_dll, convencao=convencao))
    return funcoes


@pytest.fixture(scope='module')
def cfevenda(request):
    cfe = CFeVenda(
            CNPJ=request.config.getoption('--cnpj-ac'),
            signAC=request.config.getoption('--assinatura-ac'),
            numeroCaixa=request.config.getoption('--numero-caixa'),
            destinatario=Destinatario(
                    CPF='11122233396',
                    xNome=u'João de Teste'),
            entrega=LocalEntrega(
                    xLgr='Rua Armando Gulim',
                    nro='65',
                    xBairro=u'Parque Glória III',
                    xMun='Catanduva',
                    UF='SP'),
            detalhamentos=[
                    Detalhamento(
                            produto=ProdutoServico(
                                    cProd='123456',
                                    xProd='BORRACHA STAEDTLER pvc-free',
                                    CFOP='5102',
                                    uCom='UN',
                                    qCom=Decimal('1.0000'),
                                    vUnCom=Decimal('5.75'),
                                    indRegra='A'),
                            imposto=Imposto(
                                    icms=ICMSSN102(Orig='2', CSOSN='500'),
                                    pis=PISSN(CST='49'),
                                    cofins=COFINSSN(CST='49'))),
                ],
            pagamentos=[
                    MeioPagamento(
                            cMP=constantes.WA03_DINHEIRO,
                            vMP=Decimal('10.00')),
                ])
    return cfe


@pytest.fixture(scope='module')
def cfecanc(request):
    cfecanc = CFeCancelamento(
            chCanc=request.config.getoption('--ch-canc'),
            CNPJ=request.config.getoption('--cnpj-ac'),
            signAC=request.config.getoption('--assinatura-ac'),
            numeroCaixa=request.config.getoption('--numero-caixa'))
    return cfecanc
