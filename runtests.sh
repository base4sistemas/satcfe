#!/bin/bash
#
# runtests.sh
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

#
#  Executa os testes contra um equipamento SAT em ambiente de desenvolvimento,
#  evitando funções que não são possíveis de serem executadas sem um contexto
#  ou parametrização específica. Por exemplo, é possível executar as funções
#  `ConsultarSAT` ou `ConsultarStatusOperacional`, mas não é possível testar
#  `AtivarSAT` ou `BloquearSAT`, por exemplo.
#
#  Para executar os testes, configure o caminho para a biblioteca SAT, a
#  convenção de chamada, e o código de ativação do seu equipamento:
#
#      $ export SATCFE_TEST_LIB=/opt/fabricante/libsat.so
#      $ export SATCFE_TEST_LIB_CONVENCAO=1
#      $ export SATCFE_TEST_CODIGO_ATIVACAO=12345678
#      $ export SATCFE_TEST_EMITENTE_UF=SP
#
#  A convenção de chamada é definida no projeto SATComum [1], no módulo
#  `satcomum.contantes`. As convenções de chamada são:
#
#      1 - Standard C
#      2 - Windows "stdcall"
#
# [1] https://github.com/base4sistemas/satcomum
#

: ${SATCFE_TEST_LIB:?"Defina SATCFE_TEST_LIB apontando para a biblioteca SAT"}
: ${SATCFE_TEST_LIB_CONVENCAO:?"Defina SATCFE_TEST_LIB_CONVENCAO conforme convenção de chamada para a biblioteca SAT"}
: ${SATCFE_TEST_CODIGO_ATIVACAO:?"Defina SATCFE_TEST_CODIGO_ATIVACAO com o código de ativação do equipamento SAT"}
: ${SATCFE_TEST_EMITENTE_UF:?"Defina SATCFE_TEST_EMITENTE_UF com a sigla do Estado do domicílio fiscal do equipamento SAT"}

if [ ! -f $SATCFE_TEST_LIB ]
then
    echo "Biblioteca SAT nao pode ser encontrada"
    echo "SATCFE_TEST_LIB=\"$SATCFE_TEST_LIB\""
    echo ""
    exit 1
fi

case "$1" in
    tanca)
        SATCFE_TEST_CNPJ_AC=16716114000172
        SATCFE_TEST_EMITENTE_CNPJ=08723218000186
        SATCFE_TEST_EMITENTE_IE=149626224113
        SATCFE_TEST_EMITENTE_IM=123123
        SATCFE_TEST_EMITENTE_ISSQN_REGIME=3
        SATCFE_TEST_EMITENTE_ISSQN_RATEIO=N
    ;;

    dimep)
        SATCFE_TEST_CNPJ_AC=08427847000169
        SATCFE_TEST_EMITENTE_CNPJ=61099008000141
        SATCFE_TEST_EMITENTE_IE=111111111111
        SATCFE_TEST_EMITENTE_IM=12345
        SATCFE_TEST_EMITENTE_ISSQN_REGIME=3
        SATCFE_TEST_EMITENTE_ISSQN_RATEIO=N
    ;;

    bema)
        SATCFE_TEST_CNPJ_AC=16716114000172
        SATCFE_TEST_EMITENTE_CNPJ=82373077000171
        SATCFE_TEST_EMITENTE_IE=816000002213
        SATCFE_TEST_EMITENTE_IM=123123
        SATCFE_TEST_EMITENTE_ISSQN_REGIME=3
        SATCFE_TEST_EMITENTE_ISSQN_RATEIO=N
    ;;

    *)
        if [ -n "$1" ]; then
            echo "Argumento \"$1\" desconhecido"
        else
            echo "Nenhum argumento informado"
        fi

        echo "Informe um dos argumentos: bema, dimep ou tanca"
        echo "    bema   Bematech RB-1000 FI"
        echo "    dimep  Dimep D-Sat"
        echo "    tanca  Tanca SDK-1000"
        echo ""
        exit 1;

esac

# Adicione ou remova funções da biblioteca SAT que quer invocar
# ou deixar de invocar.
pytest -a "-rs "\
"--cnpj-ac=$SATCFE_TEST_CNPJ_AC "\
"--emitente-cnpj=$SATCFE_TEST_EMITENTE_CNPJ "\
"--emitente-ie=$SATCFE_TEST_EMITENTE_IE "\
"--emitente-im=$SATCFE_TEST_EMITENTE_IM "\
"--emitente-uf=$SATCFE_TEST_EMITENTE_UF "\
"--emitente-issqn-regime=$SATCFE_TEST_EMITENTE_ISSQN_REGIME "\
"--emitente-issqn-rateio=$SATCFE_TEST_EMITENTE_ISSQN_RATEIO "\
"--codigo-ativacao=$SATCFE_TEST_CODIGO_ATIVACAO "\
"--lib-caminho=$SATCFE_TEST_LIB "\
"--lib-convencao=$SATCFE_TEST_LIB_CONVENCAO "\
"--acessa-sat "\
"--invoca-consultarsat "\
"--invoca-consultarstatusoperacional "
