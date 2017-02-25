import socket
from ryu.base import app_manager
from ryu.controller import event
from ryu.lib import hub

SDNI_EV_DISPATCHER='sdni'
BUFSIZE = 65535

class EventSdni(event.EventBase):
    def __init__(self, msg):
        super(EventSdni, self).__init__()
        self.msg = msg
class SdniCollector(app_manager.RyuApp):
    def __init__(self):
        super(SdniCollector, self).__init__()
        self.name = 'sdni_collector'
        self._start_recv()

    def start(self):
        return self.thread

    def _recv_loop(self):
        self.sock.listen(5)
        while True:
            self.sock.setblocking(True)
            (clientsocket, address) = self.sock.accept()
            data=clientsocket.recv(1024)
            #print data
            self.send_event_to_observers(EventSdni(data))

    def _start_recv(self):
        self.sock =socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.bind(('0.0.0.0',
                        9000))
        self.thread = hub.spawn_after(1, self._recv_loop)
