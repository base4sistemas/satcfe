# -*- coding: utf-8 -*-
#
# satcfe/tests/resposta/test_testefimafim.py
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

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaTesteFimAFim
from satcfe.util import as_datetime


RESP_SUCESSO = [
        u'031545|09000|Emitido com sucesso|||'
                'PENGZT48aW5mQ0ZlIHZlcnNhb0RhZG9zRW50PSIwLjA2IiB2ZXJzYW89IjA'\
                'uMDYiIHZlcnNhb1NCPSIwMTAwMDAiIElkPSJDRmUzNTE1MDkwODcyMzIxOD'\
                'AwMDE4NjU5OTAwMDA0MDE5MDAwMDAwNzk3MjA2OCI+PGlkZT48Y1VGPjM1P'\
                'C9jVUY+PGNORj43OTcyMDY8L2NORj48bW9kPjU5PC9tb2Q+PG5zZXJpZVNB'\
                'VD45MDAwMDQwMTk8L25zZXJpZVNBVD48bkNGZT4wMDAwMDA8L25DRmU+PGR'\
                'FbWk+MjAxNTA5MTI8L2RFbWk+PGhFbWk+MTAxNTEzPC9oRW1pPjxjRFY+OD'\
                'wvY0RWPjx0cEFtYj4yPC90cEFtYj48Q05QSj4xNjcxNjExNDAwMDE3MjwvQ'\
                '05QSj48c2lnbkFDPlNHUi1TQVQgU0lTVEVNQSBERSBHRVNUQU8gRSBSRVRB'\
                'R1VBUkRBIERPIFNBVDwvc2lnbkFDPjxhc3NpbmF0dXJhUVJDT0RFPmxlS2V'\
                'HNkpjQjZ6M0VoeWVOb0RrV2RwVXp3QmxrSWhOM2ZyWVpIYnRiYzU3eXRDWE'\
                '9rVWhPTyt0U3c4NXFlVThxVW5OL05QV3pTSUx6eHI3RlhYaDhHdUhYOFdwM'\
                '1BLU0sxWlFkQ29CTlJaSlFyNjBIWSsyamRIKzN2V3p0OFpWTTlJRWRPSUF0'\
                'UFc0L3E4R3M0UC81RVl5VFBpa25uMGxzTmRQTmk3OXViWDhRYVY1OE1KUVl'\
                'CdHB4TG9uQkVEZFRVMFVxWnVTckI1dzJGajBRSGQyUTBQcTZpK1JZVkkrQS'\
                's0ZDc5Smt1S3N6blNpc3F4SzNlZnFJdzhtT3lGUkxVSUxlaUxrb21RSHd5L'\
                '0dZcVQ1Wkx2Z0praExzY3pyVnB6Y1BzUlN3T0l3eDNPYUlJK0NFVS82Vnlj'\
                'bStFTVRJb1NKT3VpcUY1SllWUGZEa1hjQVc5Zz09PC9hc3NpbmF0dXJhUVJ'\
                'DT0RFPjxudW1lcm9DYWl4YT4wOTk8L251bWVyb0NhaXhhPjwvaWRlPjxlbW'\
                'l0PjxDTlBKPjA4NzIzMjE4MDAwMTg2PC9DTlBKPjx4Tm9tZT5UQU5DQSBJT'\
                'kZPUk1BVElDQSBFSVJFTEk8L3hOb21lPjx4RmFudD5UQU5DQTwveEZhbnQ+'\
                'PGVuZGVyRW1pdD48eExncj5SVUEgRU5HRU5IRUlSTyBKT1JHRSBPTElWQTw'\
                'veExncj48bnJvPjczPC9ucm8+PHhCYWlycm8+VklMQSBNQVNDT1RFPC94Qm'\
                'FpcnJvPjx4TXVuPlNBTyBQQVVMTzwveE11bj48Q0VQPjA0MzYyMDYwPC9DR'\
                'VA+PC9lbmRlckVtaXQ+PElFPjE0OTYyNjIyNDExMzwvSUU+PGNSZWdUcmli'\
                'PjM8L2NSZWdUcmliPjxjUmVnVHJpYklTU1FOPjE8L2NSZWdUcmliSVNTUU4'\
                '+PGluZFJhdElTU1FOPk48L2luZFJhdElTU1FOPjwvZW1pdD48ZGVzdD48Q0'\
                '5QSj4xNjcxNjExNDAwMDE3MjwvQ05QSj48L2Rlc3Q+PGRldCBuSXRlbT0iM'\
                'SI+PHByb2Q+PGNQcm9kPjAwMTwvY1Byb2Q+PHhQcm9kPk1pbmlQYyBUYW5j'\
                'YTwveFByb2Q+PENGT1A+NTAwMTwvQ0ZPUD48dUNvbT5VTjwvdUNvbT48cUN'\
                'vbT4xLjAwMDA8L3FDb20+PHZVbkNvbT42NTQuMzIwPC92VW5Db20+PHZQcm'\
                '9kPjY1NC4zMjwvdlByb2Q+PGluZFJlZ3JhPkE8L2luZFJlZ3JhPjx2SXRlb'\
                'T42NTQuMzI8L3ZJdGVtPjx2UmF0RGVzYz4wLjAwPC92UmF0RGVzYz48dlJh'\
                'dEFjcj4wLjAwPC92UmF0QWNyPjwvcHJvZD48aW1wb3N0bz48dkl0ZW0xMjc'\
                '0MT4xLjAwPC92SXRlbTEyNzQxPjxJQ01TPjxJQ01TMDA+PE9yaWc+MDwvT3'\
                'JpZz48Q1NUPjAwPC9DU1Q+PHBJQ01TPjEyLjAwPC9wSUNNUz48dklDTVM+N'\
                'zguNTI8L3ZJQ01TPjwvSUNNUzAwPjwvSUNNUz48UElTPjxQSVNBbGlxPjxD'\
                'U1Q+MDE8L0NTVD48dkJDPjY1NC4zMjwvdkJDPjxwUElTPjAuMDYwMDwvcFB'\
                'JUz48dlBJUz4zOS4yNjwvdlBJUz48L1BJU0FsaXE+PC9QSVM+PENPRklOUz'\
                '48Q09GSU5TQWxpcT48Q1NUPjAxPC9DU1Q+PHZCQz42NTQuMzI8L3ZCQz48c'\
                'ENPRklOUz4wLjA0MDA8L3BDT0ZJTlM+PHZDT0ZJTlM+MjYuMTc8L3ZDT0ZJ'\
                'TlM+PC9DT0ZJTlNBbGlxPjwvQ09GSU5TPjwvaW1wb3N0bz48L2RldD48dG9'\
                '0YWw+PElDTVNUb3Q+PHZJQ01TPjc4LjUyPC92SUNNUz48dlByb2Q+NjU0Lj'\
                'MyPC92UHJvZD48dkRlc2M+MC4wMDwvdkRlc2M+PHZQSVM+MzkuMjY8L3ZQS'\
                'VM+PHZDT0ZJTlM+MjYuMTc8L3ZDT0ZJTlM+PHZQSVNTVD4wLjAwPC92UElT'\
                'U1Q+PHZDT0ZJTlNTVD4wLjAwPC92Q09GSU5TU1Q+PHZPdXRybz4wLjAwPC9'\
                '2T3V0cm8+PC9JQ01TVG90Pjx2Q0ZlPjY1NC4zMjwvdkNGZT48dkNGZUxlaT'\
                'EyNzQxPjEuMDA8L3ZDRmVMZWkxMjc0MT48L3RvdGFsPjxwZ3RvPjxNUD48Y'\
                '01QPjAxPC9jTVA+PHZNUD4yMDAwLjAwPC92TVA+PC9NUD48dlRyb2NvPjEz'\
                'NDUuNjg8L3ZUcm9jbz48L3BndG8+PGluZkFkaWM+PG9ic0Zpc2NvIHhDYW1'\
                'wbz0ieENhbXBvMSI+PHhUZXh0bz54VGV4dG8xPC94VGV4dG8+PC9vYnNGaX'\
                'Njbz48L2luZkFkaWM+PC9pbmZDRmU+PFNpZ25hdHVyZSB4bWxucz0iaHR0c'\
                'DovL3d3dy53My5vcmcvMjAwMC8wOS94bWxkc2lnIyI+PFNpZ25lZEluZm8+'\
                'PENhbm9uaWNhbGl6YXRpb25NZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d'\
                '3LnczLm9yZy9UUi8yMDAxL1JFQy14bWwtYzE0bi0yMDAxMDMxNSIvPjxTaW'\
                'duYXR1cmVNZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yM'\
                'DAxLzA0L3htbGRzaWctbW9yZSNyc2Etc2hhMjU2Ii8+PFJlZmVyZW5jZSBV'\
                'Ukk9IiNDRmUzNTE1MDkwODcyMzIxODAwMDE4NjU5OTAwMDA0MDE5MDAwMDA'\
                'wNzk3MjA2OCI+PFRyYW5zZm9ybXM+PFRyYW5zZm9ybSBBbGdvcml0aG09Im'\
                'h0dHA6Ly93d3cudzMub3JnLzIwMDAvMDkveG1sZHNpZyNlbnZlbG9wZWQtc'\
                '2lnbmF0dXJlIi8+PFRyYW5zZm9ybSBBbGdvcml0aG09Imh0dHA6Ly93d3cu'\
                'dzMub3JnL1RSLzIwMDEvUkVDLXhtbC1jMTRuLTIwMDEwMzE1Ii8+PC9UcmF'\
                'uc2Zvcm1zPjxEaWdlc3RNZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d3Ln'\
                'czLm9yZy8yMDAxLzA0L3htbGVuYyNzaGEyNTYiLz48RGlnZXN0VmFsdWU+O'\
                'GlkUlF5aStNVlFPL1VhdHJkWW51UXNhYXY3WDh0dXZWMENobUVOVkRtND08'\
                'L0RpZ2VzdFZhbHVlPjwvUmVmZXJlbmNlPjwvU2lnbmVkSW5mbz48U2lnbmF'\
                '0dXJlVmFsdWU+Tzdlb2oraU9QZmxYVlBkNTNOVUdObWM1UEFuTmp2Kyt2cX'\
                'RRK2RRTXM5N0NsNWtWakVmWnVOSnEvK1Y0Q0FNellpWUNXN0YzUVFYTmsyb'\
                'jdpejZRMlYvcGFIVStWMVEvYy9UakkwUHo5VnlnUWNvdTZQVlYvVlRRcmtB'\
                'UE1IenhPOW5SbThyaU5uVGtXQVI2Y3hwajF4UXRmRlpBK2F3QktZMlpvdjE'\
                'venUzNTIwSGx1bTZBQXEwV3F4Y0tBeDk3ZEhRVU1Ia2QwQmRJQndCR3lEaW'\
                'FCVlVia0VTSlFqZHhlaEI4aDlXUFJvcXRibldKL3cxMGNDOC9hTlNDZlZ1Z'\
                '0R1L0ZrK3haSmk0SjZlWWJKVTNITTdDMTVMNHZDb2xuWGtSZERNS2UzeXJM'\
                'dGQ4QlcwdW54TXdvbW54dFhidWZIVTcvVzVxeWovUjJTaU41VmlLajB3PT0'\
                '8L1NpZ25hdHVyZVZhbHVlPjxLZXlJbmZvPjxYNTA5RGF0YT48WDUwOUNlcn'\
                'RpZmljYXRlPk1JSUdzRENDQkppZ0F3SUJBZ0lKQVJqZ3ZJem1kMkJHTUEwR'\
                '0NTcUdTSWIzRFFFQkN3VUFNR2N4Q3pBSkJnTlZCQVlUQWtKU01UVXdNd1lE'\
                'VlFRS0V5eFRaV055WlhSaGNtbGhJR1JoSUVaaGVtVnVaR0VnWkc4Z1JYTjB'\
                'ZV1J2SUdSbElGTmhieUJRWVhWc2J6RWhNQjhHQTFVRUF4TVlRVU1nVTBGVU'\
                'lHUmxJRlJsYzNSbElGTkZSa0ZhSUZOUU1CNFhEVEUxTURjd09ERTFNell6T'\
                'mxvWERUSXdNRGN3T0RFMU16WXpObG93Z2JVeEVqQVFCZ05WQkFVVENUa3dN'\
                'REF3TkRBeE9URUxNQWtHQTFVRUJoTUNRbEl4RWpBUUJnTlZCQWdUQ1ZOQlR'\
                '5QlFRVlZNVHpFUk1BOEdBMVVFQ2hNSVUwVkdRVm90VTFBeER6QU5CZ05WQk'\
                'FzVEJrRkRMVk5CVkRFb01DWUdBMVVFQ3hNZlFYVjBaVzUwYVdOaFpHOGdjR'\
                'zl5SUVGU0lGTkZSa0ZhSUZOUUlGTkJWREV3TUM0R0ExVUVBeE1uVkVGT1Ew'\
                'RWdTVTVHVDFKTlFWUkpRMEVnUlVsU1JVeEpPakE0TnpJek1qRTRNREF3TVR'\
                'nMk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUU'\
                'VBbDg5UGZqZmpaeTBRYXRnQnp2VitEdTA0ZWtqYmlZbW5WZTVTOUFITmlle'\
                'G5vOFZkcDlCNzlod0xLaURydnZ3QXRWcXJvY1dPUW1NM1NJeDVPRUN5L3Z2'\
                'Rmk0Nndhd0pUOVkyYTR6dUVGR3ZIWlN1RS9VcDNQQjUyZFAzNGFHYnBsaXM'\
                'wZDFScUlvWG9LV3ErRmxqV3MrTjg5cnd2UHhnSkdhZkdwM2UzdDhDcUlqcU'\
                'JQU0NYOEJteS8yWURqMUMvSjFDTFc5MXE5NHFWWDBDeGhLRkhBd2ZnSUtlN'\
                '1pIZVpwd3MyamlPbXRMRldLb2ZDU2Fjb25RdTVQSFVWek92N2tUcEs4WmJ2'\
                'c3ZuendMd0hhNi9yREpzT1JXLzMzVityeWZ1RHRSSCtub3MzdXNFL2F2Yy8'\
                '4bVUyNXEzcmo3ZlROYXg0Z2diNnJwRnRTeVRBV1JrRlpRSURBUUFCbzRJQ0'\
                'RqQ0NBZ293RGdZRFZSMFBBUUgvQkFRREFnWGdNSHNHQTFVZElBUjBNSEl3Y'\
                '0FZSkt3WUJCQUdCN0MwRE1HTXdZUVlJS3dZQkJRVUhBZ0VXVldoMGRIQTZM'\
                'eTloWTNOaGRDNXBiWEJ5Wlc1ellXOW1hV05wWVd3dVkyOXRMbUp5TDNKbGN'\
                'HOXphWFJ2Y21sdkwyUndZeTloWTNOaGRITmxabUY2YzNBdlpIQmpYMkZqYz'\
                'JGMGMyVm1ZWHB6Y0M1d1pHWXdhd1lEVlIwZkJHUXdZakJnb0Y2Z1hJWmFhS'\
                'FIwY0RvdkwyRmpjMkYwTFhSbGMzUmxMbWx0Y0hKbGJuTmhiMlpwWTJsaGJD'\
                'NWpiMjB1WW5JdmNtVndiM05wZEc5eWFXOHZiR055TDJGamMyRjBjMlZtWVh'\
                'wemNDOWhZM05oZEhObFptRjZjM0JqY213dVkzSnNNSUdtQmdnckJnRUZCUW'\
                'NCQVFTQm1UQ0JsakEwQmdnckJnRUZCUWN3QVlZb2FIUjBjRG92TDI5amMzQ'\
                'XRjR2xzYjNRdWFXMXdjbVZ1YzJGdlptbGphV0ZzTG1OdmJTNWljakJlQmdn'\
                'ckJnRUZCUWN3QW9aU2FIUjBjRG92TDJGamMyRjBMWFJsYzNSbExtbHRjSEp'\
                'sYm5OaGIyWnBZMmxoYkM1amIyMHVZbkl2Y21Wd2IzTnBkRzl5YVc4dlkyVn'\
                'lkR2xtYVdOaFpHOXpMMkZqYzJGMExYUmxjM1JsTG5BM1l6QVRCZ05WSFNVR'\
                'UREQUtCZ2dyQmdFRkJRY0RBakFKQmdOVkhSTUVBakFBTUNRR0ExVWRFUVFk'\
                'TUJ1Z0dRWUZZRXdCQXdPZ0VBUU9NRGczTWpNeU1UZ3dNREF4T0RZd0h3WUR'\
                'WUjBqQkJnd0ZvQVVqamxCQUZ6eXVBWGFxRzJZdVFGR2JXNWozd0l3RFFZSk'\
                'tvWklodmNOQVFFTEJRQURnZ0lCQUVteU51MkpiUmY3Z2VNb3BXUEFXZ2Fzc'\
                'HhWT0NRejU2UC9pQTB4V21FcGVheVBqU3pQTkZyNzlGcEVIRUY1Ynk0aXQw'\
                'eGlIajNjWm1Ybm1rVE5WRFhTeDAzQzFTTk9CeTZwOXA1cHM4YnZTTWxZVm1'\
                'peXI1QzdzanA5QWN2UzkyQlhla05hemNyL2NIc1RVbWxHVEhaUm13V1lrZE'\
                '56YVZMTWdRSjVSeUxuV1B5YWNQNktNdXVVK3kxU2pncktIY3NlYXc5ODdOS'\
                'E8ycS9mQ1JMNUxnZy9PNmFBMnNGUC9RTU8zV3VBRXpJQlBUMGs5ZzgwTDRE'\
                'bm5aQklueVU1amRHQjYvQ3ZaaGQ3bGF1Nm5jUVpQbDRjbnIrWTZEcjRUWjF'\
                '5dEEvTXBmMi9NSmpXOHc1WHF0YXRnUkNsM0RaN1c3RDVUaHhJVzdvQm5OYn'\
                'RranZva0gzOE9TUUpnK0Z2dGQ3QWI2YjBvOFJEeXhWalVpNUtsYSs0Q0F4W'\
                'nMxMHZ5VzRCa0Q3ZkZrdGlUelNQc3lTdHFiaW5zV2lQVy9Yek5tbG1DWCtQ'\
                'RHNRbWthemlveDRNSFEyWFBGUm5nQkxMalpPQldUTmRNUG8rekRUeWZHOWp'\
                'WQWVMRXI0dnRZL3pSSVRQNUk1R2s3YzBWR2k3dVVVZ3FzcWRsdUgreWdIcX'\
                'M1MmxObzFveExZbU9EVUZxMXhlamdtR3U0Q01jSmh6M1J1RmpYRFg2QlVjM'\
                'FUwY0pidnR6RVRLcTVwc09Za2xabUE0blNIZVdFNHA1eEkxbzAvOERLRWZF'\
                'czRHdEltSUJZUHViVVNMRW9HRm5ERjQ1UGVRVTdjSSt5TUlZcmN0NUN6bjB'\
                'NNTJsLzc3YW5jKzlOeUlHaStsQ1ZXL0lIZkVaYXdZemlNaVVVaUJ4PC9YNT'\
                'A5Q2VydGlmaWNhdGU+PC9YNTA5RGF0YT48L0tleUluZm8+PC9TaWduYXR1c'\
                'mU+PC9DRmU+|'\
                '20150912101513|'\
                '000000|'\
                'CFe35150908723218000186599000040190000007972068',
    ]


RESP_FALHA = [
        u'123456|09001|Código de ativação inválido||',
        u'123456|09002|SAT ainda não ativado||',
        u'123456|09098|SAT em processamento. Tente novamente.||',
        u'123456|09099|Erro desconhecido||',
    ]


RESP_INVALIDAS = [
        u'Resposta sem nenhum separador',
        u'Numero inesperado de campos|a|b|c|d|e|f|g|h|i|j|k',
    ]


def test_resposta_testefimafim():
    resposta = RespostaTesteFimAFim.analisar(RESP_SUCESSO[0])
    assert resposta.numeroSessao == 31545
    assert resposta.EEEEE == '09000'
    assert resposta.arquivoCFeBase64 == base64.b64encode(XML_TESTE_ASSINADO)
    assert resposta.timeStamp == as_datetime('20150912101513')
    assert resposta.numDocFiscal == 0
    assert resposta.chaveConsulta == 'CFe35150908723218000186599000040190000007972068'

    for retorno in RESP_FALHA:
        with pytest.raises(ExcecaoRespostaSAT):
            resposta = RespostaTesteFimAFim.analisar(retorno)

    for retorno in RESP_INVALIDAS:
        with pytest.raises(ErroRespostaSATInvalida):
            resposta = RespostaTesteFimAFim.analisar(retorno)


@pytest.mark.skipif(
        pytest.config.getoption('--skip-testefimafim') or
        pytest.config.getoption('--skip-funcoes-sat'),
        reason='Funcao `TesteFimAFim` explicitamente ignorada')
def test_funcao_testefimafim(clientesatlocal, cfevenda):
    resposta = clientesatlocal.teste_fim_a_fim(cfevenda)
    assert resposta.EEEEE == '09000'
    assert resposta.numDocFiscal == 0
    assert len(resposta.chaveConsulta) == 47
    assert resposta.chaveConsulta.startswith('CFe')


XML_TESTE = '<?xml version="1.0" encoding="UTF-8"?><CFe><infCFe versaoDadosE'\
    'nt="0.06"><ide><CNPJ>16716114000172</CNPJ><signAC>SGR-SAT SISTEMA DE GE'\
    'STAO E RETAGUARDA DO SAT</signAC><numeroCaixa>099</numeroCaixa></ide><e'\
    'mit><CNPJ>08723218000186</CNPJ><IE>149626224113</IE><cRegTribISSQN>1</c'\
    'RegTribISSQN><indRatISSQN>N</indRatISSQN></emit><dest><CNPJ>16716114000'\
    '172</CNPJ></dest><det nItem="1"><prod><cProd>001</cProd><xProd>MiniPc T'\
    'anca</xProd><CFOP>5001</CFOP><uCom>UN</uCom><qCom>1.0000</qCom><vUnCom>'\
    '654.320</vUnCom><indRegra>A</indRegra></prod><imposto><vItem12741>1.00<'\
    '/vItem12741><ICMS><ICMS00><Orig>0</Orig><CST>00</CST><pICMS>12.00</pICM'\
    'S></ICMS00></ICMS><PIS><PISAliq><CST>01</CST><vBC>654.32</vBC><pPIS>0.0'\
    '600</pPIS></PISAliq></PIS><COFINS><COFINSAliq><CST>01</CST><vBC>654.32<'\
    '/vBC><pCOFINS>0.0400</pCOFINS></COFINSAliq></COFINS></imposto></det><to'\
    'tal><vCFeLei12741>1.00</vCFeLei12741></total><pgto><MP><cMP>01</cMP><vM'\
    'P>2000.00</vMP></MP></pgto></infCFe></CFe>'


XML_TESTE_ASSINADO = '<CFe><infCFe versaoDadosEnt="0.06" versao="0.06" versa'\
    'oSB="010000" Id="CFe35150908723218000186599000040190000007972068"><ide>'\
    '<cUF>35</cUF><cNF>797206</cNF><mod>59</mod><nserieSAT>900004019</nserie'\
    'SAT><nCFe>000000</nCFe><dEmi>20150912</dEmi><hEmi>101513</hEmi><cDV>8</'\
    'cDV><tpAmb>2</tpAmb><CNPJ>16716114000172</CNPJ><signAC>SGR-SAT SISTEMA '\
    'DE GESTAO E RETAGUARDA DO SAT</signAC><assinaturaQRCODE>leKeG6JcB6z3Ehy'\
    'eNoDkWdpUzwBlkIhN3frYZHbtbc57ytCXOkUhOO+tSw85qeU8qUnN/NPWzSILzxr7FXXh8G'\
    'uHX8Wp3PKSK1ZQdCoBNRZJQr60HY+2jdH+3vWzt8ZVM9IEdOIAtPW4/q8Gs4P/5EYyTPikn'\
    'n0lsNdPNi79ubX8QaV58MJQYBtpxLonBEDdTU0UqZuSrB5w2Fj0QHd2Q0Pq6i+RYVI+A+4d'\
    '79JkuKsznSisqxK3efqIw8mOyFRLUILeiLkomQHwy/GYqT5ZLvgJkhLsczrVpzcPsRSwOIw'\
    'x3OaII+CEU/6Vycm+EMTIoSJOuiqF5JYVPfDkXcAW9g==</assinaturaQRCODE><numero'\
    'Caixa>099</numeroCaixa></ide><emit><CNPJ>08723218000186</CNPJ><xNome>TA'\
    'NCA INFORMATICA EIRELI</xNome><xFant>TANCA</xFant><enderEmit><xLgr>RUA '\
    'ENGENHEIRO JORGE OLIVA</xLgr><nro>73</nro><xBairro>VILA MASCOTE</xBairr'\
    'o><xMun>SAO PAULO</xMun><CEP>04362060</CEP></enderEmit><IE>149626224113'\
    '</IE><cRegTrib>3</cRegTrib><cRegTribISSQN>1</cRegTribISSQN><indRatISSQN'\
    '>N</indRatISSQN></emit><dest><CNPJ>16716114000172</CNPJ></dest><det nIt'\
    'em="1"><prod><cProd>001</cProd><xProd>MiniPc Tanca</xProd><CFOP>5001</C'\
    'FOP><uCom>UN</uCom><qCom>1.0000</qCom><vUnCom>654.320</vUnCom><vProd>65'\
    '4.32</vProd><indRegra>A</indRegra><vItem>654.32</vItem><vRatDesc>0.00</'\
    'vRatDesc><vRatAcr>0.00</vRatAcr></prod><imposto><vItem12741>1.00</vItem'\
    '12741><ICMS><ICMS00><Orig>0</Orig><CST>00</CST><pICMS>12.00</pICMS><vIC'\
    'MS>78.52</vICMS></ICMS00></ICMS><PIS><PISAliq><CST>01</CST><vBC>654.32<'\
    '/vBC><pPIS>0.0600</pPIS><vPIS>39.26</vPIS></PISAliq></PIS><COFINS><COFI'\
    'NSAliq><CST>01</CST><vBC>654.32</vBC><pCOFINS>0.0400</pCOFINS><vCOFINS>'\
    '26.17</vCOFINS></COFINSAliq></COFINS></imposto></det><total><ICMSTot><v'\
    'ICMS>78.52</vICMS><vProd>654.32</vProd><vDesc>0.00</vDesc><vPIS>39.26</'\
    'vPIS><vCOFINS>26.17</vCOFINS><vPISST>0.00</vPISST><vCOFINSST>0.00</vCOF'\
    'INSST><vOutro>0.00</vOutro></ICMSTot><vCFe>654.32</vCFe><vCFeLei12741>1'\
    '.00</vCFeLei12741></total><pgto><MP><cMP>01</cMP><vMP>2000.00</vMP></MP'\
    '><vTroco>1345.68</vTroco></pgto><infAdic><obsFisco xCampo="xCampo1"><xT'\
    'exto>xTexto1</xTexto></obsFisco></infAdic></infCFe><Signature xmlns="ht'\
    'tp://www.w3.org/2000/09/xmldsig#"><SignedInfo><CanonicalizationMethod A'\
    'lgorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/><SignatureM'\
    'ethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/><R'\
    'eference URI="#CFe35150908723218000186599000040190000007972068"><Transf'\
    'orms><Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-'\
    'signature"/><Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14'\
    'n-20010315"/></Transforms><DigestMethod Algorithm="http://www.w3.org/20'\
    '01/04/xmlenc#sha256"/><DigestValue>8idRQyi+MVQO/UatrdYnuQsaav7X8tuvV0Ch'\
    'mENVDm4=</DigestValue></Reference></SignedInfo><SignatureValue>O7eoj+iO'\
    'PflXVPd53NUGNmc5PAnNjv++vqtQ+dQMs97Cl5kVjEfZuNJq/+V4CAMzYiYCW7F3QQXNk2n'\
    '7iz6Q2V/paHU+V1Q/c/TjI0Pz9VygQcou6PVV/VTQrkAPMHzxO9nRm8riNnTkWAR6cxpj1x'\
    'QtfFZA+awBKY2Zov1/zu3520Hlum6AAq0WqxcKAx97dHQUMHkd0BdIBwBGyDiaBVUbkESJQ'\
    'jdxehB8h9WPRoqtbnWJ/w10cC8/aNSCfVugDu/Fk+xZJi4J6eYbJU3HM7C15L4vColnXkRd'\
    'DMKe3yrLtd8BW0unxMwomnxtXbufHU7/W5qyj/R2SiN5ViKj0w==</SignatureValue><K'\
    'eyInfo><X509Data><X509Certificate>MIIGsDCCBJigAwIBAgIJARjgvIzmd2BGMA0GC'\
    'SqGSIb3DQEBCwUAMGcxCzAJBgNVBAYTAkJSMTUwMwYDVQQKEyxTZWNyZXRhcmlhIGRhIEZh'\
    'emVuZGEgZG8gRXN0YWRvIGRlIFNhbyBQYXVsbzEhMB8GA1UEAxMYQUMgU0FUIGRlIFRlc3R'\
    'lIFNFRkFaIFNQMB4XDTE1MDcwODE1MzYzNloXDTIwMDcwODE1MzYzNlowgbUxEjAQBgNVBA'\
    'UTCTkwMDAwNDAxOTELMAkGA1UEBhMCQlIxEjAQBgNVBAgTCVNBTyBQQVVMTzERMA8GA1UEC'\
    'hMIU0VGQVotU1AxDzANBgNVBAsTBkFDLVNBVDEoMCYGA1UECxMfQXV0ZW50aWNhZG8gcG9y'\
    'IEFSIFNFRkFaIFNQIFNBVDEwMC4GA1UEAxMnVEFOQ0EgSU5GT1JNQVRJQ0EgRUlSRUxJOjA'\
    '4NzIzMjE4MDAwMTg2MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl89PfjfjZy'\
    '0QatgBzvV+Du04ekjbiYmnVe5S9AHNiexno8Vdp9B79hwLKiDrvvwAtVqrocWOQmM3SIx5O'\
    'ECy/vvFi46wawJT9Y2a4zuEFGvHZSuE/Up3PB52dP34aGbplis0d1RqIoXoKWq+FljWs+N8'\
    '9rwvPxgJGafGp3e3t8CqIjqBPSCX8Bmy/2YDj1C/J1CLW91q94qVX0CxhKFHAwfgIKe7ZHe'\
    'Zpws2jiOmtLFWKofCSaconQu5PHUVzOv7kTpK8ZbvsvnzwLwHa6/rDJsORW/33V+ryfuDtR'\
    'H+nos3usE/avc/8mU25q3rj7fTNax4ggb6rpFtSyTAWRkFZQIDAQABo4ICDjCCAgowDgYDV'\
    'R0PAQH/BAQDAgXgMHsGA1UdIAR0MHIwcAYJKwYBBAGB7C0DMGMwYQYIKwYBBQUHAgEWVWh0'\
    'dHA6Ly9hY3NhdC5pbXByZW5zYW9maWNpYWwuY29tLmJyL3JlcG9zaXRvcmlvL2RwYy9hY3N'\
    'hdHNlZmF6c3AvZHBjX2Fjc2F0c2VmYXpzcC5wZGYwawYDVR0fBGQwYjBgoF6gXIZaaHR0cD'\
    'ovL2Fjc2F0LXRlc3RlLmltcHJlbnNhb2ZpY2lhbC5jb20uYnIvcmVwb3NpdG9yaW8vbGNyL'\
    '2Fjc2F0c2VmYXpzcC9hY3NhdHNlZmF6c3BjcmwuY3JsMIGmBggrBgEFBQcBAQSBmTCBljA0'\
    'BggrBgEFBQcwAYYoaHR0cDovL29jc3AtcGlsb3QuaW1wcmVuc2FvZmljaWFsLmNvbS5icjB'\
    'eBggrBgEFBQcwAoZSaHR0cDovL2Fjc2F0LXRlc3RlLmltcHJlbnNhb2ZpY2lhbC5jb20uYn'\
    'IvcmVwb3NpdG9yaW8vY2VydGlmaWNhZG9zL2Fjc2F0LXRlc3RlLnA3YzATBgNVHSUEDDAKB'\
    'ggrBgEFBQcDAjAJBgNVHRMEAjAAMCQGA1UdEQQdMBugGQYFYEwBAwOgEAQOMDg3MjMyMTgw'\
    'MDAxODYwHwYDVR0jBBgwFoAUjjlBAFzyuAXaqG2YuQFGbW5j3wIwDQYJKoZIhvcNAQELBQA'\
    'DggIBAEmyNu2JbRf7geMopWPAWgaspxVOCQz56P/iA0xWmEpeayPjSzPNFr79FpEHEF5by4'\
    'it0xiHj3cZmXnmkTNVDXSx03C1SNOBy6p9p5ps8bvSMlYVmiyr5C7sjp9AcvS92BXekNazc'\
    'r/cHsTUmlGTHZRmwWYkdNzaVLMgQJ5RyLnWPyacP6KMuuU+y1SjgrKHcseaw987NHO2q/fC'\
    'RL5Lgg/O6aA2sFP/QMO3WuAEzIBPT0k9g80L4DnnZBInyU5jdGB6/CvZhd7lau6ncQZPl4c'\
    'nr+Y6Dr4TZ1ytA/Mpf2/MJjW8w5XqtatgRCl3DZ7W7D5ThxIW7oBnNbtkjvokH38OSQJg+F'\
    'vtd7Ab6b0o8RDyxVjUi5Kla+4CAxZs10vyW4BkD7fFktiTzSPsyStqbinsWiPW/XzNmlmCX'\
    '+PDsQmkaziox4MHQ2XPFRngBLLjZOBWTNdMPo+zDTyfG9jVAeLEr4vtY/zRITP5I5Gk7c0V'\
    'Gi7uUUgqsqdluH+ygHqs52lNo1oxLYmODUFq1xejgmGu4CMcJhz3RuFjXDX6BUc0U0cJbvt'\
    'zETKq5psOYklZmA4nSHeWE4p5xI1o0/8DKEfEs4GtImIBYPubUSLEoGFnDF45PeQU7cI+yM'\
    'IYrct5Czn0M52l/77anc+9NyIGi+lCVW/IHfEZawYziMiUUiBx</X509Certificate></X'\
    '509Data></KeyInfo></Signature></CFe>'
