
=======Distributed Kev-Value Store=======

``Name: Kalpish Singhal``


----------------------------------------
Design
----------------------------------------
*******Roles:*******

1. **Client** - It is endpoint interaction for the user to get or put the key:values in distribured key value store.

2. **Load Balancer** - It listens to all the request of the client, redirect request to the server and responsds to client requests as well.

3. **Backend Servers** - They store data(in format {< hashvalue >:< key:value >}) as drived by load balancer, and also responses to load balancer's queries.

There is a centralised server acting as load balancer. It takes the requests of PUT and GET i.e setting and getting the value from the client. 

POST Request: It hashes the value, for each hash it finds a particular server from the server list passed in the arguments maintained with load balancer. It also finds the secondary server to maintain two factor replication. Then it sends the data to the respective servers to store them. Servers acknowledges when the key:value pair is stored

GET Request: It finds the corret hash and tries to fetch the value from the server. If first server is not available, it fetches the value from the secondary server. It always returns the last updated value for each key.


*****Handling Failures*****
1. Load Balancer - There is no data with load balancer. It just redirects the key:value pairs to be stored on different servers. It can just be restarted in cases of failures.
2. Server Nodes - Architecture is following two factor replication i.e. Each key:value pair is stored on two different servers, so if a server fails, still the value can be retreived from another server.

----------------------------------------
How to run
----------------------------------------
1. Run apps.py to run the servers. For each node execute e.g python apps.py <host:port>
2. Run load balancer providing arguments for each node host and port e.g python App_load_balancer.py <host1:post1> <host2:post2> ....
3. Now put your key:values as request in following format:

    a) PUT: curl -H "Content-type: application/json" -XPOST http://localhost:8081/set/hello -d '"world"'
    
    b) GET: curl -H "Content-type: application/json" http://localhost:8081/get/hello
    
4. Default port for load balance is 8081.


----------------------------------------
Testing
----------------------------------------
1. Run test.py. It has following arguments with arg parser lib for help.
   
   e.g. --node is for number of servers to be run, and --port tells from where to start the series of server.
        
            --nodes 4 --port 3000
            
2. As of now, random & serial testing is being done. It generates random key:value pairs and in random fashion gets and puts on the server.

----------------------------------------
Dependencies
----------------------------------------
This project will require following to execute:
    
    1. Flask
    
    2. requests
    
    3. Python3
    
    
    
------------------------------------------
Future Scope
------------------------------------------
1. We can have a persistent storage to restart server with previous stored values.

2. Add new servers at runtime and do required rehashing.

3. Delete servers forever at runtime and do required rehashing.

4. Delete the key in distributed KV store.

