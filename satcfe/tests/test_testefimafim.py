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
import xml.etree.ElementTree as ET

import pytest

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaTesteFimAFim
from satcfe.util import as_datetime
from satcfe.util import str_to_base64


# RESP_SUCESSO = [
#         u'031545|09000|Emitido com sucesso|||'
#                 'PENGZT48aW5mQ0ZlIHZlcnNhb0RhZG9zRW50PSIwLjA2IiB2ZXJzYW89IjA'\
#                 'uMDYiIHZlcnNhb1NCPSIwMTAwMDAiIElkPSJDRmUzNTE1MDkwODcyMzIxOD'\
#                 'AwMDE4NjU5OTAwMDA0MDE5MDAwMDAwNzk3MjA2OCI+PGlkZT48Y1VGPjM1P'\
#                 'C9jVUY+PGNORj43OTcyMDY8L2NORj48bW9kPjU5PC9tb2Q+PG5zZXJpZVNB'\
#                 'VD45MDAwMDQwMTk8L25zZXJpZVNBVD48bkNGZT4wMDAwMDA8L25DRmU+PGR'\
#                 'FbWk+MjAxNTA5MTI8L2RFbWk+PGhFbWk+MTAxNTEzPC9oRW1pPjxjRFY+OD'\
#                 'wvY0RWPjx0cEFtYj4yPC90cEFtYj48Q05QSj4xNjcxNjExNDAwMDE3MjwvQ'\
#                 '05QSj48c2lnbkFDPlNHUi1TQVQgU0lTVEVNQSBERSBHRVNUQU8gRSBSRVRB'\
#                 'R1VBUkRBIERPIFNBVDwvc2lnbkFDPjxhc3NpbmF0dXJhUVJDT0RFPmxlS2V'\
#                 'HNkpjQjZ6M0VoeWVOb0RrV2RwVXp3QmxrSWhOM2ZyWVpIYnRiYzU3eXRDWE'\
#                 '9rVWhPTyt0U3c4NXFlVThxVW5OL05QV3pTSUx6eHI3RlhYaDhHdUhYOFdwM'\
#                 '1BLU0sxWlFkQ29CTlJaSlFyNjBIWSsyamRIKzN2V3p0OFpWTTlJRWRPSUF0'\
#                 'UFc0L3E4R3M0UC81RVl5VFBpa25uMGxzTmRQTmk3OXViWDhRYVY1OE1KUVl'\
#                 'CdHB4TG9uQkVEZFRVMFVxWnVTckI1dzJGajBRSGQyUTBQcTZpK1JZVkkrQS'\
#                 's0ZDc5Smt1S3N6blNpc3F4SzNlZnFJdzhtT3lGUkxVSUxlaUxrb21RSHd5L'\
#                 '0dZcVQ1Wkx2Z0praExzY3pyVnB6Y1BzUlN3T0l3eDNPYUlJK0NFVS82Vnlj'\
#                 'bStFTVRJb1NKT3VpcUY1SllWUGZEa1hjQVc5Zz09PC9hc3NpbmF0dXJhUVJ'\
#                 'DT0RFPjxudW1lcm9DYWl4YT4wOTk8L251bWVyb0NhaXhhPjwvaWRlPjxlbW'\
#                 'l0PjxDTlBKPjA4NzIzMjE4MDAwMTg2PC9DTlBKPjx4Tm9tZT5UQU5DQSBJT'\
#                 'kZPUk1BVElDQSBFSVJFTEk8L3hOb21lPjx4RmFudD5UQU5DQTwveEZhbnQ+'\
#                 'PGVuZGVyRW1pdD48eExncj5SVUEgRU5HRU5IRUlSTyBKT1JHRSBPTElWQTw'\
#                 'veExncj48bnJvPjczPC9ucm8+PHhCYWlycm8+VklMQSBNQVNDT1RFPC94Qm'\
#                 'FpcnJvPjx4TXVuPlNBTyBQQVVMTzwveE11bj48Q0VQPjA0MzYyMDYwPC9DR'\
#                 'VA+PC9lbmRlckVtaXQ+PElFPjE0OTYyNjIyNDExMzwvSUU+PGNSZWdUcmli'\
#                 'PjM8L2NSZWdUcmliPjxjUmVnVHJpYklTU1FOPjE8L2NSZWdUcmliSVNTUU4'\
#                 '+PGluZFJhdElTU1FOPk48L2luZFJhdElTU1FOPjwvZW1pdD48ZGVzdD48Q0'\
#                 '5QSj4xNjcxNjExNDAwMDE3MjwvQ05QSj48L2Rlc3Q+PGRldCBuSXRlbT0iM'\
#                 'SI+PHByb2Q+PGNQcm9kPjAwMTwvY1Byb2Q+PHhQcm9kPk1pbmlQYyBUYW5j'\
#                 'YTwveFByb2Q+PENGT1A+NTAwMTwvQ0ZPUD48dUNvbT5VTjwvdUNvbT48cUN'\
#                 'vbT4xLjAwMDA8L3FDb20+PHZVbkNvbT42NTQuMzIwPC92VW5Db20+PHZQcm'\
#                 '9kPjY1NC4zMjwvdlByb2Q+PGluZFJlZ3JhPkE8L2luZFJlZ3JhPjx2SXRlb'\
#                 'T42NTQuMzI8L3ZJdGVtPjx2UmF0RGVzYz4wLjAwPC92UmF0RGVzYz48dlJh'\
#                 'dEFjcj4wLjAwPC92UmF0QWNyPjwvcHJvZD48aW1wb3N0bz48dkl0ZW0xMjc'\
#                 '0MT4xLjAwPC92SXRlbTEyNzQxPjxJQ01TPjxJQ01TMDA+PE9yaWc+MDwvT3'\
#                 'JpZz48Q1NUPjAwPC9DU1Q+PHBJQ01TPjEyLjAwPC9wSUNNUz48dklDTVM+N'\
#                 'zguNTI8L3ZJQ01TPjwvSUNNUzAwPjwvSUNNUz48UElTPjxQSVNBbGlxPjxD'\
#                 'U1Q+MDE8L0NTVD48dkJDPjY1NC4zMjwvdkJDPjxwUElTPjAuMDYwMDwvcFB'\
#                 'JUz48dlBJUz4zOS4yNjwvdlBJUz48L1BJU0FsaXE+PC9QSVM+PENPRklOUz'\
#                 '48Q09GSU5TQWxpcT48Q1NUPjAxPC9DU1Q+PHZCQz42NTQuMzI8L3ZCQz48c'\
#                 'ENPRklOUz4wLjA0MDA8L3BDT0ZJTlM+PHZDT0ZJTlM+MjYuMTc8L3ZDT0ZJ'\
#                 'TlM+PC9DT0ZJTlNBbGlxPjwvQ09GSU5TPjwvaW1wb3N0bz48L2RldD48dG9'\
#                 '0YWw+PElDTVNUb3Q+PHZJQ01TPjc4LjUyPC92SUNNUz48dlByb2Q+NjU0Lj'\
#                 'MyPC92UHJvZD48dkRlc2M+MC4wMDwvdkRlc2M+PHZQSVM+MzkuMjY8L3ZQS'\
#                 'VM+PHZDT0ZJTlM+MjYuMTc8L3ZDT0ZJTlM+PHZQSVNTVD4wLjAwPC92UElT'\
#                 'U1Q+PHZDT0ZJTlNTVD4wLjAwPC92Q09GSU5TU1Q+PHZPdXRybz4wLjAwPC9'\
#                 '2T3V0cm8+PC9JQ01TVG90Pjx2Q0ZlPjY1NC4zMjwvdkNGZT48dkNGZUxlaT'\
#                 'EyNzQxPjEuMDA8L3ZDRmVMZWkxMjc0MT48L3RvdGFsPjxwZ3RvPjxNUD48Y'\
#                 '01QPjAxPC9jTVA+PHZNUD4yMDAwLjAwPC92TVA+PC9NUD48dlRyb2NvPjEz'\
#                 'NDUuNjg8L3ZUcm9jbz48L3BndG8+PGluZkFkaWM+PG9ic0Zpc2NvIHhDYW1'\
#                 'wbz0ieENhbXBvMSI+PHhUZXh0bz54VGV4dG8xPC94VGV4dG8+PC9vYnNGaX'\
#                 'Njbz48L2luZkFkaWM+PC9pbmZDRmU+PFNpZ25hdHVyZSB4bWxucz0iaHR0c'\
#                 'DovL3d3dy53My5vcmcvMjAwMC8wOS94bWxkc2lnIyI+PFNpZ25lZEluZm8+'\
#                 'PENhbm9uaWNhbGl6YXRpb25NZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d'\
#                 '3LnczLm9yZy9UUi8yMDAxL1JFQy14bWwtYzE0bi0yMDAxMDMxNSIvPjxTaW'\
#                 'duYXR1cmVNZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yM'\
#                 'DAxLzA0L3htbGRzaWctbW9yZSNyc2Etc2hhMjU2Ii8+PFJlZmVyZW5jZSBV'\
#                 'Ukk9IiNDRmUzNTE1MDkwODcyMzIxODAwMDE4NjU5OTAwMDA0MDE5MDAwMDA'\
#                 'wNzk3MjA2OCI+PFRyYW5zZm9ybXM+PFRyYW5zZm9ybSBBbGdvcml0aG09Im'\
#                 'h0dHA6Ly93d3cudzMub3JnLzIwMDAvMDkveG1sZHNpZyNlbnZlbG9wZWQtc'\
#                 '2lnbmF0dXJlIi8+PFRyYW5zZm9ybSBBbGdvcml0aG09Imh0dHA6Ly93d3cu'\
#                 'dzMub3JnL1RSLzIwMDEvUkVDLXhtbC1jMTRuLTIwMDEwMzE1Ii8+PC9UcmF'\
#                 'uc2Zvcm1zPjxEaWdlc3RNZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d3Ln'\
#                 'czLm9yZy8yMDAxLzA0L3htbGVuYyNzaGEyNTYiLz48RGlnZXN0VmFsdWU+O'\
#                 'GlkUlF5aStNVlFPL1VhdHJkWW51UXNhYXY3WDh0dXZWMENobUVOVkRtND08'\
#                 'L0RpZ2VzdFZhbHVlPjwvUmVmZXJlbmNlPjwvU2lnbmVkSW5mbz48U2lnbmF'\
#                 '0dXJlVmFsdWU+Tzdlb2oraU9QZmxYVlBkNTNOVUdObWM1UEFuTmp2Kyt2cX'\
#                 'RRK2RRTXM5N0NsNWtWakVmWnVOSnEvK1Y0Q0FNellpWUNXN0YzUVFYTmsyb'\
#                 'jdpejZRMlYvcGFIVStWMVEvYy9UakkwUHo5VnlnUWNvdTZQVlYvVlRRcmtB'\
#                 'UE1IenhPOW5SbThyaU5uVGtXQVI2Y3hwajF4UXRmRlpBK2F3QktZMlpvdjE'\
#                 'venUzNTIwSGx1bTZBQXEwV3F4Y0tBeDk3ZEhRVU1Ia2QwQmRJQndCR3lEaW'\
#                 'FCVlVia0VTSlFqZHhlaEI4aDlXUFJvcXRibldKL3cxMGNDOC9hTlNDZlZ1Z'\
#                 '0R1L0ZrK3haSmk0SjZlWWJKVTNITTdDMTVMNHZDb2xuWGtSZERNS2UzeXJM'\
#                 'dGQ4QlcwdW54TXdvbW54dFhidWZIVTcvVzVxeWovUjJTaU41VmlLajB3PT0'\
#                 '8L1NpZ25hdHVyZVZhbHVlPjxLZXlJbmZvPjxYNTA5RGF0YT48WDUwOUNlcn'\
#                 'RpZmljYXRlPk1JSUdzRENDQkppZ0F3SUJBZ0lKQVJqZ3ZJem1kMkJHTUEwR'\
#                 '0NTcUdTSWIzRFFFQkN3VUFNR2N4Q3pBSkJnTlZCQVlUQWtKU01UVXdNd1lE'\
#                 'VlFRS0V5eFRaV055WlhSaGNtbGhJR1JoSUVaaGVtVnVaR0VnWkc4Z1JYTjB'\
#                 'ZV1J2SUdSbElGTmhieUJRWVhWc2J6RWhNQjhHQTFVRUF4TVlRVU1nVTBGVU'\
#                 'lHUmxJRlJsYzNSbElGTkZSa0ZhSUZOUU1CNFhEVEUxTURjd09ERTFNell6T'\
#                 'mxvWERUSXdNRGN3T0RFMU16WXpObG93Z2JVeEVqQVFCZ05WQkFVVENUa3dN'\
#                 'REF3TkRBeE9URUxNQWtHQTFVRUJoTUNRbEl4RWpBUUJnTlZCQWdUQ1ZOQlR'\
#                 '5QlFRVlZNVHpFUk1BOEdBMVVFQ2hNSVUwVkdRVm90VTFBeER6QU5CZ05WQk'\
#                 'FzVEJrRkRMVk5CVkRFb01DWUdBMVVFQ3hNZlFYVjBaVzUwYVdOaFpHOGdjR'\
#                 'zl5SUVGU0lGTkZSa0ZhSUZOUUlGTkJWREV3TUM0R0ExVUVBeE1uVkVGT1Ew'\
#                 'RWdTVTVHVDFKTlFWUkpRMEVnUlVsU1JVeEpPakE0TnpJek1qRTRNREF3TVR'\
#                 'nMk1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUU'\
#                 'VBbDg5UGZqZmpaeTBRYXRnQnp2VitEdTA0ZWtqYmlZbW5WZTVTOUFITmlle'\
#                 'G5vOFZkcDlCNzlod0xLaURydnZ3QXRWcXJvY1dPUW1NM1NJeDVPRUN5L3Z2'\
#                 'Rmk0Nndhd0pUOVkyYTR6dUVGR3ZIWlN1RS9VcDNQQjUyZFAzNGFHYnBsaXM'\
#                 'wZDFScUlvWG9LV3ErRmxqV3MrTjg5cnd2UHhnSkdhZkdwM2UzdDhDcUlqcU'\
#                 'JQU0NYOEJteS8yWURqMUMvSjFDTFc5MXE5NHFWWDBDeGhLRkhBd2ZnSUtlN'\
#                 '1pIZVpwd3MyamlPbXRMRldLb2ZDU2Fjb25RdTVQSFVWek92N2tUcEs4WmJ2'\
#                 'c3ZuendMd0hhNi9yREpzT1JXLzMzVityeWZ1RHRSSCtub3MzdXNFL2F2Yy8'\
#                 '4bVUyNXEzcmo3ZlROYXg0Z2diNnJwRnRTeVRBV1JrRlpRSURBUUFCbzRJQ0'\
#                 'RqQ0NBZ293RGdZRFZSMFBBUUgvQkFRREFnWGdNSHNHQTFVZElBUjBNSEl3Y'\
#                 '0FZSkt3WUJCQUdCN0MwRE1HTXdZUVlJS3dZQkJRVUhBZ0VXVldoMGRIQTZM'\
#                 'eTloWTNOaGRDNXBiWEJ5Wlc1ellXOW1hV05wWVd3dVkyOXRMbUp5TDNKbGN'\
#                 'HOXphWFJ2Y21sdkwyUndZeTloWTNOaGRITmxabUY2YzNBdlpIQmpYMkZqYz'\
#                 'JGMGMyVm1ZWHB6Y0M1d1pHWXdhd1lEVlIwZkJHUXdZakJnb0Y2Z1hJWmFhS'\
#                 'FIwY0RvdkwyRmpjMkYwTFhSbGMzUmxMbWx0Y0hKbGJuTmhiMlpwWTJsaGJD'\
#                 'NWpiMjB1WW5JdmNtVndiM05wZEc5eWFXOHZiR055TDJGamMyRjBjMlZtWVh'\
#                 'wemNDOWhZM05oZEhObFptRjZjM0JqY213dVkzSnNNSUdtQmdnckJnRUZCUW'\
#                 'NCQVFTQm1UQ0JsakEwQmdnckJnRUZCUWN3QVlZb2FIUjBjRG92TDI5amMzQ'\
#                 'XRjR2xzYjNRdWFXMXdjbVZ1YzJGdlptbGphV0ZzTG1OdmJTNWljakJlQmdn'\
#                 'ckJnRUZCUWN3QW9aU2FIUjBjRG92TDJGamMyRjBMWFJsYzNSbExtbHRjSEp'\
#                 'sYm5OaGIyWnBZMmxoYkM1amIyMHVZbkl2Y21Wd2IzTnBkRzl5YVc4dlkyVn'\
#                 'lkR2xtYVdOaFpHOXpMMkZqYzJGMExYUmxjM1JsTG5BM1l6QVRCZ05WSFNVR'\
#                 'UREQUtCZ2dyQmdFRkJRY0RBakFKQmdOVkhSTUVBakFBTUNRR0ExVWRFUVFk'\
#                 'TUJ1Z0dRWUZZRXdCQXdPZ0VBUU9NRGczTWpNeU1UZ3dNREF4T0RZd0h3WUR'\
#                 'WUjBqQkJnd0ZvQVVqamxCQUZ6eXVBWGFxRzJZdVFGR2JXNWozd0l3RFFZSk'\
#                 'tvWklodmNOQVFFTEJRQURnZ0lCQUVteU51MkpiUmY3Z2VNb3BXUEFXZ2Fzc'\
#                 'HhWT0NRejU2UC9pQTB4V21FcGVheVBqU3pQTkZyNzlGcEVIRUY1Ynk0aXQw'\
#                 'eGlIajNjWm1Ybm1rVE5WRFhTeDAzQzFTTk9CeTZwOXA1cHM4YnZTTWxZVm1'\
#                 'peXI1QzdzanA5QWN2UzkyQlhla05hemNyL2NIc1RVbWxHVEhaUm13V1lrZE'\
#                 '56YVZMTWdRSjVSeUxuV1B5YWNQNktNdXVVK3kxU2pncktIY3NlYXc5ODdOS'\
#                 'E8ycS9mQ1JMNUxnZy9PNmFBMnNGUC9RTU8zV3VBRXpJQlBUMGs5ZzgwTDRE'\
#                 'bm5aQklueVU1amRHQjYvQ3ZaaGQ3bGF1Nm5jUVpQbDRjbnIrWTZEcjRUWjF'\
#                 '5dEEvTXBmMi9NSmpXOHc1WHF0YXRnUkNsM0RaN1c3RDVUaHhJVzdvQm5OYn'\
#                 'RranZva0gzOE9TUUpnK0Z2dGQ3QWI2YjBvOFJEeXhWalVpNUtsYSs0Q0F4W'\
#                 'nMxMHZ5VzRCa0Q3ZkZrdGlUelNQc3lTdHFiaW5zV2lQVy9Yek5tbG1DWCtQ'\
#                 'RHNRbWthemlveDRNSFEyWFBGUm5nQkxMalpPQldUTmRNUG8rekRUeWZHOWp'\
#                 'WQWVMRXI0dnRZL3pSSVRQNUk1R2s3YzBWR2k3dVVVZ3FzcWRsdUgreWdIcX'\
#                 'M1MmxObzFveExZbU9EVUZxMXhlamdtR3U0Q01jSmh6M1J1RmpYRFg2QlVjM'\
#                 'FUwY0pidnR6RVRLcTVwc09Za2xabUE0blNIZVdFNHA1eEkxbzAvOERLRWZF'\
#                 'czRHdEltSUJZUHViVVNMRW9HRm5ERjQ1UGVRVTdjSSt5TUlZcmN0NUN6bjB'\
#                 'NNTJsLzc3YW5jKzlOeUlHaStsQ1ZXL0lIZkVaYXdZemlNaVVVaUJ4PC9YNT'\
#                 'A5Q2VydGlmaWNhdGU+PC9YNTA5RGF0YT48L0tleUluZm8+PC9TaWduYXR1c'\
#                 'mU+PC9DRmU+|'\
#                 '20150912101513|'\
#                 '000000|'\
#                 'CFe35150908723218000186599000040190000007972068',
#     ]


# RESP_FALHA = [
#         u'123456|09001|Código de ativação inválido||',
#         u'123456|09002|SAT ainda não ativado||',
#         u'123456|09098|SAT em processamento. Tente novamente.||',
#         u'123456|09099|Erro desconhecido||',
#     ]


# RESP_INVALIDAS = [
#         u'Resposta sem nenhum separador',
#         u'Numero inesperado de campos|a|b|c|d|e|f|g|h|i|j|k',
#     ]


def test_resposta_testefimafim(datadir):
    with open(datadir.join('respostas-de-sucesso.txt'), 'r') as fresp, \
         open(datadir.join('cfe-teste-assinado.xml'), 'r') as fxml:
        r_sucessos = fresp.read().splitlines()
        cfe_teste = fxml.read()

    _CFe = ET.fromstring(cfe_teste)
    _infCFe = _CFe.find('./infCFe')
    chave_consulta = _infCFe.attrib['Id']

    resposta = RespostaTesteFimAFim.analisar(r_sucessos[0])
    assert resposta.numeroSessao == 31545
    assert resposta.EEEEE == '09000'
    assert resposta.arquivoCFeBase64 == str_to_base64(cfe_teste)
    assert resposta.timeStamp == as_datetime('20150912101513')
    assert resposta.numDocFiscal == 0
    assert resposta.chaveConsulta == chave_consulta


def test_respostas_de_falha(datadir):
    with open(datadir.join('respostas-de-falha.txt'), 'r') as f:
        respostas = f.read().splitlines()
    for retorno in respostas:
        with pytest.raises(ExcecaoRespostaSAT):
            RespostaTesteFimAFim.analisar(retorno)


def test_respostas_invalidas(datadir):
    with open(datadir.join('respostas-invalidas.txt'), 'r') as f:
        respostas = f.read().splitlines()
    for retorno in respostas:
        with pytest.raises(ErroRespostaSATInvalida):
            RespostaTesteFimAFim.analisar(retorno)


@pytest.mark.skipif(
        pytest.config.getoption('--skip-testefimafim', default=True) or
        pytest.config.getoption('--skip-funcoes-sat', default=True),
        reason='Funcao `TesteFimAFim` explicitamente ignorada')
def test_funcao_testefimafim(clientesatlocal, cfevenda):
    resposta = clientesatlocal.teste_fim_a_fim(cfevenda)
    assert resposta.EEEEE == '09000'
    assert resposta.numDocFiscal == 0
    assert len(resposta.chaveConsulta) == 47
    assert resposta.chaveConsulta.startswith('CFe')
