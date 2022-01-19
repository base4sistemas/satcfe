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
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import logging

__version__ = '2.2'

logging.getLogger('satcfe').addHandler(logging.NullHandler())

from satcomum.constantes import VERSAO_ER  # noqa: E402, F401
from .base import BibliotecaSAT  # noqa: E402, F401
from .clientelocal import ClienteSATLocal  # noqa: E402, F401
from .clientesathub import ClienteSATHub  # noqa: E402, F401
