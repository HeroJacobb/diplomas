import logging
import socket
import struct

from ryu.lib import hub
from ryu.base import app_manager
from ryu.controller.handler import set_ev_cls
from ryu.lib.xflow import netflow_collector
from ryu.services.protocols.bgp.bgpspeaker import BGPSpeaker
from collections import defaultdict

LOG = logging.getLogger('ryu.app.netflow_dumper')


def dump_remote_best_path_change(event):
    print 'the best path changed:', event.remote_as, event.prefix, \
        event.nexthop, event.is_withdraw


def detect_peer_down(remote_ip, remote_as):
    print 'Peer down:', remote_ip, remote_as


class NetFlowDumper(app_manager.RyuApp):
    _CONTEXTS = {
        'netflow_collector': netflow_collector.NetFlowCollector
    }

    Flows=defaultdict(list)

    def __init__(self, *args, **kwargs):
        super(NetFlowDumper, self).__init__(*args, **kwargs)
        #self.speaker = BGPSpeaker(as_number=1001, router_id='100.0.0.1',
        #                     best_path_change_handler=dump_remote_best_path_change,
        #                     peer_down_handler=detect_peer_down)
        #self.speaker.neighbor_add('100.0.0.2', 1001, next_hop='192.0.2.1')



    def ipaddr_to_str(self, ip):
        return socket.inet_ntoa(struct.pack('!I', ip))

    @set_ev_cls(netflow_collector.EventNetFlow,
                netflow_collector.NETFLOW_EV_DISPATCHER)
    def dump_flow(self, ev):
        msg = ev.msg
        LOG.info('NetFlow V%d containing %d flows', msg.version,
                 msg.count)

        flows = msg.flows

        for i in range(msg.count):
            LOG.info('Flow%d: %s -> %s ', i,
                     self.ipaddr_to_str(flows[i].srcaddr),
                     self.ipaddr_to_str(flows[i].dstaddr))
            LOG.info('%d packets and %d bytes in the flow',
                     flows[i].dpkts, flows[i].doctets)
            NetFlowDumper.Flows[self.ipaddr_to_str(flows[i].dstaddr)].append(self.ipaddr_to_str(flows[i].srcaddr))
            print NetFlowDumper.Flows
            #LOG.info("AS src: %s AS dst: %s",flows[i].src_as,flows[i].dst_as)
            #self.speaker.prefix_add(self.ipaddr_to_str(flows[i].srcaddr))

