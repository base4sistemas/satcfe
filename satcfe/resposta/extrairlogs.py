# -*- coding: utf-8 -*-
#
# satcfe/resposta/extrairlogs.py
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

import os
import tempfile

from builtins import str as text

from ..excecoes import ExcecaoRespostaSAT
from ..util import base64_to_str
from .padrao import RespostaSAT
from .padrao import analisar_retorno


class RespostaExtrairLogs(RespostaSAT):
    """Lida com as respostas da função ``ExtrairLogs`` (veja o método
    :meth:`~satcfe.base.FuncoesSAT.extrair_logs`). Os atributos esperados em
    caso de sucesso, são:

    .. sourcecode:: text

        numeroSessao (int)
        EEEEE (text)
        mensagem (text)
        cod (text)
        mensagemSEFAZ (text)
        arquivoLog (text)

    Em caso de falha, são esperados apenas os atributos padrão, conforme
    descrito na constante :attr:`~satcfe.resposta.padrao.RespostaSAT.CAMPOS`.

    .. note::

        Aqui, ``text`` diz respeito à um objeto ``unicode`` (Python 2) ou
        ``str`` (Python 3). Veja ``builtins.str`` da biblioteca ``future``.

    """

    def conteudo(self):
        """Retorna o conteúdo do log decodificado."""
        return base64_to_str(self.arquivoLog)

    def salvar(
            self,
            destino=None,
            prefix='tmp', suffix='-sat.log', dir=None,
            encoding='utf-8', encoding_errors='strict'):
        """Salva o arquivo de log decodificado.

        :param str destino: Opcional. Caminho completo para o arquivo onde os
            dados dos logs deverão ser salvos. Se não informado, será criado
            um arquivo temporário via :func:`tempfile.mkstemp`.

        :param str prefix: Opcional. Prefixo para o nome do arquivo. Se não
            informado será usado ``"tmp"``.

        :param str suffix: Opcional. Sufixo para o nome do arquivo. Se não
            informado será usado ``"-sat.log"``.

        :param dir: Opcional. Contém o caminho completo onde o arquivo
            temporário deverá ser criado. Este argumento terá efeito apenas
            quando o argumento ``destino`` não for informado.

        :param str encoding: Opcional. Codificação de caracteres a ser usada
            para codificar o conteúdo do log em bytes que serão efetivamente
            escritos no arquivo de destino. Padrão é ``"utf-8"``. Veja o
            método :meth:`str.encode` para detalhes.

        :param str encoding_errors: Opcional. Como lidar com os erros de
            codificação de caracteres. Padrão é ``"strict"``. Veja o método
            :meth:`str.encode` para detalhes.


        :return: Retorna o caminho completo para o arquivo salvo.
        :rtype: str

        :raises FileExistsError: Se o destino informado já existir.
        """
        if destino:
            if os.path.exists(destino):
                raise FileExistsError(destino)
            fd = os.open(destino, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        else:
            fd, destino = tempfile.mkstemp(
                    dir=dir,
                    prefix=prefix,
                    suffix=suffix)

        # converte conteúdo str (unicode) para bytes antes de escrever
        dados = self.conteudo().encode(encoding, errors=encoding_errors)

        os.write(fd, dados)
        os.fsync(fd)
        os.close(fd)

        return destino

    @staticmethod
    def analisar(retorno):
        """Constrói uma :class:`RespostaExtrairLogs` a partir do retorno
        informado.

        :param str retorno: Retorno da função ``ExtrairLogs``.
        """
        resposta = analisar_retorno(
                retorno,
                funcao='ExtrairLogs',
                classe_resposta=RespostaExtrairLogs,
                campos=RespostaSAT.CAMPOS + (
                        ('arquivoLog', text),
                    ),
                campos_alternativos=[
                        # se a extração dos logs falhar espera-se o padrão de
                        # campos no retorno...
                        RespostaSAT.CAMPOS,
                    ]
            )
        if resposta.EEEEE not in ('15000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta
