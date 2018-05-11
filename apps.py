import json
import sys
from flask import Flask
from flask import request
from DB_store_each_server import Db_store

app = Flask(__name__)

@app.before_first_request
class API(object):
    def __init__(self):
        self.db = Db_store()

    def setter(self,**kwargs):
        return self.db.set(data=kwargs['data'])

    def getter(self,**kwargs):
        return self.db.get(data=kwargs['data'])

a = API()

@app.route('/set',methods=['POST'])
def set():
    data_load = (json.loads(request.data.decode('utf-8')))
    return json.dumps(a.setter(data=data_load))



@app.route('/get/<key>',methods=['GET'])
def get(key=None):
    print(a.getter(data=key.strip()))
    return json.dumps(a.getter(data=key.strip()))



if __name__ == "__main__":
    server =sys.argv[1]
    servers_conf=(server.split(':')[1])
    app.run(host='0.0.0.0', debug=True, threaded=True, port=int(servers_conf))
    pass