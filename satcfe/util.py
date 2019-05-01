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
import base64

from datetime import datetime


def str_to_base64(data, encoding='utf-8'):
    """Codifica uma string (por padrão, UTF-8) em Base64.

    :param str data: String a ser codificada em Base64.
    :param str encoding: Opcional. O *encoding* da string `data`. Se não for
        especificado, o padrão é `'utf-8'`.

    :returns: Uma string UTF-8 contendo a massa de dados em Base64.
    :rtype: str
    """
    data_as_bytes = data.encode(encoding)
    base64_data = base64.b64encode(data_as_bytes)
    return base64_data.decode('utf-8')


def base64_to_str(data):
    """Decodifica uma massa de dados codificada em Base64.

    :param str data: String contendo a massa de dados codificada em Base64.
    :rtype: str
    """
    data_as_bytes = data.encode('utf-8')
    decoded_bytes = base64.b64decode(data_as_bytes)
    return decoded_bytes.decode('utf-8')


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


def hms(segundos):
    """
    Retorna o número de horas, minutos e segundos a partir do total de
    segundos informado.

    .. sourcecode:: python

        >>> hms(1)
        (0, 0, 1)

        >>> hms(60)
        (0, 1, 0)

        >>> hms(3600)
        (1, 0, 0)

        >>> hms(3601)
        (1, 0, 1)

        >>> hms(3661)
        (1, 1, 1)

    :param int segundos: O número total de segundos.

    :returns: Uma tupla contendo trẽs elementos representando, respectivamente,
        o número de horas, minutos e segundos calculados a partir do total de
        segundos.

    :rtype: tuple
    """
    h = (segundos // 3600)
    m = (segundos - (3600 * h)) // 60
    s = (segundos - (3600 * h) - (m * 60));
    return (h, m, s)


def hms_humanizado(segundos):
    """
    Retorna um texto legível que descreve o total de horas, minutos e segundos
    calculados a partir do total de segundos informados.

    .. sourcecode:: python

        >>> hms_humanizado(0)
        'zero segundos'

        >>> hms_humanizado(1)
        '1 segundo'

        >>> hms_humanizado(2)
        '2 segundos'

        >>> hms_humanizado(3600)
        '1 hora'

        >>> hms_humanizado(3602)
        '1 hora e 2 segundos'

        >>> hms_humanizado(3721)
        '1 hora, 2 minutos e 1 segundo'

    :rtype: str
    """
    p = lambda n, s, p: p if n > 1 else s
    h, m, s = hms(segundos)

    tokens = [
            '' if h == 0 else '{:d} {}'.format(h, p(h, 'hora', 'horas')),
            '' if m == 0 else '{:d} {}'.format(m, p(m, 'minuto', 'minutos')),
            '' if s == 0 else '{:d} {}'.format(s, p(s, 'segundo', 'segundos'))]

    tokens = [token for token in tokens if token]

    if len(tokens) == 1:
        return tokens[0]

    if len(tokens) > 1:
        return '{} e {}'.format(', '.join(tokens[:-1]), tokens[-1])

    return 'zero segundos' # QUESTION: se não for isso, o que seria?
