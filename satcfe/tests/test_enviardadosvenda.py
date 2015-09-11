# -*- coding: utf-8 -*-
#
# satcfe/tests/resposta/test_enviardadosvenda.py
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

from satcfe.excecoes import ErroRespostaSATInvalida
from satcfe.excecoes import ExcecaoRespostaSAT
from satcfe.resposta import RespostaEnviarDadosVenda
from satcfe.util import as_datetime


RESP_SUCESSO = [
        # o conteúdo do XML em base64 nesta resposta foi contruído a partir
        # dos dados em XML_CFE_VENDA_AUTORIZADO; o objetivo é testar o
        # tratamento da resposta e não a autenticidade do documento;
        u'123456|06000|0000|Emitido com sucesso + conteúdo notas|||'\
                'PD94bWwgdmVyc2lvbj0iMS4wIj8+CjxDRmU+CiAgPGluZkNGZSBJZD0iQ0Z'\
                'lMzUxNTA3MDg3MjMyMTgwMDAxODY1OTkwMDAwNDAxOTAwMDAyMTUxMzM0MD'\
                'giIHZlcnNhbz0iMC4wNiIgdmVyc2FvRGFkb3NFbnQ9IjAuMDYiIHZlcnNhb'\
                '1NCPSIwMTAwMDAiPgogICAgPGlkZT4KICAgICAgPGNVRj4zNTwvY1VGPgog'\
                'ICAgICA8Y05GPjUxMzM0MDwvY05GPgogICAgICA8bW9kPjU5PC9tb2Q+CiA'\
                'gICAgIDxuc2VyaWVTQVQ+OTAwMDA0MDE5PC9uc2VyaWVTQVQ+CiAgICAgID'\
                'xuQ0ZlPjAwMDAyMTwvbkNGZT4KICAgICAgPGRFbWk+MjAxNTA3MTg8L2RFb'\
                'Wk+CiAgICAgIDxoRW1pPjE1NDQyMzwvaEVtaT4KICAgICAgPGNEVj44PC9j'\
                'RFY+CiAgICAgIDx0cEFtYj4yPC90cEFtYj4KICAgICAgPENOUEo+MTY3MTY'\
                'xMTQwMDAxNzI8L0NOUEo+CiAgICAgIDxzaWduQUM+U0dSLVNBVCBTSVNURU'\
                '1BIERFIEdFU1RBTyBFIFJFVEFHVUFSREEgRE8gU0FUPC9zaWduQUM+CiAgI'\
                'CAgIDxhc3NpbmF0dXJhUVJDT0RFPlo1blZPbFdjZW90cFJ3RkVQREVUbC9y'\
                'Zm1EblFyYVg3T2FKQitmcXBSNkd4SUVjZHEwSkl5b0JhNUZ1OHZST2hjWWM'\
                'vRVNkSnhHbDdVS0ZiaVBPMWd4dFBwNWRsZTIyazV2R0hlSzV0MlRONi9Ibk'\
                'ZITDg1cWtMcS9OcXp0OXprRTM3SDcxeXZkb0hsZGdZYUpLbVh6Nm1xRmg1M'\
                'zBqYlZWQkwxdTRsZWl4ZUJCajVhemcwc1VydlZrcGtDNXVOV0tXdENiVUtu'\
                'TkQ3dEh0NG90cHJ4MFZRMSs1a0E5ZXlKMi91Tk02b2FYQ3V0UG1MNzBod0h'\
                'QQkdFZVBtWkZHSlFObEJuWDZpL0lwYm5iVVJHQlR3NnR4a3ZPV2NkZmI2Y0'\
                'ErM2dLR05pWWZrdXI4RjRqZGVEQnVQUlluVkU0d1ZUdkI5K3d4Tmd1cVV4V'\
                'HJTWGJUM1JJdz09PC9hc3NpbmF0dXJhUVJDT0RFPgogICAgICA8bnVtZXJv'\
                'Q2FpeGE+MDAyPC9udW1lcm9DYWl4YT4KICAgIDwvaWRlPgogICAgPGVtaXQ'\
                '+CiAgICAgIDxDTlBKPjA4NzIzMjE4MDAwMTg2PC9DTlBKPgogICAgICA8eE'\
                '5vbWU+VEFOQ0EgSU5GT1JNQVRJQ0EgRUlSRUxJPC94Tm9tZT4KICAgICAgP'\
                'HhGYW50PlRBTkNBPC94RmFudD4KICAgICAgPGVuZGVyRW1pdD4KICAgICAg'\
                'ICA8eExncj5SVUEgRU5HRU5IRUlSTyBKT1JHRSBPTElWQTwveExncj4KICA'\
                'gICAgICA8bnJvPjczPC9ucm8+CiAgICAgICAgPHhCYWlycm8+VklMQSBNQV'\
                'NDT1RFPC94QmFpcnJvPgogICAgICAgIDx4TXVuPlNBTyBQQVVMTzwveE11b'\
                'j4KICAgICAgICA8Q0VQPjA0MzYyMDYwPC9DRVA+CiAgICAgIDwvZW5kZXJF'\
                'bWl0PgogICAgICA8SUU+MTQ5NjI2MjI0MTEzPC9JRT4KICAgICAgPElNPjE'\
                'yMzEyMzwvSU0+CiAgICAgIDxjUmVnVHJpYj4zPC9jUmVnVHJpYj4KICAgIC'\
                'AgPGNSZWdUcmliSVNTUU4+MzwvY1JlZ1RyaWJJU1NRTj4KICAgICAgPGluZ'\
                'FJhdElTU1FOPk48L2luZFJhdElTU1FOPgogICAgPC9lbWl0PgogICAgPGRl'\
                'c3QvPgogICAgPGRldCBuSXRlbT0iMSI+CiAgICAgIDxwcm9kPgogICAgICA'\
                'gIDxjUHJvZD43ODk0MzIxNzIyMDE2PC9jUHJvZD4KICAgICAgICA8eFByb2'\
                'Q+VE9ERFlOSE8gMjAwIE1MPC94UHJvZD4KICAgICAgICA8Q0ZPUD41MTAyP'\
                'C9DRk9QPgogICAgICAgIDx1Q29tPlVOPC91Q29tPgogICAgICAgIDxxQ29t'\
                'PjEuMDAwMDwvcUNvbT4KICAgICAgICA8dlVuQ29tPjIuMDA8L3ZVbkNvbT4'\
                'KICAgICAgICA8dlByb2Q+Mi4wMDwvdlByb2Q+CiAgICAgICAgPGluZFJlZ3'\
                'JhPkE8L2luZFJlZ3JhPgogICAgICAgIDx2SXRlbT4yLjAwPC92SXRlbT4KI'\
                'CAgICAgICA8dlJhdERlc2M+MC4wMDwvdlJhdERlc2M+CiAgICAgICAgPHZS'\
                'YXRBY3I+MC4wMDwvdlJhdEFjcj4KICAgICAgPC9wcm9kPgogICAgICA8aW1'\
                'wb3N0bz4KICAgICAgICA8SUNNUz4KICAgICAgICAgIDxJQ01TU04xMDI+Ci'\
                'AgICAgICAgICAgIDxPcmlnPjA8L09yaWc+CiAgICAgICAgICAgIDxDU09TT'\
                'j41MDA8L0NTT1NOPgogICAgICAgICAgPC9JQ01TU04xMDI+CiAgICAgICAg'\
                'PC9JQ01TPgogICAgICAgIDxQSVM+CiAgICAgICAgICA8UElTU04+CiAgICA'\
                'gICAgICAgIDxDU1Q+NDk8L0NTVD4KICAgICAgICAgIDwvUElTU04+CiAgIC'\
                'AgICAgPC9QSVM+CiAgICAgICAgPENPRklOUz4KICAgICAgICAgIDxDT0ZJT'\
                'lNTTj4KICAgICAgICAgICAgPENTVD40OTwvQ1NUPgogICAgICAgICAgPC9D'\
                'T0ZJTlNTTj4KICAgICAgICA8L0NPRklOUz4KICAgICAgPC9pbXBvc3RvPgo'\
                'gICAgPC9kZXQ+CiAgICA8dG90YWw+CiAgICAgIDxJQ01TVG90PgogICAgIC'\
                'AgIDx2SUNNUz4wLjAwPC92SUNNUz4KICAgICAgICA8dlByb2Q+Mi4wMDwvd'\
                'lByb2Q+CiAgICAgICAgPHZEZXNjPjAuMDA8L3ZEZXNjPgogICAgICAgIDx2'\
                'UElTPjAuMDA8L3ZQSVM+CiAgICAgICAgPHZDT0ZJTlM+MC4wMDwvdkNPRkl'\
                'OUz4KICAgICAgICA8dlBJU1NUPjAuMDA8L3ZQSVNTVD4KICAgICAgICA8dk'\
                'NPRklOU1NUPjAuMDA8L3ZDT0ZJTlNTVD4KICAgICAgICA8dk91dHJvPjAuM'\
                'DA8L3ZPdXRybz4KICAgICAgPC9JQ01TVG90PgogICAgICA8dkNGZT4yLjAw'\
                'PC92Q0ZlPgogICAgPC90b3RhbD4KICAgIDxwZ3RvPgogICAgICA8TVA+CiA'\
                'gICAgICAgPGNNUD4wMTwvY01QPgogICAgICAgIDx2TVA+Mi4wMDwvdk1QPg'\
                'ogICAgICA8L01QPgogICAgICA8dlRyb2NvPjAuMDA8L3ZUcm9jbz4KICAgI'\
                'DwvcGd0bz4KICAgIDxpbmZBZGljPgogICAgICA8aW5mQ3BsPlZhbG9yZXMg'\
                'YXByb3hpbWFkb3MgZG9zIHRyaWJ1dG9zOgpGZWQgUiQgICAwLDIzIC8gRXN'\
                '0IFIkICAgMCwzNgpGb250ZTogSUJQVCAoOW9pM2FDKQogQmFsY2FvOiBWZW'\
                '5kYSBCYWxjYW8KIFRLOiAxMDAyOTY5MDYgIFNTOiAxMDAwMDE2ODAgIFZOR'\
                'DogUEFUUkkgIE9QCjwvaW5mQ3BsPgogICAgICA8b2JzRmlzY28geENhbXBv'\
                'PSJ4Q2FtcG8xIj4KICAgICAgICA8eFRleHRvPnhUZXh0bzE8L3hUZXh0bz4'\
                'KICAgICAgPC9vYnNGaXNjbz4KICAgIDwvaW5mQWRpYz4KICA8L2luZkNGZT'\
                '4KICA8U2lnbmF0dXJlIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL'\
                'zA5L3htbGRzaWcjIj4KICAgIDxTaWduZWRJbmZvPgogICAgICA8Q2Fub25p'\
                'Y2FsaXphdGlvbk1ldGhvZCBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3J'\
                'nL1RSLzIwMDEvUkVDLXhtbC1jMTRuLTIwMDEwMzE1Ii8+CiAgICAgIDxTaW'\
                'duYXR1cmVNZXRob2QgQWxnb3JpdGhtPSJodHRwOi8vd3d3LnczLm9yZy8yM'\
                'DAxLzA0L3htbGRzaWctbW9yZSNyc2Etc2hhMjU2Ii8+CiAgICAgIDxSZWZl'\
                'cmVuY2UgVVJJPSIjQ0ZlMzUxNTA3MDg3MjMyMTgwMDAxODY1OTkwMDAwNDA'\
                'xOTAwMDAyMTUxMzM0MDgiPgogICAgICAgIDxUcmFuc2Zvcm1zPgogICAgIC'\
                'AgICAgPFRyYW5zZm9ybSBBbGdvcml0aG09Imh0dHA6Ly93d3cudzMub3JnL'\
                'zIwMDAvMDkveG1sZHNpZyNlbnZlbG9wZWQtc2lnbmF0dXJlIi8+CiAgICAg'\
                'ICAgICA8VHJhbnNmb3JtIEFsZ29yaXRobT0iaHR0cDovL3d3dy53My5vcmc'\
                'vVFIvMjAwMS9SRUMteG1sLWMxNG4tMjAwMTAzMTUiLz4KICAgICAgICA8L1'\
                'RyYW5zZm9ybXM+CiAgICAgICAgPERpZ2VzdE1ldGhvZCBBbGdvcml0aG09I'\
                'mh0dHA6Ly93d3cudzMub3JnLzIwMDEvMDQveG1sZW5jI3NoYTI1NiIvPgog'\
                'ICAgICAgIDxEaWdlc3RWYWx1ZT5acVZERlhkL2VvNHVHR3BCYklISlFROFp'\
                'jTk43azVlYVpTRTB4aWJnQjFZPTwvRGlnZXN0VmFsdWU+CiAgICAgIDwvUm'\
                'VmZXJlbmNlPgogICAgPC9TaWduZWRJbmZvPgogICAgPFNpZ25hdHVyZVZhb'\
                'HVlPkJ6cGovUjlKNXFYK0tqczUyckxseTV2QXkvZGRCVGpuNDVDQmZoV1Jh'\
                'ZTlGWHF5SnFRL1hqczQwZWFDZDVsYlBUS3E1UHhBamhsOHIxR1pqTHZZUGN'\
                'lWlNyT2lkUjk1V3RjSE5ZL0pDUXc2Y0xraGVVMThVUWR0czRoc0t4SlhEV1'\
                'd1V0I4S2FPbmZBMW1lWTJ1M1J3bW9URUxtV283OWFxNmZqUE9MeXYzbFRXZ'\
                'kk1MUlQeis5OUtHVDVNSmJkWlF6c1MxMnN5WlpibU5uMGxsRGlKNTE1M051'\
                'WGJVaE9hYVhkOGxTSWlaaTFsRXFaSWI3clVWYkYzbWIxOXVBTFpMcndPYS9'\
                'lSzZCMlVVeUoxMXArRk9ObG4yc1NwL3crd1RqdEtSMHZENDJabzZtbkJtQk'\
                'p4VjgrcXVkVkxPQk9YNWdIZ1pMblR0Q29zK1BvUUk0UnVZUT09PC9TaWduY'\
                'XR1cmVWYWx1ZT4KICAgIDxLZXlJbmZvPgogICAgICA8WDUwOURhdGE+CiAg'\
                'ICAgICAgPFg1MDlDZXJ0aWZpY2F0ZT5NSUlHc0RDQ0JKaWdBd0lCQWdJSkF'\
                'Samd2SXptZDJCR01BMEdDU3FHU0liM0RRRUJDd1VBTUdjeEN6QUpCZ05WQk'\
                'FZVEFrSlNNVFV3TXdZRFZRUUtFeXhUWldOeVpYUmhjbWxoSUdSaElFWmhlb'\
                'VZ1WkdFZ1pHOGdSWE4wWVdSdklHUmxJRk5oYnlCUVlYVnNiekVoTUI4R0Ex'\
                'VUVBeE1ZUVVNZ1UwRlVJR1JsSUZSbGMzUmxJRk5GUmtGYUlGTlFNQjRYRFR'\
                'FMU1EY3dPREUxTXpZek5sb1hEVEl3TURjd09ERTFNell6Tmxvd2diVXhFak'\
                'FRQmdOVkJBVVRDVGt3TURBd05EQXhPVEVMTUFrR0ExVUVCaE1DUWxJeEVqQ'\
                'VFCZ05WQkFnVENWTkJUeUJRUVZWTVR6RVJNQThHQTFVRUNoTUlVMFZHUVZv'\
                'dFUxQXhEekFOQmdOVkJBc1RCa0ZETFZOQlZERW9NQ1lHQTFVRUN4TWZRWFY'\
                'wWlc1MGFXTmhaRzhnY0c5eUlFRlNJRk5GUmtGYUlGTlFJRk5CVkRFd01DNE'\
                'dBMVVFQXhNblZFRk9RMEVnU1U1R1QxSk5RVlJKUTBFZ1JVbFNSVXhKT2pBN'\
                'E56SXpNakU0TURBd01UZzJNSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9D'\
                'QVE4QU1JSUJDZ0tDQVFFQWw4OVBmamZqWnkwUWF0Z0J6dlYrRHUwNGVramJ'\
                'pWW1uVmU1UzlBSE5pZXhubzhWZHA5Qjc5aHdMS2lEcnZ2d0F0VnFyb2NXT1'\
                'FtTTNTSXg1T0VDeS92dkZpNDZ3YXdKVDlZMmE0enVFRkd2SFpTdUUvVXAzU'\
                'EI1MmRQMzRhR2JwbGlzMGQxUnFJb1hvS1dxK0ZsaldzK044OXJ3dlB4Z0pH'\
                'YWZHcDNlM3Q4Q3FJanFCUFNDWDhCbXkvMllEajFDL0oxQ0xXOTFxOTRxVlg'\
                'wQ3hoS0ZIQXdmZ0lLZTdaSGVacHdzMmppT210TEZXS29mQ1NhY29uUXU1UE'\
                'hVVnpPdjdrVHBLOFpidnN2bnp3THdIYTYvckRKc09SVy8zM1YrcnlmdUR0U'\
                'kgrbm9zM3VzRS9hdmMvOG1VMjVxM3JqN2ZUTmF4NGdnYjZycEZ0U3lUQVdS'\
                'a0ZaUUlEQVFBQm80SUNEakNDQWdvd0RnWURWUjBQQVFIL0JBUURBZ1hnTUh'\
                'zR0ExVWRJQVIwTUhJd2NBWUpLd1lCQkFHQjdDMERNR013WVFZSUt3WUJCUV'\
                'VIQWdFV1ZXaDBkSEE2THk5aFkzTmhkQzVwYlhCeVpXNXpZVzltYVdOcFlXd'\
                '3VZMjl0TG1KeUwzSmxjRzl6YVhSdmNtbHZMMlJ3WXk5aFkzTmhkSE5sWm1G'\
                'NmMzQXZaSEJqWDJGamMyRjBjMlZtWVhwemNDNXdaR1l3YXdZRFZSMGZCR1F'\
                '3WWpCZ29GNmdYSVphYUhSMGNEb3ZMMkZqYzJGMExYUmxjM1JsTG1sdGNISm'\
                'xibk5oYjJacFkybGhiQzVqYjIwdVluSXZjbVZ3YjNOcGRHOXlhVzh2YkdOe'\
                'UwyRmpjMkYwYzJWbVlYcHpjQzloWTNOaGRITmxabUY2YzNCamNtd3VZM0pz'\
                'TUlHbUJnZ3JCZ0VGQlFjQkFRU0JtVENCbGpBMEJnZ3JCZ0VGQlFjd0FZWW9'\
                'hSFIwY0RvdkwyOWpjM0F0Y0dsc2IzUXVhVzF3Y21WdWMyRnZabWxqYVdGc0'\
                'xtTnZiUzVpY2pCZUJnZ3JCZ0VGQlFjd0FvWlNhSFIwY0RvdkwyRmpjMkYwT'\
                'FhSbGMzUmxMbWx0Y0hKbGJuTmhiMlpwWTJsaGJDNWpiMjB1WW5JdmNtVndi'\
                'M05wZEc5eWFXOHZZMlZ5ZEdsbWFXTmhaRzl6TDJGamMyRjBMWFJsYzNSbEx'\
                'uQTNZekFUQmdOVkhTVUVEREFLQmdnckJnRUZCUWNEQWpBSkJnTlZIUk1FQW'\
                'pBQU1DUUdBMVVkRVFRZE1CdWdHUVlGWUV3QkF3T2dFQVFPTURnM01qTXlNV'\
                'Gd3TURBeE9EWXdId1lEVlIwakJCZ3dGb0FVampsQkFGenl1QVhhcUcyWXVR'\
                'RkdiVzVqM3dJd0RRWUpLb1pJaHZjTkFRRUxCUUFEZ2dJQkFFbXlOdTJKYlJ'\
                'mN2dlTW9wV1BBV2dhc3B4Vk9DUXo1NlAvaUEweFdtRXBlYXlQalN6UE5Gcj'\
                'c5RnBFSEVGNWJ5NGl0MHhpSGozY1ptWG5ta1ROVkRYU3gwM0MxU05PQnk2c'\
                'DlwNXBzOGJ2U01sWVZtaXlyNUM3c2pwOUFjdlM5MkJYZWtOYXpjci9jSHNU'\
                'VW1sR1RIWlJtd1dZa2ROemFWTE1nUUo1UnlMbldQeWFjUDZLTXV1VSt5MVN'\
                'qZ3JLSGNzZWF3OTg3TkhPMnEvZkNSTDVMZ2cvTzZhQTJzRlAvUU1PM1d1QU'\
                'V6SUJQVDBrOWc4MEw0RG5uWkJJbnlVNWpkR0I2L0N2WmhkN2xhdTZuY1FaU'\
                'Gw0Y25yK1k2RHI0VFoxeXRBL01wZjIvTUpqVzh3NVhxdGF0Z1JDbDNEWjdX'\
                'N0Q1VGh4SVc3b0JuTmJ0a2p2b2tIMzhPU1FKZytGdnRkN0FiNmIwbzhSRHl'\
                '4VmpVaTVLbGErNENBeFpzMTB2eVc0QmtEN2ZGa3RpVHpTUHN5U3RxYmluc1'\
                'dpUFcvWHpObWxtQ1grUERzUW1rYXppb3g0TUhRMlhQRlJuZ0JMTGpaT0JXV'\
                'E5kTVBvK3pEVHlmRzlqVkFlTEVyNHZ0WS96UklUUDVJNUdrN2MwVkdpN3VV'\
                'VWdxc3FkbHVIK3lnSHFzNTJsTm8xb3hMWW1PRFVGcTF4ZWpnbUd1NENNY0p'\
                'oejNSdUZqWERYNkJVYzBVMGNKYnZ0ekVUS3E1cHNPWWtsWm1BNG5TSGVXRT'\
                'RwNXhJMW8wLzhES0VmRXM0R3RJbUlCWVB1YlVTTEVvR0ZuREY0NVBlUVU3Y'\
                '0kreU1JWXJjdDVDem4wTTUybC83N2FuYys5TnlJR2krbENWVy9JSGZFWmF3'\
                'WXppTWlVVWlCeDwvWDUwOUNlcnRpZmljYXRlPgogICAgICA8L1g1MDlEYXR'\
                'hPgogICAgPC9LZXlJbmZvPgogIDwvU2lnbmF0dXJlPgo8L0NGZT4K|'\
                '20150718154423|'\
                'CFe35150708723218000186599000040190000215133408|'\
                '2.00|'\
                '|'\
                'Z5nVOlWceotpRwFEPDETl/rfmDnQraX7OaJB+fqpR6GxIEcdq0JIyoBa5Fu'\
                '8vROhcYc/ESdJxGl7UKFbiPO1gxtPp5dle22k5vGHeK5t2TN6/HnFHL85qk'\
                'Lq/Nqzt9zkE37H71yvdoHldgYaJKmXz6mqFh530jbVVBL1u4leixeBBj5az'\
                'g0sUrvVkpkC5uNWKWtCbUKnND7tHt4otprx0VQ1+5kA9eyJ2/uNM6oaXCut'\
                'PmL70hwHPBGEePmZFGJQNlBnX6i/IpbnbURGBTw6txkvOWcdfb6cA+3gKGN'\
                'iYfkur8F4jdeDBuPRYnVE4wVTvB9+wxNguqUxTrSXbT3RIw==',
    ]


RESP_FALHA = [
        u'123456|06001|Código de ativação inválido||',
        u'123456|06002|SAT ainda não ativado||',
        u'123456|06003|SAT não vinculado ao AC||',
        u'123456|06004|Vinculação do AC não confere||',
        u'123456|06005|Tamanho do CF-e-SAT superior a 1.500KB||',
        u'123456|06006|SAT bloqueado pelo contribuinte||',
        u'123456|06007|SAT bloqueado pela SEFAZ||',
        u'123456|06008|SAT bloqueado por falta de comunicação||',
        u'123456|06009|SAT bloqueado, código de ativação incorreto||',
        u'123456|06010|Erro de validação do conteúdo||',
        u'123456|06098|SAT em processamento. Tente novamente.||',
        u'123456|06099|Erro desconhecido na emissão||',
    ]


RESP_INVALIDAS = [
        u'Resposta sem nenhum separador',
        u'Numero inesperado de campos|a|b|c|d|e|f',
    ]


def test_resposta_enviardadosvenda():
    resposta = RespostaEnviarDadosVenda.analisar(RESP_SUCESSO[0])
    assert resposta.numeroSessao == 123456
    assert resposta.EEEEE == '06000'
    assert resposta.CCCC == '0000'
    assert resposta.arquivoCFeSAT == base64.b64encode(XML_CFE_VENDA_AUTORIZADO)
    assert resposta.timeStamp == as_datetime('20150718154423')
    assert resposta.chaveConsulta == 'CFe35150708723218000186599000040190000215133408'
    assert resposta.valorTotalCFe == Decimal('2.00')
    assert resposta.assinaturaQRCODE == 'Z5nVOlWceotpRwFEPDETl/rfmDnQraX7OaJ'\
            'B+fqpR6GxIEcdq0JIyoBa5Fu8vROhcYc/ESdJxGl7UKFbiPO1gxtPp5dle22k5v'\
            'GHeK5t2TN6/HnFHL85qkLq/Nqzt9zkE37H71yvdoHldgYaJKmXz6mqFh530jbVV'\
            'BL1u4leixeBBj5azg0sUrvVkpkC5uNWKWtCbUKnND7tHt4otprx0VQ1+5kA9eyJ'\
            '2/uNM6oaXCutPmL70hwHPBGEePmZFGJQNlBnX6i/IpbnbURGBTw6txkvOWcdfb6'\
            'cA+3gKGNiYfkur8F4jdeDBuPRYnVE4wVTvB9+wxNguqUxTrSXbT3RIw=='

    for retorno in RESP_FALHA:
        with pytest.raises(ExcecaoRespostaSAT):
            resposta = RespostaEnviarDadosVenda.analisar(retorno)

    for retorno in RESP_INVALIDAS:
        with pytest.raises(ErroRespostaSATInvalida):
            resposta = RespostaEnviarDadosVenda.analisar(retorno)


@pytest.mark.skipif(
        pytest.config.getoption('--skip-enviardadosvenda') or
        pytest.config.getoption('--skip-funcoes-sat'),
        reason='Funcao `EnviarDadosVenda` explicitamente ignorada')
def test_funcao_enviardadosvenda(clientesatlocal, cfevenda):
    resposta = clientesatlocal.enviar_dados_venda(cfevenda)
    assert resposta.EEEEE == '06000'
    assert resposta.valorTotalCFe == Decimal('5.75')
    assert len(resposta.chaveConsulta) == 47
    assert resposta.chaveConsulta.startswith('CFe')


XML_CFE_VENDA = """<?xml version="1.0"?>
<CFe>
  <infCFe versaoDadosEnt="0.06">
    <ide>
      <CNPJ>16716114000172</CNPJ>
      <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
      <numeroCaixa>002</numeroCaixa>
    </ide>
    <emit>
      <CNPJ>08723218000186</CNPJ>
      <IE>149626224113</IE>
      <IM>123123</IM>
      <cRegTribISSQN>3</cRegTribISSQN>
      <indRatISSQN>N</indRatISSQN>
    </emit>
    <dest/>
    <det nItem="1">
      <prod>
        <cProd>7894321722016</cProd>
        <xProd>TODDYNHO 200 ML</xProd>
        <CFOP>5102</CFOP>
        <uCom>UN</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>2.00</vUnCom>
        <indRegra>A</indRegra>
      </prod>
      <imposto>
        <ICMS>
          <ICMSSN102>
            <Orig>0</Orig>
            <CSOSN>500</CSOSN>
          </ICMSSN102>
        </ICMS>
        <PIS>
          <PISSN>
            <CST>49</CST>
          </PISSN>
        </PIS>
        <COFINS>
          <COFINSSN>
            <CST>49</CST>
          </COFINSSN>
        </COFINS>
      </imposto>
    </det>
    <total/>
    <pgto>
      <MP>
        <cMP>01</cMP>
        <vMP>2.00</vMP>
      </MP>
    </pgto>
    <infAdic>
      <infCpl>Valores aproximados dos tributos:
Fed R$   0,23 / Est R$   0,36
Fonte: IBPT (9oi3aC)
 Balcao: Venda Balcao
 TK: 100296906  SS: 100001680  VND: PATRI  OP
</infCpl>
    </infAdic>
  </infCFe>
</CFe>
"""

XML_CFE_VENDA_AUTORIZADO = """<?xml version="1.0"?>
<CFe>
  <infCFe Id="CFe35150708723218000186599000040190000215133408" versao="0.06" versaoDadosEnt="0.06" versaoSB="010000">
    <ide>
      <cUF>35</cUF>
      <cNF>513340</cNF>
      <mod>59</mod>
      <nserieSAT>900004019</nserieSAT>
      <nCFe>000021</nCFe>
      <dEmi>20150718</dEmi>
      <hEmi>154423</hEmi>
      <cDV>8</cDV>
      <tpAmb>2</tpAmb>
      <CNPJ>16716114000172</CNPJ>
      <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
      <assinaturaQRCODE>Z5nVOlWceotpRwFEPDETl/rfmDnQraX7OaJB+fqpR6GxIEcdq0JIyoBa5Fu8vROhcYc/ESdJxGl7UKFbiPO1gxtPp5dle22k5vGHeK5t2TN6/HnFHL85qkLq/Nqzt9zkE37H71yvdoHldgYaJKmXz6mqFh530jbVVBL1u4leixeBBj5azg0sUrvVkpkC5uNWKWtCbUKnND7tHt4otprx0VQ1+5kA9eyJ2/uNM6oaXCutPmL70hwHPBGEePmZFGJQNlBnX6i/IpbnbURGBTw6txkvOWcdfb6cA+3gKGNiYfkur8F4jdeDBuPRYnVE4wVTvB9+wxNguqUxTrSXbT3RIw==</assinaturaQRCODE>
      <numeroCaixa>002</numeroCaixa>
    </ide>
    <emit>
      <CNPJ>08723218000186</CNPJ>
      <xNome>TANCA INFORMATICA EIRELI</xNome>
      <xFant>TANCA</xFant>
      <enderEmit>
        <xLgr>RUA ENGENHEIRO JORGE OLIVA</xLgr>
        <nro>73</nro>
        <xBairro>VILA MASCOTE</xBairro>
        <xMun>SAO PAULO</xMun>
        <CEP>04362060</CEP>
      </enderEmit>
      <IE>149626224113</IE>
      <IM>123123</IM>
      <cRegTrib>3</cRegTrib>
      <cRegTribISSQN>3</cRegTribISSQN>
      <indRatISSQN>N</indRatISSQN>
    </emit>
    <dest/>
    <det nItem="1">
      <prod>
        <cProd>7894321722016</cProd>
        <xProd>TODDYNHO 200 ML</xProd>
        <CFOP>5102</CFOP>
        <uCom>UN</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>2.00</vUnCom>
        <vProd>2.00</vProd>
        <indRegra>A</indRegra>
        <vItem>2.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMSSN102>
            <Orig>0</Orig>
            <CSOSN>500</CSOSN>
          </ICMSSN102>
        </ICMS>
        <PIS>
          <PISSN>
            <CST>49</CST>
          </PISSN>
        </PIS>
        <COFINS>
          <COFINSSN>
            <CST>49</CST>
          </COFINSSN>
        </COFINS>
      </imposto>
    </det>
    <total>
      <ICMSTot>
        <vICMS>0.00</vICMS>
        <vProd>2.00</vProd>
        <vDesc>0.00</vDesc>
        <vPIS>0.00</vPIS>
        <vCOFINS>0.00</vCOFINS>
        <vPISST>0.00</vPISST>
        <vCOFINSST>0.00</vCOFINSST>
        <vOutro>0.00</vOutro>
      </ICMSTot>
      <vCFe>2.00</vCFe>
    </total>
    <pgto>
      <MP>
        <cMP>01</cMP>
        <vMP>2.00</vMP>
      </MP>
      <vTroco>0.00</vTroco>
    </pgto>
    <infAdic>
      <infCpl>Valores aproximados dos tributos:
Fed R$   0,23 / Est R$   0,36
Fonte: IBPT (9oi3aC)
 Balcao: Venda Balcao
 TK: 100296906  SS: 100001680  VND: PATRI  OP
</infCpl>
      <obsFisco xCampo="xCampo1">
        <xTexto>xTexto1</xTexto>
      </obsFisco>
    </infAdic>
  </infCFe>
  <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
    <SignedInfo>
      <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
      <SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>
      <Reference URI="#CFe35150708723218000186599000040190000215133408">
        <Transforms>
          <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
          <Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
        </Transforms>
        <DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
        <DigestValue>ZqVDFXd/eo4uGGpBbIHJQQ8ZcNN7k5eaZSE0xibgB1Y=</DigestValue>
      </Reference>
    </SignedInfo>
    <SignatureValue>Bzpj/R9J5qX+Kjs52rLly5vAy/ddBTjn45CBfhWRae9FXqyJqQ/Xjs40eaCd5lbPTKq5PxAjhl8r1GZjLvYPceZSrOidR95WtcHNY/JCQw6cLkheU18UQdts4hsKxJXDWWuWB8KaOnfA1meY2u3RwmoTELmWo79aq6fjPOLyv3lTWfI51IPz+99KGT5MJbdZQzsS12syZZbmNn0llDiJ5153NuXbUhOaaXd8lSIiZi1lEqZIb7rUVbF3mb19uALZLrwOa/eK6B2UUyJ11p+FONln2sSp/w+wTjtKR0vD42Zo6mnBmBJxV8+qudVLOBOX5gHgZLnTtCos+PoQI4RuYQ==</SignatureValue>
    <KeyInfo>
      <X509Data>
        <X509Certificate>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</X509Certificate>
      </X509Data>
    </KeyInfo>
  </Signature>
</CFe>
"""