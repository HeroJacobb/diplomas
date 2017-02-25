import gevent
import eventlet
import socket
from ryu.base import app_manager
from ryu.controller import event
from ryu.lib.xflow import netflow
from ryu.lib import hub
from pymongo import MongoClient


NETFLOW_EV_DISPATCHER='netflow'
BUFSIZE = 65535  


class EventNetFlow(event.EventBase):
    def __init__(self, msg, addrport):
        super(EventNetFlow, self).__init__()
        self.msg = msg
        self.addr, self.port = addrport


class NetFlowCollector(app_manager.RyuApp):
    def __init__(self):
        super(NetFlowCollector, self).__init__()
        self.name = 'netflow_collector'
	self.client=MongoClient()
        self.db=self.client.connections
        self._start_recv()

    def start(self):
        return self.thread

    def _recv_loop(self):
        while True:
            self.sock.setblocking(True)
            (data, addrport) = self.sock.recvfrom(BUFSIZE)
            msg = netflow.NetFlow.parser(data)
            if msg:
	        res=self.db.stat.find_one({
                'srcaddr'   : self.ipaddr_to_str(flows[i].srcaddr)      ,
                'dstaddr'   : self.ipaddr_to_str(flows[i].dstaddr)      })
		if res==None:
		     	self.db.stat.insert({
                	'srcaddr'   : self.ipaddr_to_str(flows[i].srcaddr),
               	        'dstaddr'   : self.ipaddr_to_str(flows[i].dstaddr)})
            #self.send_event_to_observers(EventNetFlow(msg, addrport))

    def _start_recv(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0',
                        9996))
        self.thread=hub.spawn_after(1,self._recv_loop)
