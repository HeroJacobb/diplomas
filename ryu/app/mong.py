from bson import ObjectId
from pymongo import MongoClient
from time import gmtime, strftime

class IodefJson():
    ID=0
    def __init__(self,alternative_id,related_activity,description,method,datetime,additional_data,ip_sources):
        IodefJson.ID=IodefJson.ID+1
        self.id=IodefJson.ID
        self.aid=alternative_id
        self.related_activity=related_activity
	self.report_time=strftime("%Y-%m-%d %H:%M:%S", gmtime())
	self.description=description
	self.method=method
        self.datetime=datetime
        self.additional_data=additional_data
        self.ip_sources=ip_sources
    def toJson(self):
        iodefjson={
            'ID' : self.id,
            'AlternativeID': self.aid,
            'RelatedActivity':self.related_activity,
	    'ReportTime':self.report_time,
	    'Description':self.description,
	    'Method':self.method,
            'History':[{'DateTime':self.datetime,
                        'AdditionalData':self.additional_data}],
            'EventData':self.ip_sources


        }
        return iodefjson


#x=IodefJson(2,"sd",3,2,['192.168.1.1'])
#print x
#x.toJson()
#client=MongoClient()
#db=client.mydb
#aa=db.iodef.insert(x.toJson())
#print aa
#bb=db.iodef.find_one({"_id": ObjectId("5729b5d88674602b373f971b")},{"_id": 0,"ID": 0})#the second field is for the attributes we dont want to get
#print bb
#if bb==None:
#    print 'eleos'
#curl=curl.Curl('0.0.0.0:5000/?file='+str(aa))
#print "gamw"
#curl.get_page()
#db.iodef.insert


#print x.toJson()
