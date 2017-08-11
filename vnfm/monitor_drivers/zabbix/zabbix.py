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

AUTHINFO = {'jsonrpc':"2.0",'method':"user.login",'params':{'user':"Admin",'password':"zabbix"},'id':1,'auth':None}
ADDINFO = {'jsonrpc':"2.0",'method':"",'params':{'host':'ubuntu',
                     'interfaces':[{'type':1,'main':1,'useip':1,'dns':"",'ip':None,'port':"10050"}],
                      'templates':[{'templateid':None},{'templateid':None}],'groups':[{'groupid':None}]},'id':4,'auth':None}
# ADDINFO = {'jsonrpc':"2.0",'method':"",'params':{'host':'ubuntu','interfaces':[{'ip':None,'port':"10050"}]
#                                                  ,'groups':[{'groupid':None}]},'id':452,'auth':None}

GROUPINFO = {'jsonrpc':"2.0",'method':"hostgroup.get",'params':{'output':'extend','filter':{'name':["Zabbix servers",]}},'id':1,'auth':None}

TEMPINFO = {'jsonrpc':"2.0",'method':"template.get",'params':{'output':'extend',
            'filter':{'host':["Template App Apache Web Server zapache",
            "Template App Zabbix Agent"]}},'id':1,'auth':None}

ACTIONINFO = {'jsonrpc':"2.0",'method':"action.create",
              'params':{'name':'Trigger action','eventsource':0,'status':0,'esc_period':120,'def_shortdata':"{TRIGGER.NAME}:{TRIGGER.STATUS}",
                        'def_longdata':"{TRIGGER.NAME}: {TRIGGER.STATUS}\r\nLast value: {ITEM.LASTVALUE]\r\n\r\n{TRIGGER.URL}",

                        "filter":{"evaltype":0,"conditions":[{'conditiontype':2,'operator':0,'value':None}]},
                        'operations':[{'operationtype':1,'esc_period':0,'esc_step_from':1,
                                       'esc_step_to':2,'evaltype':0,
                                       'opcommand':{'command':'service apache2 restart','type':2,'authtype':0,'password':'root',
                                                     'port':22,'username':'root'},'opcommand_hst':[{'hostid':None}]}]
                        },'auth':None,'id':1}




TINFO= {'jsonrpc':"2.0",'method':"host.get",'params':{'output':['hostid'],
                                                        'selectTriggers':'extend','filter':{'host':['ubuntu'],'description':['Apache down on {HOST.NAME}']}},'id':1,'auth':None}

URL = 'http://192.168.11.51:80/zabbix/api_jsonrpc.php'
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


    def add_trigger_action(self):
        pass



    def add_host_create_api(self,kwargs,token):
        info = ADDINFO
        ginfo = GROUPINFO
        tinfo = TEMPINFO
        aainfo = TINFO
        ainfo = ACTIONINFO
        info['method'] ='host.create'
        tinfo['auth']=token
        ginfo['auth'] = token
        info['auth'] =str(token)
        aainfo['auth'] =token
        ainfo['auth'] = token
        print("kwargs", kwargs.keys())

        print("###################################################")
        print("###################################################")
        ######################################we Sholud change this code ###########################################
        ######################################we Sholud change this code ###########################################
        ######################################we Sholud change this code ###########################################
        ######################################we Sholud change this code ###########################################
        ######################################we Sholud change this code ###########################################

        response = requests.post(URL, headers=HEADERS, data=json.dumps(ginfo))
        response_dict = dict(response.json())


###############ALL REQUEST one FUNCIO

        #
        # if 'apache2' == kwargs['vdus']['VDU1']['parameters']['servicename']:
        #     info['params']['templates'][0]['host'] = 'Template App Apache Web Server zapache'
        print("rrrrrrrrrrr", response_dict.keys())



        info['params']['interfaces'][0]['ip'] = kwargs['vdus']['VDU1']['mgmt_ip']
        info['params']['groups'][0]['groupid'] = response_dict['result'][0]['groupid']

        response = requests.post(URL, headers=HEADERS, data=json.dumps(tinfo))
        response_dict = dict(response.json())

        info['params']['templates'][0]['templateid'] = str(response_dict['result'][0]['templateid'])
        info['params']['templates'][1]['templateid'] = str(response_dict['result'][1]['templateid'])


        print("###################################################")
        print("###################################################")
        print("###################################################")
        print("Line 97 add_host_create_api in zabbix.py")
        print("info : ", info)
        print("kwargs",kwargs)

        print("###################################################")
        print("###################################################")
        print("###################################################")

        # response = requests.post(URL, headers=HEADERS, data=json.dumps(info))

        # get host id
        response = requests.post(URL,headers=HEADERS,data=json.dumps(info))

        response_dict = dict(response.json())
        print("response_dict", response_dict)
        print("response_dict", response_dict['result'])

        host_id = response_dict['result']['hostids']



        # aainfo['params']['hostids']= str(host_id)

        ## trriger infomation
        # aainfo['params']['filter']['hostid'][0] = str(host_id)
        print("aainfo", aainfo)
        response = requests.post(URL, headers=HEADERS, data=json.dumps(aainfo))
        print("####################TESTTESTSTESTETEE###################")
        print("response trigger",response)
        print("trigger",response.status_code)
        print("trigger",response.json())
        print("####################TESTTESTSTESTETEE###################")
        print("####################TESTTESTSTESTETEE###################")
        print("####################TESTTESTSTESTETEE###################")
        print("####################TESTTESTSTESTETEE###################")

        temp = dict(response.json())
        print("trigger item ",temp['result'][0]['triggers'][0]['triggerid'])
        triggerid = temp['result'][0]['triggers'][0]['triggerid']


        ##create action
        ainfo['params']['filter']['conditions'][0]['value']=triggerid
        ainfo['params']['operations'][0]['opcommand_hst'][0]['hostid'] = host_id[0]
        print("####################AAAAAAAAAAAAAAAAAAAAA###################")
        print('afino',ainfo)
        response = requests.post(URL, headers=HEADERS, data=json.dumps(ainfo))
        temp = dict(response.json())
        print('action result: ',temp )












    def connect_to_server(self):
        # reponse = requests.post(URL,headers=HEADERS,data=json.dumps(INFO))
        response = requests.post(URL, headers=HEADERS, data=json.dumps(AUTHINFO))
        response_dict = dict(response.json())

        print("###################################################")
        print("###################################################")
        print("###################################################")
        print("Line 87 conntect_to_server in zabbix.py")
        print("repose : ", response.status_code)
        print("repose.token: ",response_dict['result'])
        print("repose.token: ", type(response_dict))
        print("###################################################")
        print("###################################################")
        print("###################################################")
        return response.status_code,response_dict['result']





    def add_to_svcmonitor(self, vnf, kwargs):
        status_code,token = self.connect_to_server()
        self.add_host_create_api(kwargs,token)

        print("###################################################")
        print("###################################################")
        print("###################################################")
        print("Line 141 add_to_svcmonitot in zabbix.py")
        print("###################################################")
        print("###################################################")
        print("###################################################")


    def monitor_call(self, vnf, kwargs):
        pass

    def monitor_service_driver(self, plugin, context, vnf,
                               service_instance):
        # use same monitor driver to communicate with service
        return self.get_name()
