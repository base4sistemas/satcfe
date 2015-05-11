# -*- coding: utf-8 -*-
#
# satcfe/config.py
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


class ConfiguracoesSATHub(object):

    host = '10.0.0.117'
    """
    Nome ou endereço IP do host para o SATHub.
    """

    port = 5000
    """
    Número da porta em que o serviço HTTP responde.
    """

    baseurl = '/hub/v1/'
    """
    Prefixo base da URL para os serviços da API.
    """

    username = 'ninguem'
    """
    Nome de usuário para autenticação na API do serviço RESTful.
    """

    password = ''
    """
    Senha do usuário para autenticação na API do serviço RESTful.
    """


class Configuracoes(object):

    codigo_ativacao = '123456789'
    """
    Código de ativação. Senha definida pelo contribuinte no software de
    ativação, conforme item 2.1.1 da ER SAT.
    """

    numero_caixa = 1
    """
    Número do caixa, conforme atributo B14 do item 4.2.2 da ER SAT.
    Deve ser um número inteiro entre 0 e 999.
    """

    sathub = ConfiguracoesSATHub()
    """
    Configurações para acesso à API RESTful SATHub.
    """


conf = Configuracoes()
