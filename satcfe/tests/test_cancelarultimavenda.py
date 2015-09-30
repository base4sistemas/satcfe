# -*- coding: utf-8 -*-
#
# satcfe/tests/test_cancelarultimavenda.py
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

from decimal import Decimal

import pytest

from satcfe.entidades import CFeCancelamento
from satcfe.entidades import Destinatario
from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaCancelarUltimaVenda
from satcfe.util import as_datetime


RESP_SUCESSO = [
        # o conteúdo do XML em base64 nesta resposta foi contruído a partir
        # dos dados em XML_CFE_CANC_AUTORIZADO; o objetivo é testar o
        # tratamento da resposta e não a autenticidade do documento;
        u'123456|07000|0000|Cupom cancelado com sucesso + conteudo CF-e-SAT cancelado|||'
                'PD94bWwgdmVyc2lvbj0iMS4wIj8+CjxDRmVDYW5jPgogIDxpbmZDRmUKICA'\
                'gICAgICBJZD0iQ0ZlMzUxNTA5MDg3MjMyMTgwMDAxODY1OTkwMDAwNDAxOT'\
                'AwMDAzNzg1ODU0NzAiCiAgICAgICAgY2hDYW5jPSJDRmUzNTE1MDkwODcyM'\
                'zIxODAwMDE4NjU5OTAwMDA0MDE5MDAwMDM2MDUzOTk0OCIKICAgICAgICB2'\
                'ZXJzYW89IjAuMDYiPgogICAgPGRFbWk+MjAxNTA5MTE8L2RFbWk+CiAgICA'\
                '8aEVtaT4xNzU4NDA8L2hFbWk+CiAgICA8aWRlPgogICAgICA8Y1VGPjM1PC'\
                '9jVUY+CiAgICAgIDxjTkY+ODU4NTQ3PC9jTkY+CiAgICAgIDxtb2Q+NTk8L'\
                '21vZD4KICAgICAgPG5zZXJpZVNBVD45MDAwMDQwMTk8L25zZXJpZVNBVD4K'\
                'ICAgICAgPG5DRmU+MDAwMDM3PC9uQ0ZlPgogICAgICA8ZEVtaT4yMDE1MDk'\
                'xMTwvZEVtaT4KICAgICAgPGhFbWk+MTc1OTIxPC9oRW1pPgogICAgICA8Y0'\
                'RWPjA8L2NEVj4KICAgICAgPENOUEo+MTY3MTYxMTQwMDAxNzI8L0NOUEo+C'\
                'iAgICAgIDxzaWduQUM+U0dSLVNBVCBTSVNURU1BIERFIEdFU1RBTyBFIFJF'\
                'VEFHVUFSREEgRE8gU0FUPC9zaWduQUM+CiAgICAgIDxhc3NpbmF0dXJhUVJ'\
                'DT0RFPlVLSjc3VnlRMHRjK0VkTG01WmRBWUlMTXFYdlBTU0IrUUxZeiswWm'\
                'dKcFVoTk41QWNobll1QXJLUHpWVGlLcWJPYnR4YlI3bCtzNVgvVG1NR01Rd'\
                'zFUSXJ5cXY3QTBBejczTGFnVis2b1M1dWszeXZCYllSK3RXamZoK0pjbWt0'\
                'bGxZVlp2OFFWbytBWTd5Z2orbENxTGpmVWhNcUJ6VTRIYkp6QlFNeTdRUHR'\
                'DRXkyN3drN2MzUzNtVmNzbVdBTHhkM0g3bEhuWmoxd0orbGRoV0pwTlgxN2'\
                '8vNnNCME5jNmtzejRkWWtMUmZIaGVDc3BGeVRPUnRFMUFueStEYXNtbWFXO'\
                'Ek0ak5RZnJXbnhXYlF4T0ozenFpRS9wWWIvd2YvM3I4V3ZDMWx1UjV4ZGI5'\
                'a01lZGQrVE0wbFp3WlhuZFhrQWNRT0ZWTXE1Q2FZaWV0Vi9vZz09PC9hc3N'\
                'pbmF0dXJhUVJDT0RFPgogICAgICA8bnVtZXJvQ2FpeGE+MDAyPC9udW1lcm'\
                '9DYWl4YT4KICAgIDwvaWRlPgogICAgPGVtaXQ+CiAgICAgIDxDTlBKPjA4N'\
                'zIzMjE4MDAwMTg2PC9DTlBKPgogICAgICA8eE5vbWU+VEFOQ0EgSU5GT1JN'\
                'QVRJQ0EgRUlSRUxJPC94Tm9tZT4KICAgICAgPGVuZGVyRW1pdD4KICAgICA'\
                'gICA8eExncj5SVUEgRU5HRU5IRUlSTyBKT1JHRSBPTElWQTwveExncj4KIC'\
                'AgICAgICA8eEJhaXJybz5WSUxBIE1BU0NPVEU8L3hCYWlycm8+CiAgICAgI'\
                'CAgPHhNdW4+U0FPIFBBVUxPPC94TXVuPgogICAgICAgIDxDRVA+MDQzNjIw'\
                'NjA8L0NFUD4KICAgICAgPC9lbmRlckVtaXQ+CiAgICAgIDxJRT4xNDk2MjY'\
                'yMjQxMTM8L0lFPgogICAgICA8SU0+MTIzMTIzPC9JTT4KICAgIDwvZW1pdD'\
                '4KICAgIDxkZXN0Lz4KICAgIDx0b3RhbD4KICAgICAgPHZDRmU+Mi4wMDwvd'\
                'kNGZT4KICAgIDwvdG90YWw+CiAgICA8aW5mQWRpYz4KICAgICAgPG9ic0Zp'\
                'c2NvIHhDYW1wbz0ieENhbXBvMSI+CiAgICAgICAgPHhUZXh0bz54VGV4dG8'\
                'xPC94VGV4dG8+CiAgICAgIDwvb2JzRmlzY28+CiAgICA8L2luZkFkaWM+Ci'\
                'AgPC9pbmZDRmU+CiAgPFNpZ25hdHVyZSB4bWxucz0iaHR0cDovL3d3dy53M'\
                'y5vcmcvMjAwMC8wOS94bWxkc2lnIyI+CiAgICA8U2lnbmVkSW5mbz4KICAg'\
                'ICAgPENhbm9uaWNhbGl6YXRpb25NZXRob2QgQWxnb3JpdGhtPSJodHRwOi8'\
                'vd3d3LnczLm9yZy9UUi8yMDAxL1JFQy14bWwtYzE0bi0yMDAxMDMxNSIvPg'\
                'ogICAgICA8U2lnbmF0dXJlTWV0aG9kIEFsZ29yaXRobT0iaHR0cDovL3d3d'\
                'y53My5vcmcvMjAwMS8wNC94bWxkc2lnLW1vcmUjcnNhLXNoYTI1NiIvPgog'\
                'ICAgICA8UmVmZXJlbmNlIFVSST0iI0NGZTM1MTUwOTA4NzIzMjE4MDAwMTg'\
                '2NTk5MDAwMDQwMTkwMDAwMzc4NTg1NDcwIj4KICAgICAgICA8VHJhbnNmb3'\
                'Jtcz4KICAgICAgICAgIDxUcmFuc2Zvcm0gQWxnb3JpdGhtPSJodHRwOi8vd'\
                '3d3LnczLm9yZy8yMDAwLzA5L3htbGRzaWcjZW52ZWxvcGVkLXNpZ25hdHVy'\
                'ZSIvPgogICAgICAgICAgPFRyYW5zZm9ybSBBbGdvcml0aG09Imh0dHA6Ly9'\
                '3d3cudzMub3JnL1RSLzIwMDEvUkVDLXhtbC1jMTRuLTIwMDEwMzE1Ii8+Ci'\
                'AgICAgICAgPC9UcmFuc2Zvcm1zPgogICAgICAgIDxEaWdlc3RNZXRob2QgQ'\
                'Wxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGVuYyNz'\
                'aGEyNTYiLz4KICAgICAgICA8RGlnZXN0VmFsdWU+Y0tqaXc0N1FOd3pzVGx'\
                'sUEwyQXFaYTJxNTM0NzJpbndVOFVhdmwzc0JRZz08L0RpZ2VzdFZhbHVlPg'\
                'ogICAgICA8L1JlZmVyZW5jZT4KICAgIDwvU2lnbmVkSW5mbz4KICAgIDxTa'\
                'WduYXR1cmVWYWx1ZT5VNTlRcWFkalhURjZleE1mUktGNVdwcHBLNjFNQis3'\
                'RXE0emRueFNlSVpPdy9uTUwyWjE3RjdWcHZLbWNQenFyMkVVL3ozWmtXWU1'\
                'TdUtKT080a2I1MVFlb09ZZHdieWNCTURzSThCd3lyZU1lVjR3R0xoUTdJSU'\
                'lYY29yUHFtWjIyWnBudVN3bFQwbTRsd2pWcG9NWkVSYlhwYzFRNHorOE8vZ'\
                'WVmS1A1SFVQMU1aNnI4QzJpSE4xUC8zWlQySkpoUkdNdlErT0dsUHozUkhQ'\
                'TkFXdVEyTWVLTGsrL1pNTlhmalNnYUpuQnQwVHJOejBZU0pselhhZE5ycnZ'\
                '1VUVzUDkwdXdXQXRJZ204QWZLOGVXRVU2RlQ3anZHYlUwL1hhNnpnNHJiYW'\
                'p0YVY4bXJ6dDhnbUpjKzhyVXRydGNsLy9GUEQveGJEaXYzdFNwZWZTVER6N'\
                'nc9PTwvU2lnbmF0dXJlVmFsdWU+CiAgICA8S2V5SW5mbz4KICAgICAgPFg1'\
                'MDlEYXRhPgogICAgICAgIDxYNTA5Q2VydGlmaWNhdGU+TUlJR3NEQ0NCSml'\
                'nQXdJQkFnSUpBUmpndkl6bWQyQkdNQTBHQ1NxR1NJYjNEUUVCQ3dVQU1HY3'\
                'hDekFKQmdOVkJBWVRBa0pTTVRVd013WURWUVFLRXl4VFpXTnlaWFJoY21sa'\
                'ElHUmhJRVpoZW1WdVpHRWdaRzhnUlhOMFlXUnZJR1JsSUZOaGJ5QlFZWFZz'\
                'YnpFaE1COEdBMVVFQXhNWVFVTWdVMEZVSUdSbElGUmxjM1JsSUZORlJrRmF'\
                'JRk5RTUI0WERURTFNRGN3T0RFMU16WXpObG9YRFRJd01EY3dPREUxTXpZek'\
                '5sb3dnYlV4RWpBUUJnTlZCQVVUQ1Rrd01EQXdOREF4T1RFTE1Ba0dBMVVFQ'\
                'mhNQ1FsSXhFakFRQmdOVkJBZ1RDVk5CVHlCUVFWVk1UekVSTUE4R0ExVUVD'\
                'aE1JVTBWR1FWb3RVMUF4RHpBTkJnTlZCQXNUQmtGRExWTkJWREVvTUNZR0E'\
                'xVUVDeE1mUVhWMFpXNTBhV05oWkc4Z2NHOXlJRUZTSUZORlJrRmFJRk5RSU'\
                'ZOQlZERXdNQzRHQTFVRUF4TW5WRUZPUTBFZ1NVNUdUMUpOUVZSSlEwRWdSV'\
                'WxTUlV4Sk9qQTROekl6TWpFNE1EQXdNVGcyTUlJQklqQU5CZ2txaGtpRzl3'\
                'MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUFsODlQZmpmalp5MFFhdGdCenZ'\
                'WK0R1MDRla2piaVltblZlNVM5QUhOaWV4bm84VmRwOUI3OWh3TEtpRHJ2dn'\
                'dBdFZxcm9jV09RbU0zU0l4NU9FQ3kvdnZGaTQ2d2F3SlQ5WTJhNHp1RUZHd'\
                'khaU3VFL1VwM1BCNTJkUDM0YUdicGxpczBkMVJxSW9Yb0tXcStGbGpXcytO'\
                'ODlyd3ZQeGdKR2FmR3AzZTN0OENxSWpxQlBTQ1g4Qm15LzJZRGoxQy9KMUN'\
                'MVzkxcTk0cVZYMEN4aEtGSEF3ZmdJS2U3WkhlWnB3czJqaU9tdExGV0tvZk'\
                'NTYWNvblF1NVBIVVZ6T3Y3a1RwSzhaYnZzdm56d0x3SGE2L3JESnNPUlcvM'\
                'zNWK3J5ZnVEdFJIK25vczN1c0UvYXZjLzhtVTI1cTNyajdmVE5heDRnZ2I2'\
                'cnBGdFN5VEFXUmtGWlFJREFRQUJvNElDRGpDQ0Fnb3dEZ1lEVlIwUEFRSC9'\
                'CQVFEQWdYZ01Ic0dBMVVkSUFSME1ISXdjQVlKS3dZQkJBR0I3QzBETUdNd1'\
                'lRWUlLd1lCQlFVSEFnRVdWV2gwZEhBNkx5OWhZM05oZEM1cGJYQnlaVzV6W'\
                'Vc5bWFXTnBZV3d1WTI5dExtSnlMM0psY0c5emFYUnZjbWx2TDJSd1l5OWhZ'\
                'M05oZEhObFptRjZjM0F2WkhCalgyRmpjMkYwYzJWbVlYcHpjQzV3WkdZd2F'\
                '3WURWUjBmQkdRd1lqQmdvRjZnWElaYWFIUjBjRG92TDJGamMyRjBMWFJsYz'\
                'NSbExtbHRjSEpsYm5OaGIyWnBZMmxoYkM1amIyMHVZbkl2Y21Wd2IzTnBkR'\
                'zl5YVc4dmJHTnlMMkZqYzJGMGMyVm1ZWHB6Y0M5aFkzTmhkSE5sWm1GNmMz'\
                'QmpjbXd1WTNKc01JR21CZ2dyQmdFRkJRY0JBUVNCbVRDQmxqQTBCZ2dyQmd'\
                'FRkJRY3dBWVlvYUhSMGNEb3ZMMjlqYzNBdGNHbHNiM1F1YVcxd2NtVnVjMk'\
                'Z2Wm1samFXRnNMbU52YlM1aWNqQmVCZ2dyQmdFRkJRY3dBb1pTYUhSMGNEb'\
                '3ZMMkZqYzJGMExYUmxjM1JsTG1sdGNISmxibk5oYjJacFkybGhiQzVqYjIw'\
                'dVluSXZjbVZ3YjNOcGRHOXlhVzh2WTJWeWRHbG1hV05oWkc5ekwyRmpjMkY'\
                'wTFhSbGMzUmxMbkEzWXpBVEJnTlZIU1VFRERBS0JnZ3JCZ0VGQlFjREFqQU'\
                'pCZ05WSFJNRUFqQUFNQ1FHQTFVZEVRUWRNQnVnR1FZRllFd0JBd09nRUFRT'\
                '01EZzNNak15TVRnd01EQXhPRFl3SHdZRFZSMGpCQmd3Rm9BVWpqbEJBRnp5'\
                'dUFYYXFHMll1UUZHYlc1ajN3SXdEUVlKS29aSWh2Y05BUUVMQlFBRGdnSUJ'\
                'BRW15TnUySmJSZjdnZU1vcFdQQVdnYXNweFZPQ1F6NTZQL2lBMHhXbUVwZW'\
                'F5UGpTelBORnI3OUZwRUhFRjVieTRpdDB4aUhqM2NabVhubWtUTlZEWFN4M'\
                'DNDMVNOT0J5NnA5cDVwczhidlNNbFlWbWl5cjVDN3NqcDlBY3ZTOTJCWGVr'\
                'TmF6Y3IvY0hzVFVtbEdUSFpSbXdXWWtkTnphVkxNZ1FKNVJ5TG5XUHlhY1A'\
                '2S011dVUreTFTamdyS0hjc2Vhdzk4N05ITzJxL2ZDUkw1TGdnL082YUEyc0'\
                'ZQL1FNTzNXdUFFeklCUFQwazlnODBMNERublpCSW55VTVqZEdCNi9DdlpoZ'\
                'DdsYXU2bmNRWlBsNGNucitZNkRyNFRaMXl0QS9NcGYyL01Kalc4dzVYcXRh'\
                'dGdSQ2wzRFo3VzdENVRoeElXN29Cbk5idGtqdm9rSDM4T1NRSmcrRnZ0ZDd'\
                'BYjZiMG84UkR5eFZqVWk1S2xhKzRDQXhaczEwdnlXNEJrRDdmRmt0aVR6U1'\
                'BzeVN0cWJpbnNXaVBXL1h6Tm1sbUNYK1BEc1Fta2F6aW94NE1IUTJYUEZSb'\
                'mdCTExqWk9CV1ROZE1Qbyt6RFR5Zkc5alZBZUxFcjR2dFkvelJJVFA1STVH'\
                'azdjMFZHaTd1VVVncXNxZGx1SCt5Z0hxczUybE5vMW94TFltT0RVRnExeGV'\
                'qZ21HdTRDTWNKaHozUnVGalhEWDZCVWMwVTBjSmJ2dHpFVEtxNXBzT1lrbF'\
                'ptQTRuU0hlV0U0cDV4STFvMC84REtFZkVzNEd0SW1JQllQdWJVU0xFb0dGb'\
                'kRGNDVQZVFVN2NJK3lNSVlyY3Q1Q3puME01MmwvNzdhbmMrOU55SUdpK2xD'\
                'VlcvSUhmRVphd1l6aU1pVVVpQng8L1g1MDlDZXJ0aWZpY2F0ZT4KICAgICA'\
                'gPC9YNTA5RGF0YT4KICAgIDwvS2V5SW5mbz4KICA8L1NpZ25hdHVyZT4KPC'\
                '9DRmVDYW5jPgo=|'\
                '20150911175921|'\
                'CFe35150908723218000186599000040190000378585470|'\
                '2.00|'\
                '|'\
                'UKJ77VyQ0tc+EdLm5ZdAYILMqXvPSSB+QLYz+0ZgJpUhNN5AchnYuArKPzV'\
                'TiKqbObtxbR7l+s5X/TmMGMQw1TIryqv7A0Az73LagV+6oS5uk3yvBbYR+t'\
                'Wjfh+JcmktllYVZv8QVo+AY7ygj+lCqLjfUhMqBzU4HbJzBQMy7QPtCEy27'\
                'wk7c3S3mVcsmWALxd3H7lHnZj1wJ+ldhWJpNX17o/6sB0Nc6ksz4dYkLRfH'\
                'heCspFyTORtE1Any+DasmmaW8I4jNQfrWnxWbQxOJ3zqiE/pYb/wf/3r8Wv'\
                'C1luR5xdb9kMedd+TM0lZwZXndXkAcQOFVMq5CaYietV/og==',
    ]


RESP_FALHA = [
        u'123456|07001|Código de ativação inválido||',
        u'123456|07002|Cupom inválido||',
        u'123456|07003|SAT bloqueado pelo contribuinte||',
        u'123456|07004|SAT bloqueado pela SEFAZ||',
        u'123456|07005|SAT bloqueado por falta de comunicação||',
        u'123456|07006|SAT bloqueado, código de ativação incorreto||',
        u'123456|07007|Erro de validação do conteúdo||',
        u'123456|07098|SAT em processamento. Tente novamente.||',
        u'123456|07099|Erro desconhecido na emissão||',
    ]


RESP_INVALIDAS = [
        u'Resposta sem nenhum separador',
        u'Numero inesperado de campos|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p',
    ]


def test_resposta_cancelarultimavenda():
    resposta = RespostaCancelarUltimaVenda.analisar(RESP_SUCESSO[0])
    assert resposta.numeroSessao == 123456
    assert resposta.EEEEE == '07000'
    assert resposta.CCCC == '0000'
    assert resposta.arquivoCFeBase64 == base64.b64encode(XML_CFE_CANC_AUTORIZADO)
    assert resposta.timeStamp == as_datetime('20150911175921')
    assert resposta.chaveConsulta == 'CFe35150908723218000186599000040190000378585470'
    assert resposta.valorTotalCFe == Decimal('2.00')
    assert resposta.assinaturaQRCODE == 'UKJ77VyQ0tc+EdLm5ZdAYILMqXvPSSB'\
            '+QLYz+0ZgJpUhNN5AchnYuArKPzVTiKqbObtxbR7l+s5X/TmMGMQw1TIryq'\
            'v7A0Az73LagV+6oS5uk3yvBbYR+tWjfh+JcmktllYVZv8QVo+AY7ygj+lCq'\
            'LjfUhMqBzU4HbJzBQMy7QPtCEy27wk7c3S3mVcsmWALxd3H7lHnZj1wJ+ld'\
            'hWJpNX17o/6sB0Nc6ksz4dYkLRfHheCspFyTORtE1Any+DasmmaW8I4jNQf'\
            'rWnxWbQxOJ3zqiE/pYb/wf/3r8WvC1luR5xdb9kMedd+TM0lZwZXndXkAcQ'\
            'OFVMq5CaYietV/og=='

    for retorno in RESP_FALHA:
        with pytest.raises(ExcecaoRespostaSAT):
            resposta = RespostaCancelarUltimaVenda.analisar(retorno)

    for retorno in RESP_INVALIDAS:
        with pytest.raises(ErroRespostaSATInvalida):
            resposta = RespostaCancelarUltimaVenda.analisar(retorno)


@pytest.mark.skipif(
        pytest.config.getoption('--skip-cancelarultimavenda') or
        pytest.config.getoption('--skip-funcoes-sat'),
        reason='Funcao `CancelarUltimaVenda` explicitamente ignorada')
def test_funcao_enviardadosvenda(clientesatlocal, cfevenda):
    # realiza uma venda para cancelar em seguida
    rvenda = clientesatlocal.enviar_dados_venda(cfevenda)

    cfecanc = CFeCancelamento(
            chCanc=rvenda.chaveConsulta,
            CNPJ=pytest.config.getoption('--cnpj-ac'),
            signAC=pytest.config.getoption('--assinatura-ac'),
            numeroCaixa=pytest.config.getoption('--numero-caixa'),
            destinatario=Destinatario(
                    CPF='11122233396',
                    xNome=u'João de Teste'))

    rcanc = clientesatlocal.cancelar_ultima_venda(cfecanc.chCanc, cfecanc)
    assert rcanc.EEEEE == '07000'
    assert rcanc.valorTotalCFe == Decimal('5.75')


XML_CFE_CANCELAMENTO = """<?xml version="1.0" encoding="UTF-8"?>
<CFeCanc>
  <infCFe chCanc="CFe35150908723218000186599000040190000360539948">
    <ide>
      <CNPJ>16716114000172</CNPJ>
      <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
      <numeroCaixa>002</numeroCaixa>
    </ide>
    <emit/>
    <dest/>
    <total/>
    <infAdic/>
  </infCFe>
</CFeCanc>
"""

XML_CFE_CANC_AUTORIZADO = """<?xml version="1.0"?>
<CFeCanc>
  <infCFe
        Id="CFe35150908723218000186599000040190000378585470"
        chCanc="CFe35150908723218000186599000040190000360539948"
        versao="0.06">
    <dEmi>20150911</dEmi>
    <hEmi>175840</hEmi>
    <ide>
      <cUF>35</cUF>
      <cNF>858547</cNF>
      <mod>59</mod>
      <nserieSAT>900004019</nserieSAT>
      <nCFe>000037</nCFe>
      <dEmi>20150911</dEmi>
      <hEmi>175921</hEmi>
      <cDV>0</cDV>
      <CNPJ>16716114000172</CNPJ>
      <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
      <assinaturaQRCODE>UKJ77VyQ0tc+EdLm5ZdAYILMqXvPSSB+QLYz+0ZgJpUhNN5AchnYuArKPzVTiKqbObtxbR7l+s5X/TmMGMQw1TIryqv7A0Az73LagV+6oS5uk3yvBbYR+tWjfh+JcmktllYVZv8QVo+AY7ygj+lCqLjfUhMqBzU4HbJzBQMy7QPtCEy27wk7c3S3mVcsmWALxd3H7lHnZj1wJ+ldhWJpNX17o/6sB0Nc6ksz4dYkLRfHheCspFyTORtE1Any+DasmmaW8I4jNQfrWnxWbQxOJ3zqiE/pYb/wf/3r8WvC1luR5xdb9kMedd+TM0lZwZXndXkAcQOFVMq5CaYietV/og==</assinaturaQRCODE>
      <numeroCaixa>002</numeroCaixa>
    </ide>
    <emit>
      <CNPJ>08723218000186</CNPJ>
      <xNome>TANCA INFORMATICA EIRELI</xNome>
      <enderEmit>
        <xLgr>RUA ENGENHEIRO JORGE OLIVA</xLgr>
        <xBairro>VILA MASCOTE</xBairro>
        <xMun>SAO PAULO</xMun>
        <CEP>04362060</CEP>
      </enderEmit>
      <IE>149626224113</IE>
      <IM>123123</IM>
    </emit>
    <dest/>
    <total>
      <vCFe>2.00</vCFe>
    </total>
    <infAdic>
      <obsFisco xCampo="xCampo1">
        <xTexto>xTexto1</xTexto>
      </obsFisco>
    </infAdic>
  </infCFe>
  <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
    <SignedInfo>
      <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
      <SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>
      <Reference URI="#CFe35150908723218000186599000040190000378585470">
        <Transforms>
          <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
          <Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
        </Transforms>
        <DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
        <DigestValue>cKjiw47QNwzsTllPL2AqZa2q53472inwU8Uavl3sBQg=</DigestValue>
      </Reference>
    </SignedInfo>
    <SignatureValue>U59QqadjXTF6exMfRKF5WpppK61MB+7Eq4zdnxSeIZOw/nML2Z17F7VpvKmcPzqr2EU/z3ZkWYMSuKJOO4kb51QeoOYdwbycBMDsI8BwyreMeV4wGLhQ7IIIXcorPqmZ22ZpnuSwlT0m4lwjVpoMZERbXpc1Q4z+8O/eefKP5HUP1MZ6r8C2iHN1P/3ZT2JJhRGMvQ+OGlPz3RHPNAWuQ2MeKLk+/ZMNXfjSgaJnBt0TrNz0YSJlzXadNrrvuUEsP90uwWAtIgm8AfK8eWEU6FT7jvGbU0/Xa6zg4rbajtaV8mrzt8gmJc+8rUtrtcl//FPD/xbDiv3tSpefSTDz6w==</SignatureValue>
    <KeyInfo>
      <X509Data>
        <X509Certificate>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</X509Certificate>
      </X509Data>
    </KeyInfo>
  </Signature>
</CFeCanc>
"""
