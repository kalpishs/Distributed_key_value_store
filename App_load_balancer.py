import json
import sys
from flask import Flask
app = Flask(__name__)
from flask import request
from flask import abort
import hashlib

import requests

def hash(key, partition_number):

    hash_object = hashlib.sha256(key.encode('utf-8')) # sha256
    hex_value = hash_object.hexdigest()
    part_value = int(hex_value, 32)
    return  part_value % partition_number,hex_value

def put(key,val,server_name):
    payload = {key:val}
    res = requests.post(server_name+'/set', json=payload)
    return 'response from server:{}'.format(res.text)
    pass

@app.route('/set/<key>', methods=['GET', 'POST'])
def set(key=None):
    if request.method == 'POST':
        if(key==None) or not(key.isalnum()) :
            return abort(422,"Unprocessable entity alphanumric Key required")

        value=(json.loads(request.data.decode('utf-8')))
        if len(value)==0:
            return abort(422, "Unprocessable entity, value required to put ")

        #get the server to put the key and the Hashed key
        server_put,Hash_key = (hash(key, len(app.config['server'])))

        for ky,val in value.items():
            return_val= put(Hash_key,{key:val},app.config['server'][server_put])
            break
        pass
    else:
        return  abort(403,"method not avilable")
        pass
    return return_val



@app.route('/')
def home():
   return 'servers are {!r} '.format(app.config.get('server'))



if __name__ == "__main__":

    print("Number of SERVERS: ", len(sys.argv[1:]))
    servers = []
    for i in range (1,len(sys.argv)):
        servers.append("http://"+ sys.argv[i])
    app.config['server'] = servers

    app.run(host='0.0.0.0',debug=True,threaded=True,port=8081)

