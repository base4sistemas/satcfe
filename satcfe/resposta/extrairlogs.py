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

import base64
import errno
import os

from satcomum.util import forcar_unicode

from ..excecoes import ExcecaoRespostaSAT
from .padrao import RespostaSAT
from .padrao import analisar_retorno


class RespostaExtrairLogs(RespostaSAT):

    def conteudo(self):
        """
        Retorna o conteúdo do log decodificado.
        """
        return base64.b64decode(self.arquivoLog)


    def salvar(self, destino=None, prefix='tmp', suffix='-sat.log'):
        """
        Salva o arquivo de log decodificado e retorna o caminho absoluto do
        arquivo. Se o destino não for informado, então será criado um arquivo
        temporário.
        """
        if destino:
            if os.path.exists(destino):
                raise IOError((errno.EEXIST, 'File exists', destino,))
            destino = os.path.abspath(destino)
            fd = os.open(destino, os.O_EXCL|os.O_CREAT|os.O_WRONLY)
        else:
            fd, destino = tempfile.mkstemp(prefix=prefix, suffix=suffix)

        os.write(fd, self.conteudo())
        os.fsync(fd)
        os.close(fd)

        return os.path.abspath(destino)


    @staticmethod
    def analisar(retorno):
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='ExtrairLogs',
                classe_resposta=RespostaExtrairLogs,
                campos=CAMPOS_PADRAO + (
                        ('arquivoLog', unicode),
                    )
            )
        if resposta.EEEEE not in ('15000',):
            raise ExcecaoRespostaSAT(resposta)
        return resposta
