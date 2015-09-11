# -*- coding: utf-8 -*-
#
# satcfe/tests/resposta/test_comunicarcertificadoicpbrasil.py
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

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaSAT


RESP_SUCESSO = [
        u'123456|05000|Certificado transmitido com sucesso||',
    ]


RESP_FALHA = [
        u'123456|05001|Código de ativação inválido||',
        u'123456|05002|Erro de comunicação com a SEFAZ||',
        u'123456|05003|Certificado inválido||',
        u'123456|05098|SAT em processamento. Tente novamente.||',
        u'123456|05099|Erro desconhecido||',
    ]


RESP_INVALIDA = [
        u'Resposta sem nenhum separador',
        u'Numero inesperado de campos|a|b|c|d|e|f',
    ]


CERTIFICADO_ICPBRASIL = """-----BEGIN CERTIFICATE-----
VGhlIFplbiBvZiBQeXRob24sIGJ5IFRpbSBQZXRlcnMKCkJlYXV0aWZ1bCBpcyBiZXR0ZXIg
dGhhbiB1Z2x5LgpFeHBsaWNpdCBpcyBiZXR0ZXIgdGhhbiBpbXBsaWNpdC4KU2ltcGxlIGlz
IGJldHRlciB0aGFuIGNvbXBsZXguCkNvbXBsZXggaXMgYmV0dGVyIHRoYW4gY29tcGxpY2F0
ZWQuCkZsYXQgaXMgYmV0dGVyIHRoYW4gbmVzdGVkLgpTcGFyc2UgaXMgYmV0dGVyIHRoYW4g
ZGVuc2UuClJlYWRhYmlsaXR5IGNvdW50cy4KU3BlY2lhbCBjYXNlcyBhcmVuJ3Qgc3BlY2lh
bCBlbm91Z2ggdG8gYnJlYWsgdGhlIHJ1bGVzLgpBbHRob3VnaCBwcmFjdGljYWxpdHkgYmVh
dHMgcHVyaXR5LgpFcnJvcnMgc2hvdWxkIG5ldmVyIHBhc3Mgc2lsZW50bHkuClVubGVzcyBl
eHBsaWNpdGx5IHNpbGVuY2VkLgpJbiB0aGUgZmFjZSBvZiBhbWJpZ3VpdHksIHJlZnVzZSB0
aGUgdGVtcHRhdGlvbiB0byBndWVzcy4KVGhlcmUgc2hvdWxkIGJlIG9uZS0tIGFuZCBwcmVm
ZXJhYmx5IG9ubHkgb25lIC0tb2J2aW91cyB3YXkgdG8gZG8gaXQuCkFsdGhvdWdoIHRoYXQg
d2F5IG1heSBub3QgYmUgb2J2aW91cyBhdCBmaXJzdCB1bmxlc3MgeW91J3JlIER1dGNoLgpO
b3cgaXMgYmV0dGVyIHRoYW4gbmV2ZXIuCkFsdGhvdWdoIG5ldmVyIGlzIG9mdGVuIGJldHRl
ciB0aGFuICpyaWdodCogbm93LgpJZiB0aGUgaW1wbGVtZW50YXRpb24gaXMgaGFyZCB0byBl
eHBsYWluLCBpdCdzIGEgYmFkIGlkZWEuCklmIHRoZSBpbXBsZW1lbnRhdGlvbiBpcyBlYXN5
IHRvIGV4cGxhaW4sIGl0IG1heSBiZSBhIGdvb2QgaWRlYS4KTmFtZXNwYWNlcyBhcmUgb25l
IGhvbmtpbmcgZ3JlYXQgaWRlYSAtLSBsZXQncyBkbyBtb3JlIG9mIHRob3NlIQ==
-----END CERTIFICATE-----
"""


def test_resposta_comunicarcertificadoicpbrasil():
    resposta = RespostaSAT.comunicar_certificado_icpbrasil(RESP_SUCESSO[0])
    assert resposta.numeroSessao == 123456
    assert resposta.EEEEE == '05000'

    for retorno in RESP_FALHA:
        with pytest.raises(ExcecaoRespostaSAT):
            resposta = RespostaSAT.comunicar_certificado_icpbrasil(retorno)

    for retorno in RESP_INVALIDA:
        with pytest.raises(ErroRespostaSATInvalida):
            resposta = RespostaSAT.comunicar_certificado_icpbrasil(retorno)


@pytest.mark.skipif(
        pytest.config.getoption('--skip-comunicarcertificadoicpbrasil') or
        pytest.config.getoption('--skip-funcoes-sat'),
        reason='Funcao `ComunicarCertificadoICPBRASIL` explicitamente ignorada')
def test_funcao_comunicarcertificadoicpbrasil(clientesatlocal):
    # a comunicação do certificado ICP Brasil é complementar à ativação do
    # equipamento SAT e nenhum equipamento em desenvolvimento permite a
    # ativação, pois já vem ativado pelo fabricante, por isso, não esperamos
    # sucesso na execução da função
    with pytest.raises(ExcecaoRespostaSAT):
        resposta = clientesatlocal.comunicar_certificado_icpbrasil(
                CERTIFICADO_ICPBRASIL)
