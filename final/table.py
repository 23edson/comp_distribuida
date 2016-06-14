#Computação Distribuída
#Edson Lemes da Silva

from bottle import run, get, post, view, request, redirect, response, route
import json
from threading import Thread
from threading import Lock
import requests
import sys
import time
from vectorclock import VectorClock


messages = []
servers_list = []
layoutx = []
layouty = []
x = 0
y = 0
#eventCount = 1
#messages_1 = []

#aux = []
mylink = None

NO_ERROR = 200

Vector = VectorClock()
#msgsCounter = 1

@get('/')
@view('index')
def index():
    return {'messages': messages, 'layoutx' : layoutx, 'layouty' : layouty }

@route('/<name>')
@view('index')
def index(name):
    return {'messages': messages, 'layoutx' : layoutx, 'layouty' : layouty}

@post('/send')
def sendMessage():
	global x
	global y
    #name=""
	m = []
	for i in range(1,(x*y)+1):
		m.append(request.forms.get('message' + str(i)))
		
	#print(m)
	
	for (indexx,i) in enumerate(m):
		for (index,j) in enumerate(messages):
			if indexx == index:
				#print(str(indexx) +" " + str(index))
				j[0] = i
				aux = Vector.getCounter(str(index))
				aux = aux + 1
				Vector.update(str(index), aux)
			
				#print(j)
				break
				
	#print(messages)
   # messages.append([n, m])
    #messages_1.append([n,m])
	redirect('/')

@get('/peers')
def peersMethod():

    data = json.dumps(servers_list)
    return data

@get('/msgs')
def peersMethod():
    data = json.dumps(messages)
    return data

@get('/clock')
def clockMethod():
	m =Vector.getVector()
	data = json.dumps(m)
	return data

def getPeers(who):
    url = str(who) + "/peers"
    #print("teste"+url+"\n")

    try:
        req = requests.get(url)
        if req.status_code == NO_ERROR:
            data = json.loads(req.text)
            
            return data
    except:
       time.sleep(1) 

    return None

        
def getMessages(who):
    url = str(who) + "/msgs"
    #print(" " + url + "\n")
    try:

        req = requests.get(url)
        if req.status_code == NO_ERROR:
            data = json.loads(req.text)
            
            return data
    except:
        time.sleep(1)

    return None

def getClock(who):
	url = str(who) + "/clock"
	try:
		req = requests.get(url)
		if req.status_code == NO_ERROR:
			data = json.loads(req.text)
			return data
	except:
		time.sleep(1)
	return None


def checkList(msg, host):
	temp = VectorClock()
	data = getClock(host)
	temp.listToObj(data)
	#print(msg)
	#return 0
	for (index,msgi) in enumerate(msg):
		aux = Vector.getCounter(str(index))
		
		try:
			aux_1 = temp.getCounter(str(index))
			Vector.update(str(index),int(aux_1))
		except:
			continue
			
			
		for (i,mes) in enumerate(messages):
			if i == index:
				mes[0] = msgi[0]
				#print(str(i) + " " + str(mes[0]))
    			
    	
    			
    		
    	
    
    
    
#Thread para controle da lista de servidores            
def serversControl(thread_name,mutex):
    print(thread_name + " iniciada")
    while 1:
    	
        #print("")
        time.sleep(1)
        mutex.acquire(1)
        
        global servers_list
        for links in servers_list:
            if links != myLink: 
                new_peer = getPeers(links)
                if new_peer != None:
                    #print(servers_list)
                    for test in new_peer:
                        if not test in servers_list:
                            servers_list.append(test)
                            #msg = (test, 0)
                            #aux.append(msg)
        mutex.release()
        #  time.sleep(1)

#Thread para controle da lista de mensagens
def messagesControl(thread_name,mutex):
    print(thread_name + " iniciada")
    while 1:
        #print("f")
        mutex.acquire(1)
        time.sleep(0.8)
        global messages
        for link in servers_list:
            if link != myLink:
                msg = getMessages(link)
                if msg != None:
                    #print("entrei")
                    #print(msg)
                    checkList(msg, link)
        mutex.release()
        
def getTableSize(x,y):
	layoutx.append("")
	count = 0
	for i in range(1,x+1):
			layoutx.append(i)
			
	for i in range(1,y+1):
		layouty.append(i)
		
	for i in range(1,y+1):
		for j in range(1,x+1):
			Vector.update(str(count), 0)
			count = count+1
			if j == x:
				messages.append(["", str(i)+","+str(j)+";"])
				
			else:
				messages.append(["",str(i)+","+str(j)])
				
				
				
	print(messages)        

x = int(sys.argv[2])
y = int(sys.argv[3])
getTableSize(x,y)
#print(layoutx)
#print(layouty)
#print(messages)
myLink = "http://localhost:" + str(sys.argv[1])
servers_list.append([myLink,2])

for i in sys.argv:
    if i != 'table.py' and i != sys.argv[1] and i!=sys.argv[2] and i!=sys.argv[3]:
        servers_list.append(["http://localhost:" +str(i)],0)
        #msg = ("http://localhost:"+str(i),0)
        #aux.append(msg)
print("lista de conhecidos inicializada\n")



    
mutex = Lock()
thread1 = Thread(target = serversControl, args = ("Thread 1",mutex)).start()
thread2 = Thread(target = messagesControl, args = ("Thread 2",mutex)).start()

run(host='localhost', port = int(sys.argv[1]))
