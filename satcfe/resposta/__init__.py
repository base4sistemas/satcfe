# -*- coding: utf-8 -*-
#
# satcfe/resposta/__init__.py
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

from .associarassinatura import RespostaAssociarAssinatura  # noqa: F401
from .ativarsat import RespostaAtivarSAT  # noqa: F401
from .cancelarultimavenda import RespostaCancelarUltimaVenda  # noqa: F401
from .consultarnumerosessao import RespostaConsultarNumeroSessao  # noqa: F401
from .consultarstatusoperacional import RespostaConsultarStatusOperacional  # noqa: F401, E501
from .consultarultimasessaofiscal import RespostaConsultarUltimaSessaoFiscal  # noqa: F401, E501
from .enviardadosvenda import RespostaEnviarDadosVenda  # noqa: F401
from .extrairlogs import RespostaExtrairLogs  # noqa: F401
from .padrao import RespostaSAT  # noqa: F401
from .testefimafim import RespostaTesteFimAFim  # noqa: F401
