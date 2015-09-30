# -*- coding: utf-8 -*-
#
# satcfe/tests/conftest.py
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

from unidecode import unidecode

from satcomum import constantes

from satcfe.base import BibliotecaSAT
from satcfe.clientelocal import ClienteSATLocal
from satcfe.entidades import CFeCancelamento
from satcfe.entidades import CFeVenda
from satcfe.entidades import Destinatario
from satcfe.entidades import Emitente
from satcfe.entidades import LocalEntrega
from satcfe.entidades import Detalhamento
from satcfe.entidades import ProdutoServico
from satcfe.entidades import Imposto
from satcfe.entidades import ICMSSN102
from satcfe.entidades import PISSN
from satcfe.entidades import COFINSSN
from satcfe.entidades import MeioPagamento


def pytest_addoption(parser):

    parser.addoption('--cnpj-ac',
            action='store',
            default='16716114000172',
            help='CNPJ da empresa desenvolvedora da AC (apenas digitos)')

    parser.addoption('--emitente-cnpj',
            action='store',
            default='08723218000186',
            help='CNPJ do estabelecimento emitente (apenas digitos)')

    parser.addoption('--emitente-ie',
            action='store',
            default='149626224113',
            help='Inscricao estadual do emitente (apenas digitos)')

    parser.addoption('--emitente-im',
            action='store',
            default='123123',
            help='Inscricao municipal do emitente (apenas digitos)')

    parser.addoption('--emitente-uf',
            action='store',
            default='SP',
            help='Sigla da unidade federativa do estabelecimento emitente')

    parser.addoption('--emitente-issqn-regime',
            action='store',
            default='3',
            help='Regime especial de tributacao do ISSQN ({}) do emitente, '
                    'em casos de testes de emissao de venda e/ou '
                    'cancelamento'.format(_valores_possiveis(
                            constantes.C15_CREGTRIBISSQN_EMIT)))

    parser.addoption('--emitente-issqn-rateio',
            action='store',
            default='N',
            help='Indicador de rateio do desconto sobre o subtotal para '
                    'produtos tributados no ISSQN ({}) do emitente, '
                    'em casos de testes de emissao de venda e/ou '
                    'cancelamento'.format(_valores_possiveis(
                            constantes.C16_INDRATISSQN_EMIT)))

    parser.addoption('--codigo-ativacao',
            action='store',
            default='12345678',
            help='Codigo de ativacao configurado no equipamento SAT')

    parser.addoption('--assinatura-ac',
            action='store',
            default=constantes.ASSINATURA_AC_TESTE,
            help='Conteudo da assinatura da AC')

    parser.addoption('--numero-caixa',
            action='store',
            default=1,
            type=int,
            help='Numero do caixa de origem')

    parser.addoption('--lib-caminho',
            action='store',
            default='sat.dll',
            help='Caminho para a biblioteca SAT')

    parser.addoption('--lib-convencao',
            action='store',
            choices=[constantes.STANDARD_C, constantes.WINDOWS_STDCALL],
            default=constantes.STANDARD_C,
            type=int,
            help='Convencao de chamada para a biblioteca SAT '
                    '({})'.format(_valores_possiveis(
                            constantes.CONVENCOES_CHAMADA)))

    # TODO: implementar testes para acesso compartilhado ao equipamento SAT
    # --sathub-host     127.0.0.1
    # --sathub-port     8080
    # --sathub-baseurl  /hub/v1/
    # --sathub-username
    # --sathub-password

    # opções para ignorar funções SAT específicas
    parser.addoption('--skip-funcoes-sat',
            action='store_true',
            help='Ignora testes de todas as funcoes SAT evitando qualquer '
                    'acesso ao equipamento')

    parser.addoption('--skip-ativarsat',
            action='store_true',
            help='Ignora funcao `AtivarSAT`')

    parser.addoption('--skip-comunicarcertificadoicpbrasil',
            action='store_true',
            help='Ignora funcao `ComunicarCertificadoICPBRASIL`')

    parser.addoption('--skip-enviardadosvenda',
            action='store_true',
            help='Ignora funcao `EnviarDadosVenda`')

    parser.addoption('--skip-cancelarultimavenda',
            action='store_true',
            help='Ignora funcao `CancelarUltimaVenda`')

    parser.addoption('--skip-consultarsat',
            action='store_true',
            help='Ignora funcao `ConsultarSAT`')

    parser.addoption('--skip-testefimafim',
            action='store_true',
            help='Ignora funcao `TesteFimAFim`')

    parser.addoption('--skip-consultarstatusoperacional',
            action='store_true',
            help='Ignora funcao `ConsultarStatusOperacional`')

    parser.addoption('--skip-consultarnumerosessao',
            action='store_true',
            help='Ignora funcao `ConsultarNumeroSessao`')

    parser.addoption('--skip-configurarinterfacederede',
            action='store_true',
            help='Ignora funcao `ConfigurarInterfaceDeRede`')

    parser.addoption('--skip-associarassinatura',
            action='store_true',
            help='Ignora funcao `AssociarAssinatura`')

    parser.addoption('--skip-atualizarsoftwaresat',
            action='store_true',
            help='Ignora funcao `AtualizarSoftwareSAT`')

    parser.addoption('--skip-extrairlogs',
            action='store_true',
            help='Ignora funcao `ExtrairLogs`')

    parser.addoption('--skip-bloquearsat',
            action='store_true',
            help='Ignora funcao `BloquearSAT`')

    parser.addoption('--skip-desbloquearsat',
            action='store_true',
            help='Ignora funcao `DesbloquearSAT`')

    parser.addoption('--skip-trocarcodigodeativacao',
            action='store_true',
            help='Ignora funcao `TrocarCodigoDeAtivacao`')


@pytest.fixture(scope='module')
def clientesatlocal(request):
    funcoes = ClienteSATLocal(
            BibliotecaSAT(
                    request.config.getoption('--lib-caminho'),
                    convencao=request.config.getoption('--lib-convencao')),
            codigo_ativacao=request.config.getoption('--codigo-ativacao'))
    return funcoes


@pytest.fixture(scope='module')
def cfevenda(request):
    _opcao = request.config.getoption
    cfe = CFeVenda(
            CNPJ=_opcao('--cnpj-ac'),
            signAC=_opcao('--assinatura-ac'),
            numeroCaixa=_opcao('--numero-caixa'),
            emitente=Emitente(
                    CNPJ=_opcao('--emitente-cnpj'),
                    IE=_opcao('--emitente-ie'),
                    IM=_opcao('--emitente-im'),
                    cRegTribISSQN=_opcao('--emitente-issqn-regime'),
                    indRatISSQN=_opcao('--emitente-issqn-rateio')),
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


def _valores_possiveis(opcoes):
    return '; '.join(['{}-{}'.format(v, unidecode(s)) for v, s in opcoes])
