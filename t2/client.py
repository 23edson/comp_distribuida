import requests
import json
import sys
from hashf import hashFunction
NO_ERROR = 200
MOD = 3
url = "localhost:"
protocol = "http://"
hosts = []


port = int(sys.argv[1])

myLink = protocol+url+str(port)

for i in sys.argv:
    if i != 'client.py' and i != sys.argv[1]:
        
        hosts.append(url+str(i))

for i in hosts:
    print("key " + hashFunction(protocol+i,MOD) + " chave " + protocol+i)

for i in hosts:
    #print(hosts[1])
    req = requests.put(myLink+ '/dht/' + hashFunction(protocol+i,MOD) + "/" + i)
    if not req.status_code == NO_ERROR:
        print("PUT request problem")

for i in hosts:
    req = requests.get(myLink + '/dht/lookup/' + hashFunction(protocol + i,MOD))
    if not req.status_code == NO_ERROR:
        print("GET request problem")
    else:
        data = json.loads(req.text)
        print(data)

for i in hosts:
    req = requests.get(myLink + '/dht/lookup_dist/' + hashFunction(protocol+i,MOD))
    if req.status_code == NO_ERROR:
        data = json.loads(req.text)
        print(data)
    else:
        print("GET-2 request problem")
            
