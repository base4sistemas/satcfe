# -*- coding: utf-8 -*-
#
# satcfe/rede.py
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

import xml.etree.ElementTree as ET

from satcomum.constantes import REDE_TIPOINTER_OPCOES
from satcomum.constantes import REDE_SEG_OPCOES
from satcomum.constantes import REDE_TIPOLAN_OPCOES
from satcomum.constantes import REDE_PROXY_OPCOES

from .entidades import Entidade


class ConfiguracaoRede(Entidade):
    """Uma entidade que contém os parâmetros de configurações da interface de
    rede do equipamento SAT. Uma instância desta classe é usada como argumento
    para o método :meth:`~satcfe.base._FuncoesSAT.configurar_interface_de_rede`.

    :param str tipoInter: Tipo de interface de rede que o equipamento SAT
        deverá utilizar. As opções de tipos de rede estão disponíveis na
        constante :attr:`~satcomum.constantes.REDE_TIPOINTER_OPCOES`.

    :param str SSID: *Opcional* Nome da rede sem fio, se for o caso, contendo
        até 32 caracteres.

    :param str seg: *Opcional* Tipo de segurança da rede sem fio. As opções
        estão na constante :attr:`~satcomum.constantes.REDE_SEG_OPCOES`.

    :param str codigo: *Opcional* Senha de acesso à rede sem fio, contendo
        até 64 caracteres.

    :param str tipoLan: Tipo da rede LAN. As opções estão disponíveis na
        constante :attr:`~satcomum.constantes.REDE_TIPOLAN_OPCOES`.

    :param str lanIP: *Opcional* Endereço IP do equipamento SAT.

    :param str lanMask: *Opcional* Máscara de sub-rede.

    :param str lanGW: *Opcional* Endereço IP do gateway padrão.

    :param str lanDNS1: *Opcional* Endereço IP do DNS primário.

    :param str lanDNS2: *Opcional* Endereço IP do DNS secundário.

    :param str usuario: *Opcional* Nome do usuário para obtenção do endereço IP,
        se necessário, contendo até 64 caracteres.

    :param str senha: *Opcional* Senha do usuário para obtenção do endereço IP,
        relacionado ao parâmetro ``usuario``, se necessário, contendo até 32
        caracteres.

    :param str proxy: *Opcional* Indica a configuração de proxy da rede.
        As opções estão disponíveis na
        constante :attr:`~satcomum.constantes.REDE_PROXY_OPCOES`.

    :param str proxy_ip: *Opcional* Endereço IP do servidor proxy.

    :param int proxy_porta: *Opcional* Número da porta por onde o servidor de
        proxy responde.

    :param str proxy_user: *Opcional* Nome do usuário para acesso ao proxy, se
        necessário, contendo até 64 caracteres.

    :param str proxy_senha: *Opcional* Senha do usuário para acesso ao proxy,
        relacionado ao parâmetro ``proxy_user``, se necessário, contendo
        até 64 caracteres.

    .. sourcecode:: python

        >>> from satcomum import constantes
        >>> conf = ConfiguracaoRede(
        ...         tipoInter=constantes.REDE_TIPOINTER_ETHE,
        ...         tipoLan=constantes.REDE_TIPOLAN_DHCP)
        >>> ET.tostring(conf._xml())
        '<config><tipoInter>ETHE</tipoInter><tipoLan>DHCP</tipoLan></config>'

    """

    def __init__(self, **kwargs):
        super(ConfiguracaoRede, self).__init__(schema={
                'tipoInter': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in REDE_TIPOINTER_OPCOES]},
                'SSID': {
                        'type': 'string',
                        'required': False,
                        'minlength': 1, 'maxlength': 32},
                'seg': {
                        'type': 'string',
                        'required': False,
                        'allowed': [v for v,s in REDE_SEG_OPCOES]},
                'codigo': {
                        'type': 'string',
                        'required': False,
                        'minlength': 1, 'maxlength': 64},
                'tipoLan': {
                        'type': 'string',
                        'required': True,
                        'allowed': [v for v,s in REDE_TIPOLAN_OPCOES]},
                'lanIP': {
                        'type': 'ipv4',
                        'required': False},
                'lanMask': {
                        'type': 'ipv4',
                        'required': False},
                'lanGW': {
                        'type': 'ipv4',
                        'required': False},
                'lanDNS1': {
                        'type': 'ipv4',
                        'required': False},
                'lanDNS2': {
                        'type': 'ipv4',
                        'required': False},
                'usuario': {
                        'type': 'string',
                        'required': False,
                        'minlength': 1, 'maxlength': 64},
                'senha': {
                        'type': 'string',
                        'required': False,
                        'minlength': 1, 'maxlength': 64},
                'proxy': {
                        'type': 'string',
                        'required': False,
                        'allowed': [v for v,s in REDE_PROXY_OPCOES]},
                'proxy_ip': {
                        'type': 'ipv4',
                        'required': False},
                'proxy_porta': {
                        'type': 'integer',
                        'required': False,
                        'min': 0, 'max': 65535},
                'proxy_user': {
                        'type': 'string',
                        'required': False,
                        'minlength': 1, 'maxlength': 64},
                'proxy_senha': {
                        'type': 'string',
                        'required': False,
                        'minlength': 1, 'maxlength': 64},
            }, **kwargs)


    def _construir_elemento_xml(self, *args, **kwargs):
        config = ET.Element('config')
        for elemento in self._schema.keys():
            valor = getattr(self, elemento, None)
            if valor:
                ET.SubElement(config, elemento).text = valor
        return config
