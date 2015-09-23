# -*- coding: utf-8 -*-
#
# satcfe/util.py
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

from datetime import datetime
from unidecode import unidecode


def as_ascii(value):
    """Converte a sequência unicode para ``str`` ou apenas retorna o argumento.

    .. sourcecode:: python

        >>> type(as_ascii('testando'))
        <type 'str'>
        >>> type(as_ascii(u'bênção'))
        <type 'str'>
        >>> as_ascii(u'b\u00EAn\u00E7\u00E3o')
        'bencao'

    """
    if isinstance(value, unicode):
        return unidecode(value)
    return value


def as_clean_unicode(value):
    """Resulta na conversão do argumento para ``unicode`` e a subsequente
    remoção dos espaços em branco das bordas.

    .. sourcecode:: python

        >>> as_clean_unicode('abc')
        u'abc'
        >>> as_clean_unicode('abc\\n')
        u'abc'
        >>> as_clean_unicode(' \\tabc \\t \\n   ')
        u'abc'

    """
    return unicode(value).strip()


def as_date(value):
    """Converte uma sequência string para um objeto :class:`datetime.date`. Os
    espaços em branco das bordas da sequência serão removidos antes da
    conversão.

    .. sourcecode:: python

        >>> import datetime
        >>> as_date('20150709')
        datetime.date(2015, 7, 9)
        >>> as_date('20150709\\n')
        datetime.date(2015, 7, 9)
        >>> as_date('  \\n')
        Traceback (most recent call last):
         ...
        ValueError: ...

    """
    return datetime.strptime(value.strip(), '%Y%m%d').date()


def as_date_or_none(value):
    """Converte uma sequência string para um objeto :class:`datetime.date` ou
    resulta em ``None`` se a sequência estiver vazia após terem sido removidos
    espaços em branco das bordas.

    .. sourcecode:: python

        >>> import datetime
        >>> as_date_or_none('20150709')
        datetime.date(2015, 7, 9)
        >>> as_date_or_none('20150709\\n')
        datetime.date(2015, 7, 9)
        >>> assert as_date_or_none('  \\n') is None

    """
    try:
        return datetime.strptime(value.strip(), '%Y%m%d').date()
    except ValueError:
        return None


def as_datetime(value):
    """Converte uma sequência string para um objeto :class:`datetime.datetime`.
    Os espaços em branco das bordas da sequência serão removidos antes da
    conversão.

    .. sourcecode:: python

        >>> import datetime
        >>> as_datetime('20150709143944')
        datetime.datetime(2015, 7, 9, 14, 39, 44)
        >>> as_datetime('20150709143944\\n')
        datetime.datetime(2015, 7, 9, 14, 39, 44)
        >>> as_datetime(' \\t \\n ')
        Traceback (most recent call last):
         ...
        ValueError: ...


    """
    return datetime.strptime(value.strip(), '%Y%m%d%H%M%S')


def as_datetime_or_none(value):
    """Converte uma sequência string para um objeto :class:`datetime.datetime`
    ou resulta em ``None`` se a sequência estiver vazia após terem sido
    removidos espaços em branco das bordas.

    .. sourcecode:: python

        >>> import datetime
        >>> as_datetime_or_none('20150709143944')
        datetime.datetime(2015, 7, 9, 14, 39, 44)
        >>> as_datetime_or_none('20150709143944\\n')
        datetime.datetime(2015, 7, 9, 14, 39, 44)
        >>> assert as_datetime_or_none(' \\t \\n ') is None

    """
    try:
        return datetime.strptime(value.strip(), '%Y%m%d%H%M%S')
    except ValueError:
        return None


def normalizar_ip(ip):
    """Normaliza uma sequência string que contenha um endereço IP.

    Normalmente os equipamentos SAT, seguindo a ER SAT, resultam endereços IP
    com um aspecto similar a ``010.000.000.001``, visualmente desagradável e
    difícil de ler. Esta função normaliza o endereço acima como ``10.0.0.1``.

    .. sourcecode:: python

        >>> normalizar_ip('010.000.000.001')
        '10.0.0.1'
        >>> normalizar_ip('10.0.0.1')
        '10.0.0.1'
        >>> normalizar_ip('')
        Traceback (most recent call last):
         ...
        ValueError: invalid literal for int() with base 10: ''

    """
    return '.'.join([str(int(n, 10)) for n in ip.split('.')])
