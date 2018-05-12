import  random
import string
import argparse
import threading
import subprocess
import time
import requests

lb_host='localhost'
lb_port='8081'
list_options=['GET','SET']


def output_reader(proc):
    for line in iter(proc.stdout.readline, b''):
        print('got line: {0}'.format(line.decode('utf-8')), end='')

def generate_random_keys_val():
    alphabet = string.ascii_lowercase
    keys = []
    values = []
    num_key=random.randint(0,50)
    for i in range(num_key):
        key = ''
        val = ''
        for i in range(10):
            key += alphabet[random.randint(0, len(alphabet) - 1)]
        for i in range(20):
            val += alphabet[random.randint(0, len(alphabet) - 1)]
        keys.append(key)
        values.append(val)
    return keys,values
    pass

def start_n_servers(server):

    cmd="python apps.py {}".format(server)
    print(cmd)
    proc = subprocess.Popen(['python', 'apps.py', server],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    t = threading.Thread(target=output_reader, args=(proc,))
    t.start() #runs infinite
    return

def start_load_balancer(listserver):

    proc = subprocess.Popen(['python', 'App_load_balancer.py']+listserver,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    t = threading.Thread(target=output_reader, args=(proc,))
    t.start() #runs infinite
    return
    pass


def put_key_val(key,value):

    cmd_str = "http://"+lb_host + ":" + lb_port+'/set/'+key
    payload = value
    time.sleep(0.5)
    res = requests.post(cmd_str, json=payload)
    time.sleep(0.5)
    pass


def get_key_val(key):
    cmd_str = "http://"+lb_host + ":" + lb_port
    time.sleep(0.5)
    res = requests.get('{0}/get/{1}'.format(cmd_str,key))
    time.sleep(0.5)
    print(res.text)
    return res

def Random_test(num_request,keys,vals):
    print(" Testsing the basic SET / GET requests in all the avilable nodes ")
    time.sleep(0.5)
    for i in range(0,num_request):
        choice=random.choice(list_options)
        if choice=='GET':
            get_key_val(random.choice(keys))
        if choice=='SET':
            put_key_val(random.choice(keys),random.choice(vals))
        time.sleep(0.5)
        pass

def Serial_Test(num_reqest,keys,vals):
    time.sleep(0.5)
    chosen_k_V={}
    for i in range(0,int(num_request/2)):
        key_chosen=random.choice(keys)
        vals_chosen=random.choice(vals)
        chosen_k_V[key_chosen]=vals_chosen
        put_key_val(key_chosen,vals_chosen)
    for k,v in chosen_k_V.items():
        get_key_val(k)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.', prog='myprogram')
    parser.add_argument('-n','--nodes', help='number of nodes for KV store',required=True,type=int)
    parser.add_argument('-p','--port',help='starting port address for nodes',required=True,type=int)
    parser.add_argument('-r','--request',help='number of put and get request',default=10,type=int)
    parser.add_argument('-ht','--host',help='host name',default='localhost')
    parser.add_argument('-c','--choice',help='choice of Random put/get',default='order')
    args = parser.parse_args()
    nodes=args.nodes
    start_port=args.port
    num_request=args.request
    host=args.host
    list_servers=[]
    keys, vals = generate_random_keys_val()
    for i in range(0,nodes):
        server=host+":"+str(start_port)
        time.sleep(0.5)
        start_n_servers(server)
        time.sleep(0.5)
        list_servers.append(server)
        start_port+=1
    time.sleep(0.5)
    start_load_balancer(list_servers)
    time.sleep(0.5)
    selected_test=args.choice
    if selected_test=='Random':
        Random_test(num_request,keys,vals)
    else:
        Serial_Test(num_request,keys,vals)

