import json
import sys
from flask import Flask
app = Flask(__name__)
from flask import request
from flask import abort
from DB_store_each_server import Db_store

@app.before_first_request
class API(object):
    def __init__(self):
        self.db = Db_store()
    def seting(self,**kwargs):
        return self.db.set(data=kwargs['data'])

a = API()

@app.route('/set',methods=['POST'])
def set():
    data_load = (json.loads(request.data.decode('utf-8')))
    print(a.seting(data=data_load))
    return "hello"
    pass



if __name__ == "__main__":
    server =sys.argv[1]
    servers_conf=server.split(':')
    app.run(host=servers_conf[0], debug=True, threaded=True, port=3000)
    app.run(host=servers_conf[0], debug=True, threaded=True, port=3001)
    pass