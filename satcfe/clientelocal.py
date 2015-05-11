# -*- coding: utf-8 -*-
#
# satcfe/clientelocal.py
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

from .base import _FuncoesSAT
from .config import conf
from .resposta import RespostaExtrairLogs
from .resposta import RespostaSAT


class ClienteSATLocal(_FuncoesSAT):
    """
    Acesso ao equipamento SAT conectado na máquina local, para acesso às
    funções da DLL do SAT-CF-e.
    """

    def __init__(self, *args, **kwargs):
        super(ClienteSATLocal, self).__init__(*args, **kwargs)


    def enviar_dados_venda(self, *args, **kwargs):
        retorno = super(ClienteSATLocal, self).\
                enviar_dados_venda(*args, **kwargs)
        return RespostaSAT.enviar_dados_venda(retorno)


    def consultar_sat(self, *args, **kargs):
        retorno = super(ClienteSATLocal, self).consultar_sat(*args, **kwargs)
        return RespostaSAT.consultar_sat(retorno)


    def extrair_logs(self, *args, **kwargs):
        retorno = super(ClienteSATLocal, self).consultar_sat(*args, **kwargs)
        return RespostaExtrairLogs.analisar(retorno)
