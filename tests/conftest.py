# -*- coding: utf-8 -*-
#
# tests/conftest.py
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

import os
import re
import shutil

from collections import namedtuple
from decimal import Decimal

from builtins import str as text

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
from satcfe.rede import ConfiguracaoRede


_SATCFE_TEST_LIB = 'SATCFE_TEST_LIB'
_SATCFE_TEST_LIB_CONVENCAO = 'SATCFE_TEST_LIB_CONVENCAO'
_SATCFE_TEST_CODIGO_ATIVACAO = 'SATCFE_TEST_CODIGO_ATIVACAO'
_SATCFE_TEST_EMITENTE_UF = 'SATCFE_TEST_EMITENTE_UF'
_SATCFE_TEST_CNPJ_AC = 'SATCFE_TEST_CNPJ_AC'
_SATCFE_TEST_EMITENTE_CNPJ = 'SATCFE_TEST_EMITENTE_CNPJ'
_SATCFE_TEST_EMITENTE_IE = 'SATCFE_TEST_EMITENTE_IE'
_SATCFE_TEST_EMITENTE_IM = 'SATCFE_TEST_EMITENTE_IM'
_SATCFE_TEST_EMITENTE_ISSQN_REGIME = 'SATCFE_TEST_EMITENTE_ISSQN_REGIME'
_SATCFE_TEST_EMITENTE_ISSQN_RATEIO = 'SATCFE_TEST_EMITENTE_ISSQN_RATEIO'


_MarkerData = namedtuple('_MarkerData', 'name reason option_help')


def _to_cmd_line_option(marker_name):
    # <marker_name> str (eg. "invoca_ativarsat" -> "--invoca-ativarsat")
    return '--{}'.format(marker_name.replace('_', '-'))


def _marker_data(funcao_sat):
    reason = (
            'Ignorando testes marcados como "invoca-{name:s}"; '
            'Requer "--invoca-{name:s}" e "--acessa-sat" para que '
            'sejam executados'
        ).format(name=funcao_sat.lower())

    option_help = (
            'Permite que sejam executados os testes que acessem a '
            'biblioteca SAT (eventualmente acessando o equipamento SAT real), '
            'para acesso à função "{:s}"'
        ).format(funcao_sat)

    md = _MarkerData(
            name='invoca_{}'.format(funcao_sat.lower()),
            reason=reason,
            option_help=option_help)

    return md


_MARKERS = [
        #
        # Até a versão 4.5.0 pytest requer que os marcadores sejam
        # explicitamente definidos; ao alterar estes dados, revise os
        # marcadores relacionados em setup.cfg;
        #
        # Veja estes links:
        # https://docs.pytest.org/en/latest/example/markers.html
        # https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
        #
        _MarkerData(
                name='acessa_sat',
                reason=(
                        'Ignorando testes marcados como "acessa_sat"; '
                        'Requer "--acessa-sat" para que sejam '
                        'executados'
                    ),
                option_help=(
                        'Permite que sejam executados os testes que acessem a '
                        'biblioteca SAT (eventualmente acessando o '
                        'equipamento SAT real)'
                    ),
            ),
        _marker_data('AtivarSAT'),
        _marker_data('ComunicarCertificadoICPBRASIL'),
        _marker_data('EnviarDadosVenda'),
        _marker_data('CancelarUltimaVenda'),
        _marker_data('ConsultarSAT'),
        _marker_data('TesteFimAFim'),
        _marker_data('ConsultarStatusOperacional'),
        _marker_data('ConsultarNumeroSessao'),
        _marker_data('ConfigurarInterfaceDeRede'),
        _marker_data('AssociarAssinatura'),
        _marker_data('AtualizarSoftwareSAT'),
        _marker_data('ExtrairLogs'),
        _marker_data('BloquearSAT'),
        _marker_data('DesbloquearSAT'),
        _marker_data('TrocarCodigoDeAtivacao'),
        _marker_data('ConsultarUltimaSessaoFiscal'),
    ]


def pytest_addoption(parser):

    parser.addoption(
            '--cnpj-ac',
            action='store',
            default=os.getenv(_SATCFE_TEST_CNPJ_AC, default='16716114000172'),
            help='CNPJ da empresa desenvolvedora da AC (apenas digitos)')

    parser.addoption(
            '--emitente-cnpj',
            action='store',
            default=os.getenv(
                    _SATCFE_TEST_EMITENTE_CNPJ,
                    default='08723218000186'),
            help='CNPJ do estabelecimento emitente (apenas digitos)')

    parser.addoption(
            '--emitente-ie',
            action='store',
            default=os.getenv(
                    _SATCFE_TEST_EMITENTE_IE,
                    default='149626224113'),
            help='Inscricao estadual do emitente (apenas digitos)')

    parser.addoption(
            '--emitente-im',
            action='store',
            default=os.getenv(_SATCFE_TEST_EMITENTE_IM, default='123123'),
            help='Inscricao municipal do emitente (apenas digitos)')

    parser.addoption(
            '--emitente-uf',
            action='store',
            default=os.getenv(_SATCFE_TEST_EMITENTE_UF, default='SP'),
            help='Sigla da unidade federativa do estabelecimento emitente')

    parser.addoption(
            '--emitente-issqn-regime',
            action='store',
            default=os.getenv(
                    _SATCFE_TEST_EMITENTE_ISSQN_REGIME,
                    default=constantes.C15_SOCIEDADE_PROFISSIONAIS),
            help=(
                    'Regime especial de tributacao do ISSQN ({:s}) do '
                    'emitente, em casos de testes de emissao de venda e/ou '
                    'cancelamento'
                ).format(_valores_possiveis(constantes.C15_CREGTRIBISSQN_EMIT)))

    parser.addoption(
            '--emitente-issqn-rateio',
            action='store',
            default=os.getenv(
                    _SATCFE_TEST_EMITENTE_ISSQN_RATEIO,
                    default=constantes.C16_NAO_RATEADO),
            help=(
                    'Indicador de rateio do desconto sobre o subtotal para '
                    'produtos tributados no ISSQN ({:s}) do emitente, em '
                    'casos de testes de emissao de venda e/ou cancelamento'
                ).format(_valores_possiveis(constantes.C16_INDRATISSQN_EMIT)))

    parser.addoption(
            '--codigo-ativacao',
            action='store',
            default=os.getenv(
                    _SATCFE_TEST_CODIGO_ATIVACAO,
                    default='12345678'),
            help='Codigo de ativacao configurado no equipamento SAT')

    parser.addoption(
            '--assinatura-ac',
            action='store',
            default=constantes.ASSINATURA_AC_TESTE,
            help='Conteudo da assinatura da AC')

    parser.addoption(
            '--numero-caixa',
            action='store',
            default=1,
            type=int,
            help='Numero do caixa de origem')

    parser.addoption(
            '--lib-caminho',
            action='store',
            default=os.getenv(_SATCFE_TEST_LIB, default='libsat.so'),
            help='Caminho completo para a biblioteca SAT')

    parser.addoption(
            '--lib-convencao',
            action='store',
            choices=[constantes.STANDARD_C, constantes.WINDOWS_STDCALL],
            default=os.getenv(
                    _SATCFE_TEST_LIB_CONVENCAO,
                    default=constantes.STANDARD_C),
            type=int,
            help=(
                    'Convencao de chamada para a biblioteca SAT ({:s})'
                ).format(_valores_possiveis(constantes.CONVENCOES_CHAMADA)))

    # TODO: implementar testes para acesso compartilhado ao equipamento SAT
    # --sathub-host     127.0.0.1
    # --sathub-port     8080
    # --sathub-baseurl  /hub/v1/
    # --sathub-username
    # --sathub-password

    # Opções para permitir, via linha de comando, a execução de testes
    # marcados como testes que acessam à biblioteca SAT; por exemplo:
    #
    #     python setup.py test -a "--acessa-sat --invoca-ativarsat"
    #
    # Irá permitir que sejam executados os testes que indiquem acesso à
    # biblioteca SAT e/ou que acessem a função AtivarSAT, por exemplo:
    #
    #     @pytest.mark.acessa_sat
    #     @pytest.mark.invoca_ativarsat
    #     def test_meu_teste_que_acessa_funcao_ativarsat(clientesatlocal):
    #         assert 1 == 0, "Quem diria!"
    #
    for el in _MARKERS:
        option_name = _to_cmd_line_option(el.name)
        parser.addoption(
                option_name,
                action='store_true',
                default=False,
                help=el.option_help)


def pytest_collection_modifyitems(config, items):
    markers_set = {}

    for el in _MARKERS:
        option_name = _to_cmd_line_option(el.name)
        if not config.getoption(option_name):
            markers_set[el.name] = pytest.mark.skip(reason=el.reason)

    for item in items:
        for key, marker in markers_set.items():
            if key in item.keywords:
                item.add_marker(marker)


@pytest.fixture(scope='function')
def datadir(tmpdir, request):
    """Este fixture procura por um diretório de dados com o mesmo nome do
    módulo de teste (mas sem a extensão ".py" e com o prefixo "test_" e/ou o
    sufixo "_test" removidos) dentro de ``satcfe/tests/data/``.

    Por exemplo, o módulo de testes ``tests/test_ativarsat.py`` possui um
    diretório de dados em ``tests/data/ativarsat/``.

    Existindo um diretório de dados, todo seu conteúdo será copiado para o
    diretório temporário (*fixture* ``tmpdir`` de pytest), de modo que os
    testes possam usar esses arquivos.

    No exemplo abaixo, os arquivos ``data.txt`` e ``huge.txt`` deverão ser
    criados no diretório ``tests/data/foo/``. Note que o diretório ``data/``
    está no mesmo diretório em que módulo ``test_foo.py`` se encontra:

    .. sourcecode:: python

        def test_foo(datadir):
            with open(datadir.join('data.txt'), 'r') as f_data, \
                 open(datadir.join('huge.txt'), 'r') as f_huge:
                data = f_data.read()
                expected_result = f_huge.read()
            result = do_something_with(data)
            assert result == expected_result

    .. note::

        Baseado `nesta resposta <https://stackoverflow.com/a/29631801>`_ de
        Stack Overflow.

    """
    path, name = os.path.split(request.module.__file__)
    name, _ = os.path.splitext(name)
    name = re.sub(r'^test_|_test$', '', name)
    dirname = os.path.join(path, 'data', name)

    if os.path.isdir(dirname):
        for name in os.listdir(dirname):
            filename = os.path.join(dirname, name)
            if os.path.isfile(filename):
                # copia apenas arquivos regulares (os.path.isfile)
                dst = text(tmpdir)
                shutil.copy(filename, dst)

    return tmpdir


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


@pytest.fixture(scope='module')
def cfecancelamento(request):
    _opcao = request.config.getoption
    # (!) Talvez seja necessário atribuir valor ao atributo 'chCanc' nas
    #     funcoes que utilizarem esta fixture.
    cfe_canc = CFeCancelamento(
            CNPJ=_opcao('--cnpj-ac'),
            signAC=_opcao('--assinatura-ac'),
            numeroCaixa=_opcao('--numero-caixa'),
            destinatario=Destinatario(
                    CPF='11122233396',
                    xNome='João de Teste'))
    return cfe_canc


@pytest.fixture(scope='module')
def rede_completo(request):
    conf = ConfiguracaoRede(
            tipoInter=constantes.REDE_TIPOINTER_WIFI,
            SSID='Principal',
            seg=constantes.REDE_SEG_WPA_ENTERPRISE,
            codigo='s3cr370',
            tipoLan=constantes.REDE_TIPOLAN_DHCP,
            lanIP='192.168.5.101',
            lanMask='255.255.255.0',
            lanGW='192.168.5.1',
            lanDNS1='192.168.5.201',
            lanDNS2='192.168.5.202',
            usuario='john',
            senha='c0nn0r',
            proxy=constantes.REDE_PROXY_CONFIGURACAO,
            proxy_ip='192.168.5.101',
            proxy_porta=8080,
            proxy_user='anderson',
            proxy_senha='7h0m45')
    return conf


@pytest.fixture(scope='module')
def rede_minimo(request):
    conf = ConfiguracaoRede(
            tipoInter=constantes.REDE_TIPOINTER_ETHE,
            tipoLan=constantes.REDE_TIPOLAN_DHCP,
            proxy=constantes.REDE_PROXY_NONE)
    return conf


def _valores_possiveis(opcoes):
    return '; '.join(['{}-{}'.format(v, unidecode(s)) for v, s in opcoes])
