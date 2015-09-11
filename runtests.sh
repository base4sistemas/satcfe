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
# Executa os testes contra um equipamento SAT em ambiente de desenvolvimento,
# evitando funções que não são possíveis de serem executadas sem um contexto
# ou parametrização específica. Por exemplo, é possível executar as funções
# `ConsultarSAT` ou `ConsultarStatusOperacional`, mas não `AtivarSAT` ou
# `BloquearSAT`
# Cada equipamento SAT irá requerer certos parâmetros conforme o fabricante:
#
# Tanca SDK-1000 [www.tanca.com.br]
#
#    --cnpj-ac=16716114000172
#    --emitente-cnpj=08723218000186
#    --emitente-ie=149626224113
#    --emitente-im=123123
#    --emitente-issqn-regime=3
#    --emitente-issqn-rateio=N
#    --codigo-ativacao=12345678
#
# Dimep D-Sat [www.dimep.com.br]
#
#    --cnpj-ac=08427847000169
#    --emitente-cnpj=61099008000141
#    --emitente-ie=111111111111
#    --emitente-im=12345
#    --emitente-issqn-regime=3
#    --emitente-issqn-rateio=N
#    --codigo-ativacao=123456789
#
# Bematech RB-1000 FI [www.bematech.com.br]
#
#    --cnpj-ac=16716114000172
#    --emitente-cnpj=82373077000171
#    --emitente-ie=816000002213
#    --emitente-im=123123
#    --emitente-issqn-regime=3
#    --emitente-issqn-rateio=N
#    --codigo-ativacao=12345678
#
# As configurações abaixo são para o equipamento SAT Tanca SDK-1000.
# Configure o caminho correto para a sua DLL conforme seu sistema
# operacional e arquitetura. Por exemplo:
#
#     $ export SATCFE_TEST_DLL=/home/user/tanca/linux/libsat64.so
#     $ export SATCFE_TEST_DLLCONV=1
#
# A convenção de chamada é definida no projeto SATComum [1], no módulo
# `satcomum.contantes`. As convenções de chamada são:
#
#     1 - Standard C
#     2 - Windows "stdcall"
#
# [1] https://github.com/base4sistemas/satcomum
#

: ${SATCFE_TEST_DLL:?"Defina SATCFE_TEST_DLL apontando para a DLL/SO SAT"}
: ${SATCFE_TEST_DLLCONV:?"Defina SATCFE_TEST_DLLCONV conforme convencao de chamada para a DLL/SO SAT "}

if [ ! -f $SATCFE_TEST_DLL ]
then
    echo "DLL/SO SAT nao pode ser encontrada"
    echo "SATCFE_TEST_DLL=\"$SATCFE_TEST_DLL\""
    echo ""
    exit 1
fi

python setup.py test -a "-rs "\
"--cnpj-ac=16716114000172 "\
"--emitente-cnpj=08723218000186 "\
"--emitente-ie=149626224113 "\
"--emitente-im=123123 "\
"--emitente-uf=SP "\
"--emitente-issqn-regime=3 "\
"--emitente-issqn-rateio=N "\
"--codigo-ativacao=12345678 "\
"--dll-caminho=$SATCFE_TEST_DLL "\
"--dll-convencao=$SATCFE_TEST_DLLCONV "
