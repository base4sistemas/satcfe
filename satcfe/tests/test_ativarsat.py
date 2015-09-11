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

import base64

import pytest

from satcomum import br
from satcomum import constantes

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaAtivarSAT


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


RESP_SUCESSO = [
        u'123456|04000|Ativado corretamente|||LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQm5UQ0NBUVlDQVFBd1hURUxNQWtHQTFVRUJoTUNVMGN4RVRBUEJnTlZCQW9UQ0UweVEzSjVjSFJ2TVJJdwpFQVlEVlFRREV3bHNiMk5oYkdodmMzUXhKekFsQmdrcWhraUc5dzBCQ1FFV0dHRmtiV2x1UUhObGNuWmxjaTVsCmVHRnRjR3hsTG1SdmJUQ0JuekFOQmdrcWhraUc5dzBCQVFFRkFBT0JqUUF3Z1lrQ2dZRUFyMW5ZWTFRcmxsMXIKdUIvRnFsQ1JycjVudnVwZElOKzN3RjdxOTE1dHZFUW9jNzRibnU2YjhJYmJHUk1oemR6bXZRNFN6RmZWRUF1TQpNdVRIZXliUHE1dGg3WURyVE5pektLeE9CbnFFMktZdVg5WDIyQTFLaDQ5c29KSkZnNmtQYjlNVWdpWkJpTWx2CnRiN0szQ0hmZ3c1V2FnV25MbDhMYitjY3ZLWlpsKzhDQXdFQUFhQUFNQTBHQ1NxR1NJYjNEUUVCQkFVQUE0R0IKQUhwb1JwNVlTNTVDWnB5K3dkaWdRRXdqTC93U2x1dm8rV2p0cHZQMFlvQk1KdTRWTUtlWmk0MDVSN284b0V3aQpQZGxycmxpS05rbkZtSEtJYUNLVExSY1U1OVNjQTZBREVJV1V6cW1VelA1Q3M2anJTUm8zTktmZzFiZDA5RDFLCjlyc1FrUmM5VXJ2OW1SQklzcmVkR25ZRUNOZVJhSzVSMXl6cE9vd25pblhDCi0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQ==',
        u'123456|04006|CSR ICP-BRASIL criado com sucesso|||LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQm5UQ0NBUVlDQVFBd1hURUxNQWtHQTFVRUJoTUNVMGN4RVRBUEJnTlZCQW9UQ0UweVEzSjVjSFJ2TVJJdwpFQVlEVlFRREV3bHNiMk5oYkdodmMzUXhKekFsQmdrcWhraUc5dzBCQ1FFV0dHRmtiV2x1UUhObGNuWmxjaTVsCmVHRnRjR3hsTG1SdmJUQ0JuekFOQmdrcWhraUc5dzBCQVFFRkFBT0JqUUF3Z1lrQ2dZRUFyMW5ZWTFRcmxsMXIKdUIvRnFsQ1JycjVudnVwZElOKzN3RjdxOTE1dHZFUW9jNzRibnU2YjhJYmJHUk1oemR6bXZRNFN6RmZWRUF1TQpNdVRIZXliUHE1dGg3WURyVE5pektLeE9CbnFFMktZdVg5WDIyQTFLaDQ5c29KSkZnNmtQYjlNVWdpWkJpTWx2CnRiN0szQ0hmZ3c1V2FnV25MbDhMYitjY3ZLWlpsKzhDQXdFQUFhQUFNQTBHQ1NxR1NJYjNEUUVCQkFVQUE0R0IKQUhwb1JwNVlTNTVDWnB5K3dkaWdRRXdqTC93U2x1dm8rV2p0cHZQMFlvQk1KdTRWTUtlWmk0MDVSN284b0V3aQpQZGxycmxpS05rbkZtSEtJYUNLVExSY1U1OVNjQTZBREVJV1V6cW1VelA1Q3M2anJTUm8zTktmZzFiZDA5RDFLCjlyc1FrUmM5VXJ2OW1SQklzcmVkR25ZRUNOZVJhSzVSMXl6cE9vd25pblhDCi0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQ==',
    ]


RESP_FALHA = [
        u'123456|04001|Erro na criação do certificado||',
        u'123456|04002|SEFAZ não reconhece este SAT (CNPJ inválido)||',
        u'123456|04003|SAT já ativado||',
        u'123456|04004|SAT com uso cessado||',
        u'123456|04005|Erro de comunicação com a SEFAZ||',
        u'123456|04007|Erro na criação do CSR ICP-BRASIL||',
        u'123456|04098|SAT em processamento. Tente novamente.||',
        u'123456|04099|Erro desconhecido na ativacao||',
    ]


RESP_INVALIDA = [
        u'Resposta sem nenhum separador',
        u'Numero inesperado de campos|a|b|c|d|e|f',
    ]


def test_resposta_ativarsat():
    resposta = RespostaAtivarSAT.analisar(RESP_SUCESSO[0])
    assert resposta.numeroSessao == 123456
    assert resposta.EEEEE == '04000'
    assert resposta.CSR == base64.b64encode(CSR_EXEMPLO)
    assert resposta.csr() == CSR_EXEMPLO

    resposta = RespostaAtivarSAT.analisar(RESP_SUCESSO[1])
    assert resposta.numeroSessao == 123456
    assert resposta.EEEEE == '04006'
    assert resposta.CSR == base64.b64encode(CSR_EXEMPLO)
    assert resposta.csr() == CSR_EXEMPLO

    for retorno in RESP_FALHA:
        with pytest.raises(ExcecaoRespostaSAT):
            resposta = RespostaAtivarSAT.analisar(retorno)

    for retorno in RESP_INVALIDA:
        with pytest.raises(ErroRespostaSATInvalida):
            resposta = RespostaAtivarSAT.analisar(retorno)


@pytest.mark.skipif(
        pytest.config.getoption('--skip-ativarsat') or
        pytest.config.getoption('--skip-funcoes-sat'),
        reason='Funcao `AtivarSAT` explicitamente ignorada')
def test_funcao_ativarsat(clientesatlocal):
    # nenhum equipamento SAT em desenvolvimento (kit desenvolvimento)
    # permite a ativação, pois já vem ativado pelo fabricante, por isso
    # não esperamos sucesso na execução da função
    with pytest.raises(ExcecaoRespostaSAT):
        resposta = clientesatlocal.ativar_sat(
                constantes.CERTIFICADO_ACSAT_SEFAZ,
                pytest.config.getoption('--emitente-cnpj'),
                br.codigo_ibge_uf(pytest.config.getoption('--emitente-uf')))
