import requests
import json

class Switch():
    def __init__(self,dpid=3149609468469440):
        self.dpid=dpid
        self.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    def add_flow(self,nw_src="",nw_dst="0.0.0.0/0",udp=None,port="[]"):
        if port=="[]" and nw_dst=="0.0.0.0/0" and udp==None:
	    values = {"dpid": self.dpid, "match": {"nw_src": nw_src,"dl_type": 2048 }, "actions": []}
	elif port=="[]":
	    values = {"dpid": self.dpid, "match": {"nw_src": nw_src,"nw_dst":nw_dst,"tp_src":udp,"nw_proto":17,"dl_type": 2048 }, "actions": []}
	
	else :
	    print port
	    print nw_src
            values = {"dpid": self.dpid,"match":{"nw_src":nw_src,"dl_type": 2048},"actions" : [ { "type" : "OUTPUT" ,"port": port}]}
	data=json.dumps(values)
        requests.post('http://localhost:8080/stats/flowentry/add',data,headers=self.headers)

    def del_flows(self):
	self.values={"dpid": self.dpid, "match": {}}
	self.data=json.dumps(self.values)	
        requests.post('http://localhost:8080/stats/flowentry/delete',self.data,headers=self.headers)



