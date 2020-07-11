# -*- coding: utf-8 -*-
#
# tests/test_util.py
#
# Copyright 2019 Base4 Sistemas Ltda ME
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

import datetime

import pytest

from satcfe.util import as_date
from satcfe.util import as_date_or_none
from satcfe.util import as_datetime
from satcfe.util import as_datetime_or_none
from satcfe.util import hms
from satcfe.util import hms_humanizado
from satcfe.util import normalizar_ip


def test_as_date():
    ref_date = datetime.date(2015, 7, 9)
    assert as_date('20150709') == ref_date
    assert as_date('20150709\n') == ref_date

    with pytest.raises(ValueError):
        as_date('  \n')


def test_as_date_or_none():
    ref_date = datetime.date(2015, 7, 9)
    assert as_date_or_none('20150709') == ref_date
    assert as_date_or_none('20150709\n') == ref_date
    assert as_date_or_none('  \n') is None


def test_as_datetime():
    ref_datetime = datetime.datetime(2015, 7, 9, 14, 39, 44)
    assert as_datetime('20150709143944') == ref_datetime
    assert as_datetime('20150709143944\n') == ref_datetime

    with pytest.raises(ValueError):
        as_datetime(' \t \n ')


def test_as_datetime_or_none():
    ref_datetime = datetime.datetime(2015, 7, 9, 14, 39, 44)
    assert as_datetime_or_none('20150709143944') == ref_datetime
    assert as_datetime_or_none('20150709143944\n') == ref_datetime
    assert as_datetime_or_none(' \t \n ') is None


def test_normalizar_ip():
    assert normalizar_ip('010.000.000.001') == '10.0.0.1'
    assert normalizar_ip('10.0.0.1') == '10.0.0.1'

    with pytest.raises(ValueError):
        normalizar_ip('')


def test_hms():
    assert hms(1) == (0, 0, 1)
    assert hms(60) == (0, 1, 0)
    assert hms(3600) == (1, 0, 0)
    assert hms(3601) == (1, 0, 1)
    assert hms(3661) == (1, 1, 1)


def test_hms_humanizado():
    assert hms_humanizado(0) == 'zero segundos'
    assert hms_humanizado(1) == '1 segundo'
    assert hms_humanizado(2) == '2 segundos'
    assert hms_humanizado(3600) == '1 hora'
    assert hms_humanizado(3602) == '1 hora e 2 segundos'
    assert hms_humanizado(3721) == '1 hora, 2 minutos e 1 segundo'
