# -*- coding: utf-8 -*-
#
# satcfe/tests/resposta/test_ativarsat.py
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

import pytest

from satcomum import br
from satcomum import constantes

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaAtivarSAT
from satcfe.util import str_to_base64


CSR_EXEMPLO = """-----BEGIN CERTIFICATE REQUEST-----
MIIBnTCCAQYCAQAwXTELMAkGA1UEBhMCU0cxETAPBgNVBAoTCE0yQ3J5cHRvMRIw
EAYDVQQDEwlsb2NhbGhvc3QxJzAlBgkqhkiG9w0BCQEWGGFkbWluQHNlcnZlci5l
eGFtcGxlLmRvbTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAr1nYY1Qrll1r
uB/FqlCRrr5nvupdIN+3wF7q915tvEQoc74bnu6b8IbbGRMhzdzmvQ4SzFfVEAuM
MuTHeybPq5th7YDrTNizKKxOBnqE2KYuX9X22A1Kh49soJJFg6kPb9MUgiZBiMlv
tb7K3CHfgw5WagWnLl8Lb+ccvKZZl+8CAwEAAaAAMA0GCSqGSIb3DQEBBAUAA4GB
AHpoRp5YS55CZpy+wdigQEwjL/wSluvo+WjtpvP0YoBMJu4VMKeZi405R7o8oEwi
PdlrrliKNknFmHKIaCKTLRcU59ScA6ADEIWUzqmUzP5Cs6jrSRo3NKfg1bd09D1K
9rsQkRc9Urv9mRBIsredGnYECNeRaK5R1yzpOowninXC
-----END CERTIFICATE REQUEST-----"""


def test_resposta_ativarsat(datadir):
    with open(datadir.join('respostas-de-sucesso.txt'), 'r') as f:
        r_sucessos = f.read().splitlines()

    resposta = RespostaAtivarSAT.analisar(r_sucessos[0])
    assert resposta.numeroSessao == 123456
    assert resposta.EEEEE == '04000'
    assert resposta.CSR == str_to_base64(CSR_EXEMPLO)
    assert resposta.csr() == CSR_EXEMPLO

    resposta = RespostaAtivarSAT.analisar(r_sucessos[1])
    assert resposta.numeroSessao == 123456
    assert resposta.EEEEE == '04006'
    assert resposta.CSR == str_to_base64(CSR_EXEMPLO)
    assert resposta.csr() == CSR_EXEMPLO


def test_respostas_de_falha(datadir):
    with open(datadir.join('respostas-de-falha.txt'), 'r') as f:
        respostas = f.read().splitlines()
    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaAtivarSAT.analisar(retorno)


def test_respostas_invalidas(datadir):
    with open(datadir.join('respostas-invalidas.txt'), 'r') as f:
        respostas = f.read().splitlines()
    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaAtivarSAT.analisar(retorno)


@pytest.mark.skipif(
        pytest.config.getoption('--skip-ativarsat') or
        pytest.config.getoption('--skip-funcoes-sat'),
        reason='Funcao `AtivarSAT` explicitamente ignorada')
def test_funcao_ativarsat(clientesatlocal):
    # nenhum equipamento SAT em desenvolvimento (kit desenvolvimento)
    # permite a ativação, pois já vem ativado pelo fabricante, por isso
    # não esperamos sucesso na execução da função
    with pytest.raises(ExcecaoRespostaSAT):
        clientesatlocal.ativar_sat(
                constantes.CERTIFICADO_ACSAT_SEFAZ,
                pytest.config.getoption('--emitente-cnpj'),
                br.codigo_ibge_uf(pytest.config.getoption('--emitente-uf')))
