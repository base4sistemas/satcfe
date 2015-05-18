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

from satcomum import constantes

from .entidades import Entidade


class ConfiguracaoRede(Entidade):
    """
    Uma entidade que contém os parâmetros de configurações da interface de
    rede do equipamento SAT. Uma instância desta classe é usada como argumento
    para o método :meth:`~satcfe.base._FuncoesSAT.configurar_interface_de_rede`.

    .. sourcecode:: python

        >>> conf = ConfiguracaoRede(
        ...         tipoInter=constantes.REDE_TIPOINTER_ETHE,
        ...         tipoLan=constantes.REDE_TIPOLAN_DHCP)
        >>> ET.tostring(conf._xml())
        '<config><tipoInter>ETHE</tipoInter><tipoLan>DHCP</tipoLan></config>'

    """

    _schema = {
            'tipoInter': {
                    'type': 'string',
                    'required': True,
                    'allowed': [v for v,s in constantes.REDE_TIPOINTER_OPCOES]},
            'SSID': {
                    'type': 'string',
                    'required': False,
                    'minlength': 1, 'maxlength': 32},
            'seg': {
                    'type': 'string',
                    'required': False,
                    'allowed': [v for v,s in constantes.REDE_SEG_OPCOES]},
            'codigo': {
                    'type': 'string',
                    'required': False,
                    'minlength': 1, 'maxlength': 64},
            'tipoLan': {
                    'type': 'string',
                    'required': True,
                    'allowed': [v for v,s in constantes.REDE_TIPOLAN_OPCOES]},
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
                    'allowed': [v for v,s in constantes.REDE_PROXY_OPCOES]},
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
        }


    def _construir_elemento_xml(self, *args, **kwargs):

        config = ET.Element('config')

        for elemento in self._schema.keys():
            valor = getattr(self, elemento, None)
            if valor:
                ET.SubElement(config, elemento).text = valor

        return config
