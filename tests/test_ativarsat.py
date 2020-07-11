# -*- coding: utf-8 -*-
#
# tests/test_ativarsat.py
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

from io import open

from builtins import str as text

import pytest

from satcomum import br
from satcomum import constantes

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaAtivarSAT
from satcfe.resposta.ativarsat import ATIVADO_CORRETAMENTE
from satcfe.resposta.ativarsat import CSR_ICPBRASIL_CRIADO_SUCESSO
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
    arquivo = text(datadir.join('respostas-de-sucesso.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    resposta = RespostaAtivarSAT.analisar(respostas[0])
    assert resposta.numeroSessao == 123456
    assert resposta.EEEEE == ATIVADO_CORRETAMENTE
    assert resposta.CSR == str_to_base64(CSR_EXEMPLO)
    assert resposta.csr() == CSR_EXEMPLO

    resposta = RespostaAtivarSAT.analisar(respostas[1])
    assert resposta.numeroSessao == 123456
    assert resposta.EEEEE == CSR_ICPBRASIL_CRIADO_SUCESSO
    assert resposta.CSR == str_to_base64(CSR_EXEMPLO)
    assert resposta.csr() == CSR_EXEMPLO


def test_respostas_de_falha(datadir):
    arquivo = text(datadir.join('respostas-de-falha.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaAtivarSAT.analisar(retorno)


def test_respostas_invalidas(datadir):
    arquivo = text(datadir.join('respostas-invalidas.txt'))
    with open(arquivo, 'r', encoding='utf-8') as f:
        respostas = f.read().splitlines()

    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaAtivarSAT.analisar(retorno)


@pytest.mark.acessa_sat
@pytest.mark.invoca_ativarsat
def test_funcao_ativarsat(request, clientesatlocal):
    # Nenhum equipamento SAT de desenvolvimento (kit SAT) permite a ativação,
    # pois já vem ativado pelo fabricante, por isso não esperamos sucesso na
    # execução da função, a não ser contra uma biblioteca SAT de simulação.
    #
    # Este teste baseia-se na resposta da biblioteca SAT de simulação (mockup)
    # que é usada nos testes do projeto SATHub:
    # https://github.com/base4sistemas/sathub
    #
    emitente_cnpj = request.config.getoption('--emitente-cnpj')
    emitente_uf = request.config.getoption('--emitente-uf')

    resposta = clientesatlocal.ativar_sat(
            constantes.CERTIFICADO_ACSAT_SEFAZ,
            emitente_cnpj,
            br.codigo_ibge_uf(emitente_uf))

    assert resposta.CSR == str_to_base64(CSR_EXEMPLO)
    assert resposta.mensagem == 'Ativado corretamente'
