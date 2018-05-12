import json
import sys
from flask import Flask
app = Flask(__name__)
from flask import request
from flask import abort
import hashlib
import requests
from configobj import ConfigObj


def hash(key, partition_number):
    hash_object = hashlib.sha256(key.encode('utf-8')) # sha256
    hex_value = hash_object.hexdigest()
    part_value = int(hex_value, 32)
    return  part_value % partition_number, part_value%(partition_number-1),hex_value

def put(key,val,server_name):
    payload = {key:val}
    res = requests.post(server_name+'/set', json=payload)
    return 'response from server:{}'.format(res.text)

def geter(key,server_name):
    res= requests.get(server_name+'/get/'+key)
    return 'response from server:{}'.format(res.text)
    #return "hello"

@app.route('/get/<key>',methods=['GET'])
def get(key=None):
    if request.method == 'GET':
        if(key==None) or not(key.isalnum()) :
            return abort(422,"Unprocessable entity alphanumric Key required")
        server_get,server_2_get, Hash_key = (hash(key, len(app.config['server'])))
        server_list = app.config['server'][:]
        server_list.pop(server_get)
        try:
            return_val = geter(Hash_key, app.config['server'][server_get])
            if(return_val=='response from server: No such key on any server '):
                return_val = geter(Hash_key, server_list[server_2_get])
        except:
            return_val=geter(Hash_key,server_list[server_2_get])
        return return_val
    else:
        return abort(403, "method not avilable")


@app.route('/set/<key>', methods=['GET', 'POST'])
def set(key=None):
    if request.method == 'POST':
        if(key==None) or not(key.isalnum()) :
            return abort(422,"Unprocessable entity alphanumric Key required")

        value=(json.loads(request.data.decode('utf-8')))
        if len(value)==0:
            return abort(422, "Unprocessable entity, value required to put ")

        #get the server to put the key and the Hashed key
        server_put,server_2_put,Hash_key = (hash(key, len(app.config['server'])))
        server_list=app.config['server'][:]
        server_list.pop(server_put)
        try:
            return_val = put(Hash_key, {key: value}, app.config['server'][server_put])
            store_repica= put(Hash_key,{key:value},server_list[server_2_put])
        except:
            return_val = put(Hash_key, {key: value}, server_list[server_2_put])
        print("************************")
        print(server_list)
        print("*************************")
        return return_val
    else:
        return  abort(403,"method not avilable")


@app.route('/')
def home():
   return 'servers are {!r} '.format(app.config.get('server'))



if __name__ == "__main__":
    print("Number of SERVERS: ", len(sys.argv[1:]))
    servers = []
    config = ConfigObj('config.ini')
    
    for i in range (1,len(sys.argv)):
        servers.append("http://"+ sys.argv[i])
        hash(sys.argv[i],len(sys.argv))
    app.config['server'] = servers
    app.run(host='0.0.0.0',debug=True,threaded=True,port=8081)

