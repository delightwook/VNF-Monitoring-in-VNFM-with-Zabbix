# All Rights Reserved.
#
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import abc

import six
import json
import requests
from oslo_config import cfg

from tacker.api import extensions

OPTS = [
    cfg.StrOpt('servicename', default='apache2',
               help=_('select Service name'))
]
cfg.CONF.register_opts(OPTS, 'zabbix')

AUTHINFO = {'jsonrpc':"2.0",'method':"user.login",'params':{'user':"Admin",'password':"zabbix"},'id':1,'auth':"null"}
URL = 'http://220.70.2.143:7778/zabbix'
HEADERS={'Content-Type':'application/json-rpc'}


class VNFMonitorZabbix(extensions.PluginInterface):


    def get_type(self):
        """Return one of predefined type of the hosting vnf drivers."""
        return 'zabbix'



    def get_name(self):
        """Return a symbolic name for the VNF Monitor plugin."""
        return 'zabbix'



    def get_description(self):
        """Return description of VNF Monitor plugin."""
        return 'Tacker VNFMonitor Zabbix Driver'

    def monitor_get_config(self, plugin, context, vnf):
        """Return dict of monitor configuration data.

        :param plugin:
        :param context:
        :param vnf:
        :returns: dict
        :returns: dict of monitor configuration data
        """
        return {}


    def monitor_url(self, plugin, context, vnf):
        """Return the url of vnf to monitor.

        :param plugin:
        :param context:
        :param vnf:
        :returns: string
        :returns: url of vnf to monitor
        """

        pass

    def create_api(self,kwargs):
        pass


    def connect_to_server(self):
        # reponse = requests.get(URL,headers=HEADERS,data=json.dumps(AUTHINFO))
        reponse = requests.get(URL)

        print("###################################################")
        print("###################################################")
        print("###################################################")
        print("Line 87 conntect_to_server in zabbix.py")
        print("repose : ",reponse)
        print("###################################################")
        print("###################################################")
        print("###################################################")





    def add_to_svcmonitor(self, vnf, kwargs):
        self.connect_to_server()
        print("###################################################")
        print("###################################################")
        print("###################################################")
        print("Line 76 add_to_zabbix in zabbix.py")
        print("kwargs : ",kwargs)
        print("###################################################")
        print("###################################################")
        print("###################################################")


    def monitor_call(self, vnf, kwargs):
        pass

    def monitor_service_driver(self, plugin, context, vnf,
                               service_instance):
        # use same monitor driver to communicate with service
        return self.get_name()
