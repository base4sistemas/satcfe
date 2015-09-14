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
import tempfile

from satcomum.util import forcar_unicode

from ..excecoes import ExcecaoRespostaSAT
from .padrao import RespostaSAT
from .padrao import analisar_retorno


class RespostaExtrairLogs(RespostaSAT):
    """Lida com as respostas da função ``ExtrairLogs`` (veja o método
    :meth:`~satcfe.base.FuncoesSAT.extrair_logs`). Os atributos esperados em
    caso de sucesso, são:

    .. sourcecode:: text

        numeroSessao (int)
        EEEEE (unicode)
        mensagem (unicode)
        cod (unicode)
        mensagemSEFAZ (unicode)
        arquivoLog (unicode)

    Em caso de falha, são esperados apenas os atributos padrão, conforme
    descrito na constante :attr:`~satcfe.resposta.padrao.RespostaSAT.CAMPOS`.
    """

    def conteudo(self):
        """Retorna o conteúdo do log decodificado."""
        return base64.b64decode(self.arquivoLog)


    def salvar(self, destino=None, prefix='tmp', suffix='-sat.log'):
        """Salva o arquivo de log decodificado.

        :param str destino: (Opcional) Caminho completo para o arquivo onde os
            dados dos logs deverão ser salvos. Se não informado, será criado
            um arquivo temporário via :func:`tempfile.mkstemp`.

        :param str prefix: (Opcional) Prefixo para o nome do arquivo. Se não
            informado será usado ``"tmp"``.

        :param str suffix: (Opcional) Sufixo para o nome do arquivo. Se não
            informado será usado ``"-sat.log"``.

        :return: Retorna o caminho completo para o arquivo salvo.
        :rtype: str

        :raises IOError: Se o destino for informado e o arquivo já existir.
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
        """Constrói uma :class:`RespostaExtrairLogs` a partir do retorno
        informado.

        :param unicode retorno: Retorno da função ``ExtrairLogs``.
        """
        resposta = analisar_retorno(forcar_unicode(retorno),
                funcao='ExtrairLogs',
                classe_resposta=RespostaExtrairLogs,
                campos=RespostaSAT.CAMPOS + (
                        ('arquivoLog', unicode),
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
