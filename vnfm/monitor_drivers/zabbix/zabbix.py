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
from fnmatch import fnmatchcase
OPTS = [
    cfg.StrOpt('servicename', default='apache2',
               help=_('select Service name'))
]
cfg.CONF.register_opts(OPTS, 'zabbix')




AUTHINFO = {'jsonrpc':"2.0",'method':"user.login",'params':{'user':"Admin",'password':"zabbix"},'id':1,'auth':None}


TEMP_GET_DICT = {'jsonrpc':"2.0",'method':"template.get",'params':{'output':'extend',
            'filter':{'host':["Template App HTTP Service",
            "Template App Zabbix Agent"]}},'id':1,'auth':None}


TEMP_CREATE_DICT = {'jsonrpc':"2.0",'method':"template.create",
                    'params':{'host':"Template Tacker  ",'groups':{'groupid':1}
            ,'hosts':[]},'id':1004,'auth':None}


ITEM_CREATE_DICT = {'jsonrpc':"2.0",'method':"item.create",
                    'params':{'hostid':None,'interfaceid':'NULL','name':"",'key_':"",'type':0,
                              'value_type':3,'delay':1},'id':1004,'auth':None}




ITEM_KEY_LIST={'Agent Status':'agent.ping','Network Status':'net.if.total',
               'Service Health':'net.tcp.service','maximum_pro_cpu_usage':'proc.cpu.util',
              'maximum_pro_memory_usage':'proc.mem','maximum_cpu_memory_usage':'system.cpu.util',
               'maximum_cpu_load_usage':'system.cpu.load','Process Number':'proc.num',
               'Total Memory Size':'vm.memory.size[total]','Swap Size':'system.swap.size'}


TRIGGER_CREATE_DICT={'jsonrpc':"2.0",'method':"trigger.create",'templateid': None ,'auth':None,'id':1004}

TRIGGER_LIST={'Agent Status':[{'description':'Zabbix agent on {HOST.NAME} is unreachable for 5 minutes',
                                'expression':'','priority':3}],
               'Service Health':[{'description':'service is down on {HOST.NAME}','expression':'','priority':3}],
              'maximum_pro_memory_usage':[{'description':'Process Memory is lacking on {HOST.NAME}','expression':'','priority':3}],
              'maximum_cpu_memory_usage':[{'description':'Disk I/O is overloaded on {HOST.NAME}','expression':'' ,'priority':3}],
               'maximum_cpu_load_usage':[{'description':'Processor load is too high on {HOST.NAME}','expression':'','priority':3}],
              'Process Number':[{'description':'Too many processes running on {HOST.NAME}','expression':'','priority':3}]}

TINFO= {'jsonrpc':"2.0",'method':"host.get",'params':{'output':['hostid'],
                                                        'selectTriggers':'extend',
                                                      'filter':{'host':['ubuntu'],'description':['HTTP service is down on {HOST.NAME}']}},'id':1,'auth':None}


ACTION_CREATE_DICT = {'jsonrpc':"2.0",'method':"action.create",
              'params':{'name':'Trigger action','eventsource':0,'status':0,'esc_period':120,'def_shortdata':"{TRIGGER.NAME}:{TRIGGER.STATUS}",
                        'def_longdata':"{TRIGGER.NAME}: {TRIGGER.STATUS}\r\nLast value: {ITEM.LASTVALUE]\r\n\r\n{TRIGGER.URL}",

                        "filter":{"evaltype":0,"conditions":[{'conditiontype':2,'operator':0,'value':None}]},
                        'operations':[{'operationtype':1,'esc_period':0,'esc_step_from':1,
                                       'esc_step_to':2,'evaltype':0,
                                       'opcommand':{'command':None,'type':0,'execute_on':0,
                                                     },'opcommand_hst':[{'hostid':None}]}]
                        },'auth':None,'id':1}

ACTION_CMD_LIST={'Service Health':'sudo service apache2 restart'}



HOST_CREATE_INFO = {'jsonrpc':"2.0",'method':"host.create",'params':{'host':'ubuntu',
                     'interfaces':[{'type':1,'main':1,'useip':1,'dns':"",'ip':None,'port':"10050"}],
                      'templates':[{'templateid':None}],'groups':[{'groupid':None}]},'id':4,'auth':None}




GROUP_GET_INFO = {'jsonrpc':"2.0",'method':"hostgroup.get",'params':{'output':'extend','filter':{'name':["Zabbix servers",]}},'id':1,'auth':None}

GRAPH_CREATE_DICT = {'jsonrpc':'2.0','method':'graph.create','params':{'name':None,'width':900,'height':200,
                                                                       'gitems':[]},'auth':None,'id':1004}

URL = 'http://192.168.11.53:80/zabbix/api_jsonrpc.php'
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

    def send_post(self,query):
        response = requests.post(URL, headers=HEADERS, data=json.dumps(query))
        return dict(response.json())

    def create_graph(self,token,itemid,name):
        GRAPH_C_DICT = GRAPH_CREATE_DICT
        GRAPH_C_DICT['auth'] = token


        gitems= [{'itemid':itemid,'color':'00AA00'}]

        GRAPH_C_DICT['params']['gitems']=gitems
        GRAPH_C_DICT['params']['name'] = name
        print('GRAPH_C_DICT',GRAPH_C_DICT)
        response = self.send_post(GRAPH_C_DICT)
        print('response',response)




    def create_action(self,token,triggerid,hostid,servicename):
        ACTION_C_DICT= ACTION_CREATE_DICT
        ACTION_C_DICT['auth'] = token

        ACTION_C_DICT['params']['operations'][0]['opcommand_hst'][0]['hostid'] = hostid[0]
        ACTION_C_DICT['params']['operations'][0]['opcommand']['command'] = ACTION_CMD_LIST[servicename]
        ACTION_C_DICT['params']['filter']['conditions'][0]['value'] = triggerid[0]
        print('ACTION_C_DICT ',ACTION_C_DICT)
        response = self.send_post(ACTION_C_DICT)
        return response

    def create_trigger(self,token,trigger_params,templateid):
        TRIGGER_C_DICT = TRIGGER_CREATE_DICT
        TRIGGER_C_DICT['auth'] =token
        TRIGGER_C_DICT['params'] = trigger_params
        TRIGGER_C_DICT['templateid']=templateid
        print('##############################################')
        print('##############################################')
        print("TRIGGER_C_DICTTRIGGER_C_DICTTRIGGER_C_DICT",TRIGGER_C_DICT)
        response = self.send_post(TRIGGER_C_DICT)
        print("response : ",response)
        print('##############################################')
        print('##############################################')
        return response



    def create_trigger_param(self):
        pass


    def create_item(self,parameters,token,vduname,tempid,tempname):

        ITEM_C_DICT = ITEM_CREATE_DICT
        ITEM_C_DICT['auth'] = token
        TRIGGER_P_DICT=TRIGGER_LIST
        print("parameters : ",parameters)




        maximum_high_pro_value = parameters['maximum_high_pro_value']
        maximum_cpu_memory_usage = parameters['maximum_cpu_memory_usage']
        maximum_cpu_load_usage = parameters['maximum_cpu_load_usage']
        maximum_pro_memory_usage = parameters['service']['maximum_pro_memory_usage']

        print('##############################################')
        print('##############################################')

        print('SERVICE PARAMETERS :',parameters['service'])

        print('##############################################')
        print('##############################################')
        trigger_params = []

        serviceid = None
        servicename = None

        #2. Create ITEM

        ITEM_C_DICT['params']['hostid'] = int(tempid)


        #Agent Status
        ITEM_C_DICT['params']['name'] = 'Zabbix Agent Status Check'
        ITEM_C_DICT['params']['key_'] = str(ITEM_KEY_LIST['Agent Status'])
        ITEM_C_DICT['params']['value_type'] = 3
        response = self.send_post(ITEM_C_DICT)

        TRIGGER_P_DICT['Agent Status'][0]['expression']='{' + tempname+':'+ ITEM_KEY_LIST['Agent Status']+'.nodata(5m)}=1'


        trigger_params.append(TRIGGER_P_DICT['Agent Status'][0])

        print('##############################################')
        print('##############################################')
        print('TRIGGER_P_DICT[Agent Status] : ',TRIGGER_P_DICT['Agent Status'])
        print('trigger_params : ', trigger_params)
        print('##############################################')
        print('##############################################')

        # Network Status
        temp = '[' + 'ens3' + ']'
        ITEM_C_DICT['params']['name'] = 'Network Status Check'
        ITEM_C_DICT['params']['key_'] = str(ITEM_KEY_LIST['Network Status'] + temp)
        ITEM_C_DICT['params']['value_type'] = 3
        self.send_post(ITEM_C_DICT)
        ###Call create_function
        # self.create_trigger()



            # this code is find servicesssss
            # if you all service check status shell script make
            # so we don't need this if code
        for item in parameters.keys():
            if  item =='service' :
                for item in parameters['service'].keys():
                    if item == 'servicename':
                        if parameters['service'][item] == 'apache2':
                            temp='['+'http'+']'
                            #net.tcp.service[service,<ip>,<port>]
                            ITEM_C_DICT['params']['name'] = 'Apache2 Status Check'
                            ITEM_C_DICT['params']['key_'] = str(ITEM_KEY_LIST['Service Health'] +temp)
                            ITEM_C_DICT['params']['value_type']=3

                            response = self.send_post(ITEM_C_DICT)

                            TRIGGER_P_DICT['Service Health'][0]['expression'] = '{' + tempname + ':' + \
                                                                              ITEM_C_DICT['params']['key_'] +'.max(#3)}=0'

                            print('response',response)
                            response = self.create_trigger(token,TRIGGER_P_DICT['Service Health'][0],tempid)
                            print('response', response)
                            serviceid =response['result']['triggerids']
                            servicename = 'Service Health'




                        else:
                            # net.tcp.service[service,<ip>,<port>]
                            temp='['+parameters['service']['servicename']+']'
                            ITEM_C_DICT['params']['name'] = 'Service Status Check'
                            ITEM_C_DICT['params']['key_'] = str(ITEM_KEY_LIST['Service Health'] +temp)
                            ITEM_C_DICT['params']['value_type']=3
                            result =  self.send_post(ITEM_C_DICT)


                            TRIGGER_P_DICT['Service Health'][0]['expression'] = '{' + tempname + ':' + \
                                                                                ITEM_C_DICT['params'][
                                                                                    'key_'] + '.max(#3)}=0'
                            trigger_params.append(TRIGGER_P_DICT['Service Health'][0])


                            ###Call create_function


                            print('RESULT : ',result)
                    else :

                            # proc.cpu.util[<name>,<user>,<mode>,<cmdline>,<memtype>,<zone>] = >  process CPU util


                            temp  = '[' + parameters['service']['servicename'] + ',root]'
                            ITEM_C_DICT['params']['key_'] = str(ITEM_KEY_LIST[item]) + temp

                            if item == 'maximum_pro_cpu_usage' :

                                 pass

                            else:
                                # proc.mem[<name>,<user>,<mode>,<cmdline>,<memtype>] = >  process usage memory
                                ITEM_C_DICT['params']['value_type'] = 3
                                ITEM_C_DICT['params']['name'] = 'Service '+ parameters['service']['servicename']+ 'Memory Usage'

                                print("ITEM_C_DICT ", ITEM_C_DICT)
                                result = self.send_post(ITEM_C_DICT)
                                self.create_graph(token, result['result']['itemids'][0],
                                                  ITEM_C_DICT['params']['name'] + ' Graph')

                                TRIGGER_P_DICT['maximum_pro_memory_usage'][0]['expression'] = '{' + tempname + ':' + \
                                                                                              ITEM_C_DICT['params'][
                                                                                                  'key_'] + '.avg(5)}>'+str(maximum_pro_memory_usage)
                                trigger_params.append(TRIGGER_P_DICT['maximum_pro_memory_usage'][0])

                                print('RESULT : ', result)
            elif item == 'maximum_high_pro_value' :
                temp = '[,,run]'
                # procnum[<name>,<user>,<state>,<cmdline>]
                ITEM_C_DICT['params']['name'] = 'Process Number'
                ITEM_C_DICT['params']['key_'] = str(ITEM_KEY_LIST['Process Number'] + temp)
                ITEM_C_DICT['params']['value_type'] =3
                print("ITEM_C_DICT ITEM_C_DICT", ITEM_C_DICT)
                result = self.send_post(ITEM_C_DICT)
                self.create_graph(token, result['result']['itemids'][0],ITEM_C_DICT['params']['name']+' Graph')
                print('result ' ,result)


                print('type maximum_high_pro_value ',type(maximum_high_pro_value))


                TRIGGER_P_DICT['Process Number'][0]['expression'] = '{' + tempname + ':' + ITEM_C_DICT['params']['key_'] + '.avg(5s)}>' + str(maximum_high_pro_value)
                print('TRIGGER_P_DICT',TRIGGER_P_DICT)
                print('maximum_high_pro_value',maximum_high_pro_value)
                print('type maximum_high_pro_value ',type(maximum_high_pro_value))

                trigger_params.append(TRIGGER_P_DICT['Process Number'][0])


                ###Call create_function


                print('RESULT : ', result)
            elif item == 'maximum_cpu_memory_usage':
                temp = '[,iowait]'
                # system.cpu.util<cpu>,<mode>] => CPU Usage
                ITEM_C_DICT['params']['name'] = 'CPU Utill Usage'
                ITEM_C_DICT['params']['key_'] = str(ITEM_KEY_LIST['maximum_cpu_memory_usage'] + temp)
                ITEM_C_DICT['params']['value_type'] = 0
                print("ITEM_C_DICT ", ITEM_C_DICT)
                result = self.send_post(ITEM_C_DICT)
                self.create_graph(token, result['result']['itemids'][0], ITEM_C_DICT['params']['name'] + ' Graph')
                TRIGGER_P_DICT['maximum_cpu_memory_usage'][0]['expression'] = '{' + tempname + ':' + \
                                                                           ITEM_C_DICT['params'][
                                                                               'key_'] + '.avg(1m)}>' +str(maximum_cpu_memory_usage)

                trigger_params.append(TRIGGER_P_DICT['maximum_cpu_memory_usage'][0])


            elif item ==  'maximum_cpu_load_usage':
                temp = '[percpu,avg1]'
                #system.cpu.load[<cpu>,<mode>]
                ITEM_C_DICT['params']['name'] = 'CPU Load'
                ITEM_C_DICT['params']['key_'] = str(ITEM_KEY_LIST['maximum_cpu_load_usage'] + temp)
                ITEM_C_DICT['params']['value_type'] = 0
                print("ITEM_C_DICT ", ITEM_C_DICT)
                result = self.send_post(ITEM_C_DICT)
                self.create_graph(token, result['result']['itemids'][0], ITEM_C_DICT['params']['name'] + ' Graph')
                TRIGGER_P_DICT['maximum_cpu_load_usage'][0]['expression'] = '{' + tempname + ':' + \
                                                                           ITEM_C_DICT['params'][
                                                                               'key_'] + '.avg(1m)}>' + str(maximum_cpu_load_usage)
                print('TRIGGER_P_DICT[maximum_cpu_load_usage][0][expression]',TRIGGER_P_DICT['maximum_cpu_load_usage'][0]['expression'])

                trigger_params.append(TRIGGER_P_DICT['maximum_cpu_load_usage'][0])

        print("TRIGGERPARAMSTRIGGERPARAMSTRIGGERPARAMSTRIGGERPARAMSTRIGGERPARAMS")
        print('trigger_params',trigger_params)
        response = self.create_trigger(token, trigger_params, tempid)
        print('response' ,response)

        trigger_params = []
        return serviceid,servicename


    def create_template(self,kwagrs,token,vduname):
        parameters = kwagrs['vdus'][vduname[0]]['parameters']
        TEMP_C_DICT = TEMP_CREATE_DICT
        server_token = token


        # 1. create template
        if str(vduname[0]) not in TEMP_C_DICT['params']['host']:
            TEMP_C_DICT['params']['host'] += str(vduname[0])
        TEMP_C_DICT['auth'] = server_token
        print("TEMP_CREATE_DICT : ", TEMP_C_DICT)
        temp_create_response = self.send_post(TEMP_C_DICT)
        print("temp_create_response : ",temp_create_response)
        tmpid= temp_create_response['result']['templateids'][0]


        #Call Create ITEM FUNCTION

        serviceid,servicename = self.create_item(parameters, token, vduname, tmpid,TEMP_C_DICT['params']['host'])
        return tmpid,serviceid,servicename







    def add_host_create_api(self,kwargs,token):

        HOST_C_DICT = HOST_CREATE_INFO
        GROUP_G_DICT = GROUP_GET_INFO
        vduname = [node for node in kwargs['vdus'] if fnmatchcase(node, 'VDU*')]
        mgmt_ip =  kwargs['vdus'][vduname[0]]['mgmt_ip']
        zbx_admin_passwd= kwargs['vdus'][vduname[0]]['parameters']['zabbix_admin_passwd']

        zabbix_server_ip =kwargs['vdus'][vduname[0]]['parameters']['zabbix_server_ip']

        # 1. create TEMPLATE(ITEM, TRIGGER,ACTION)
        tempid,servicetgrid,servicetgrname = self.create_template(kwargs,token,vduname)

        # 2. create host
        print("########################################################")
        print("########################################################")
        print("########################################################")
        print("Line 128 add_host_create_api in zabbix.py")
        print("mgmt_ip : ",mgmt_ip)######")
        print("########################################################")


        GROUP_G_DICT['auth'] = token
        print("zbx_admin_passwd : ", zbx_admin_passwd)

        print("zabbix_server_ip : ", zabbix_server_ip)

        print("########################################################")
        print("########################################################")
        print("########################################################")


        GROUP_G_DICT['auth'] = token
        response = self.send_post(GROUP_G_DICT)

        print('response',response)
        HOST_C_DICT['auth'] = token
        HOST_C_DICT['params']['host'] = str(vduname[0]).lower()
        HOST_C_DICT['params']['interfaces'][0]['ip'] = mgmt_ip
        HOST_C_DICT['params']['templates'][0]['templateid'] = tempid
        HOST_C_DICT['params']['groups'][0]['groupid']=response['result'][0]['groupid']
        print('HOST_C_DICT',HOST_C_DICT)
        response = self.send_post(HOST_C_DICT)
        print('response',response)


        response = self.create_action(token,servicetgrid,response['result']['hostids'],servicetgrname)
        print('ACTION RESPONSE : ',response)







    def get_token_from_server(self):
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
        status_code,token = self.get_token_from_server()
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
