from flask import Flask
from flask import request,Response,abort,jsonify
from pymongo import MongoClient
from bson import ObjectId
from bson import json_util


#POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, db=0)
#my_server = redis.Redis(connection_pool=POOL)
#context = SSL.Context(SSL.SSLv23_METHOD)

application = Flask(__name__)

client = MongoClient('localhost:27017')
db=client.connections

@application.route('/report',methods=['GET','POST'])
def hello_world():
    try:
       fl=request.args.get('file')
    except(ValueError):
       return abort(400)
    res=db.iodef.find_one({"_id": ObjectId(fl)},{"_id": 0,"ID": 0})
    if (res!=None):
            return json_util.dumps(res)
    return abort(400)

if __name__ == '__main__':
    application.run(host='192.168.1.1',threaded=True)#,ssl_context=context)
