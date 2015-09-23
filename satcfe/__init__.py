# -*- coding: utf-8 -*-
#
# satcfe/__init__.py
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

import os

__version__ = '0.0.7'

if 'SATCFE_SETUP_SCRIPT' not in os.environ:
    from satcomum.constantes import VERSAO_ER
    from .config import conf
    from .base import DLLSAT
    from .clientelocal import ClienteSATLocal
    from .clientesathub import ClienteSATHub
