# Copyright (C) 2013 Nippon Telegraph and Telephone Corporation.
# Copyright (C) 2013 YAMAMOTO Takashi <yamamoto at valinux co jp>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import eventlet
import struct
# BGPSpeaker needs sockets patched

from ryu.services.protocols.bgp.bgpspeaker import BGPSpeaker
from mong import IodefJson

eventlet.monkey_patch()

from ryu.base import app_manager

from ryu.services.protocols.bgp.peer import *
from ryu.lib import hub
from pymongo import MongoClient
from ryu.lib.xflow import netflow_collector
from ryu.lib import sdni_collector
from ryu.controller import ofp_event
from ryu.controller.handler import set_ev_cls
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from simple_switch_13 import SimpleSwitch13
import curly
from address_creation import AC
from restful_marinos import Switch
class Bgp_sender(app_manager.RyuApp):
    _CONTEXTS = {
        'netflow_collector': netflow_collector.NetFlowCollector,
        'sdni_collector': sdni_collector.SdniCollector
    }

    def __init__(self, *args, **kwargs):
        super(Bgp_sender, self).__init__(*args, **kwargs)
        self.counter=0
        self.uri_enabled_capability=False
        self.peer={}
	self.client=MongoClient()
	self.db=self.client.connections
        self.thread=hub.spawn_after(0,self.bgp_sender)



    # Get sdni_uri that point to iodef file
    @set_ev_cls(sdni_collector.EventSdni, sdni_collector.SDNI_EV_DISPATCHER)
    def dump_msg(self, ev):
           print ev.msg

    def ipaddr_to_str(self, ip):
        return socket.inet_ntoa(struct.pack('!I', ip))

    @set_ev_cls(netflow_collector.EventNetFlow,
                netflow_collector.NETFLOW_EV_DISPATCHER)
    def dump_flow(self, ev):
        msg = ev.msg
        flows=msg.flows
        for i in range(msg.count):
        #    print  ('Flow%d: %s -> %s ', i,
        #             self.ipaddr_to_str(flows[i].srcaddr),
        #             self.ipaddr_to_str(flows[i].dstaddr))
	    
	   res= self.db.stat.find_one({
		'srcaddr'   : self.ipaddr_to_str(flows[i].srcaddr) 	,
	    	'dstaddr'   : self.ipaddr_to_str(flows[i].dstaddr)      })
	   if res==None:
		self.db.stat.insert({
                'srcaddr'   : self.ipaddr_to_str(flows[i].srcaddr)      ,
                'dstaddr'   : self.ipaddr_to_str(flows[i].dstaddr)      })
 	   #self.speaker.prefix_add(self.ipaddr_to_str(flows[i].srcaddr))
	   #To update db from netflow if the src-dest ip record doesn't exist 
	'''	
	   
		'rest_stats': {
		'nexthop'   : flows[i].nexthop		   		,
		'dpkts'     : flows[i].dpkts 			   	,	
		'doctets'   : flows[i].doctets 				,     
		'first'     : flows[i].first 				,     
		'last'      : flows[i].last 				,     
		'srcport'   : flows[i].srcport 				,     
		'dstport'   : flows[i].dstport 				,     
		'tcp_flags' : flows[i].tcp_flags 			,     
		'prot'      : flows[i].prot 				,    
		'tos'       : flows[i].tos 				,     
		'src_as'    : flows[i].src_as				,     
		'dst_as'    : flows[i].dst_as 				,     
		'src_mask'  : flows[i].src_mask 			,     
		'dst_mask'  : flows[i].dst_mask } 		     
	'''	

 	
            #self.speaker.prefix_add(self.ipaddr_to_str(flows[i].srcaddr))
    
    	
    def drop_to_router(self,ip):
	for i in ip:
	    self.speaker.prefix_add(i)    
	    
    def bgp_sender(self):
        def dump_remote_best_path_change(event):
            print 'the best path changed:', event.remote_as, event.prefix, \
                event.nexthop, event.is_withdraw

        def detect_peer_down(remote_ip, remote_as):
            print 'Peer down:', remote_ip, remote_as
        def detect_peer_up(remote_ip,remote_as,uri_enabled,peer):
            print 'Peer up', remote_ip,remote_as
            if uri_enabled:
                self.uri_enabled_capability=True
                self.peer[remote_ip]=(peer,self.uri_enabled_capability)#Create peer dictionary with key ip and value a tuple of peer and uri_enabled capability
                self.uri_enabled_capability = False
            else:
                self.peer[remote_ip]=(peer,False)

        self.speaker = BGPSpeaker(as_number=1000, router_id='147.102.13.198',
                                 best_path_change_handler=dump_remote_best_path_change,
                                 peer_down_handler=detect_peer_down,peer_up_handler=detect_peer_up)
	#self.speaker = BGPSpeaker(as_number=1000, router_id='2.1.1.1',
        #                        best_path_change_handler=dump_remote_best_path_change,
        #                         peer_down_handler=detect_peer_down,peer_up_handler=detect_peer_up)
	
        self.speaker.neighbor_add('147.102.13.156', 1000, next_hop='192.0.2.1')

        #self.speaker.neighbor_add('192.168.1.2', 1001,enable_uri=True)
        #self.speaker.neighbor_add('2.1.1.2', 1000, next_hop='192.0.2.1')
	#alla = PrefixFilter('0.0.0.0/0',policy=PrefixFilter.POLICY_DENY)
	#self.speaker.out_filter_set('192.168.1.2',[alla])
	#self.speaker.out_filter_set('2.1.1.2',[alla])
	#self.drop_to_router(AC(1000).create())
        #self.speaker.
	eventlet.sleep(20)
	self.drop_to_router(['21.0.0.0/8'])
	"""
	ofs=Switch()
        while True:
            eventlet.sleep(20)
            #ofs.add_flow("15.15.15.15")
	    self.drop_to_router(['11.102.0.101/32'])
	    y=IodefJson(2,"sd","a","b",3,2,['11.102.0.101/32'])
	    a=y.toJson()
	    ID=self.db.iodef.insert(a)

            x = bgp.BGPUpdate(withdrawn_routes_len=0, nlri=["mitigation-1.netmode.ntua.gr:8081/report?file="+str(ID)], total_path_attribute_len=0, uri_nlri=True)
            for iter in self.peer:
                print self.peer[iter][1]
                if self.peer[iter][1] == True:  # Check if uri_enabled capability is enabled
                    self.peer[iter][0]._protocol.send(x)  # Send to peer the bgpupdate message

	"""
	
