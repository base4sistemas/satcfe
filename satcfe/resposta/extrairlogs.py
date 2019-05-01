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
import os
import tempfile

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
        EEEEE (str)
        mensagem (str)
        cod (str)
        mensagemSEFAZ (str)
        arquivoLog (str)

    Em caso de falha, são esperados apenas os atributos padrão, conforme
    descrito na constante :attr:`~satcfe.resposta.padrao.RespostaSAT.CAMPOS`.
    """

    def conteudo(self):
        """Retorna o conteúdo do log decodificado."""
        return base64_to_str(self.arquivoLog)


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

        :raises FileExistsError: Se o destino informado já existir.
        """
        if destino:
            if os.path.exists(destino):
                raise FileExistsError(destino)
            fd = os.open(destino, 'w', encoding='utf-8')
        else:
            fd, destino = tempfile.mkstemp(prefix=prefix, suffix=suffix)

        os.write(fd, self.conteudo())
        os.fsync(fd)
        os.close(fd)

        return destino


    @staticmethod
    def analisar(retorno):
        """Constrói uma :class:`RespostaExtrairLogs` a partir do retorno
        informado.

        :param str retorno: Retorno da função ``ExtrairLogs``.
        """
        resposta = analisar_retorno(retorno,
                funcao='ExtrairLogs',
                classe_resposta=RespostaExtrairLogs,
                campos=RespostaSAT.CAMPOS + (
                        ('arquivoLog', str),
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
