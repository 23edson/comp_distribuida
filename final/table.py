#Computação Distribuída
#Edson Lemes da Silva
#Esta aplicação representa uma tabela de dados distribuída, assim, é possível enviar e receber dados na tabela
#através de peers cuja url é conhecida

from bottle import run, get, post, view, request, redirect, response, route,put
import json
from threading import Thread
from threading import Lock
import requests
import sys
import time
from vectorclock import VectorClock


messages = []
servers_list = []
know_servers = []

layoutx = []
layouty = []
x = 0
y = 0

mylink = None

NO_ERROR = 200

Vector = VectorClock()

@get('/')
@view('index')
def index():
    return {'messages': messages, 'layoutx' : layoutx, 'layouty' : layouty, 'users' : servers_list}

#@route('/<on>')
#@view('index')
#def index(name):
#    return {'messages': messages, 'layoutx' : layoutx, 'layouty' : layouty,'users' : servers_list}
#Recebe a mansagem e sincroniza com a lista, atualizando também o vectorClock respectivo a cada posição da
#tabela
@post('/send')
def sendMessage():
	global x
	global y
	m = []
	for i in range(1,(x*y)+1):
		m.append(request.forms.get('message' + str(i)))
		
	
	
	for (indexx,i) in enumerate(m):
		for (index,j) in enumerate(messages):
			if indexx == index:
				
				j[0] = i
				aux = Vector.getCounter(str(index))
				aux = aux + 1
				Vector.update(str(index), aux)
			
				
				break
				
	
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

@put('/peers/<name>')
def peersSyncMethod(name):
	return putPeers(name)
	
def getPeers(who):
    url = str(who[0]) + "/peers"
    

    try:
 
        req = requests.get(url)
        if req.status_code == NO_ERROR:
            data = json.loads(req.text)
            return data
    except:
       time.sleep(1) 

    return None

        
def getMessages(who):
    url = str(who[0]) + "/msgs"
    
    try:

        req = requests.get(url)
        if req.status_code == NO_ERROR:
            data = json.loads(req.text)
            
            return data
    except:
        time.sleep(1)

    return None
    
def putPeers(name):
	global servers_list
	host = "http://localhost:"
	host = host+str(name)
	
	flag = 1
	
	time.sleep(2)
	#mutex.acquire(1)
	for i in servers_list:
		if i[0] == host:
			flag = 0
			break
	if flag == 1:
		servers_list.append([host,1])
	#print(servers_list)
	#mutex.release(1)
	if flag:
		return 1
	return 0

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

#Quando recebe a lista de mensagens de algum servidor, verifica no vectorCLock do servidor recebido se
#há modificações mais recentes que a armazenada no vectorCLock local 
def checkList(msg, host):
	temp = VectorClock()
	data = getClock(host)
	for  (i,j) in data:
		temp.update(i,j)
	
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
				
    			

def peersSynct(thread_name,mutex):
	print(thread_name + " iniciada")
	while 1:
		time.sleep(1)
		mutex.acquire(1)
		global servers_list
		for i in servers_list:
			if i[0] != myLink:
				try:
					req = requests.put(i[0] + "/peers/"+myLink[17:])
				except:
					continue
		mutex.release()
#Thread para controle da lista de servidores            
def serversControl(thread_name,mutex):
    print(thread_name + " iniciada")
    while 1:
    	time.sleep(1.5)
    	mutex.acquire(1)
    	global servers_list
    	flag = 1
    	flag1 = 1
    	for links in servers_list:
    		
    		if links[0]!=myLink:
    	
    			new_peer=getPeers(links)
    			
    			if new_peer!=None:
    				
    				links[1] = 1
    				for test in new_peer:
    					
    					for aux in servers_list:
    						if test[0] == aux[0]:
    							flag = 0
    						
    					if flag == 1:
    						
    						servers_list.append(test)
    					else:
    						flag = 1
    			else:
    				
    				links[1] = 0
    			
    				
    	mutex.release()
        #  time.sleep(1)

#Thread para controle da lista de mensagens
def messagesControl(thread_name,mutex):
    print(thread_name + " iniciada")
    while 1:
        
        mutex.acquire(1)
        time.sleep(1.3)
        global messages
        for link in servers_list:
            if link[0] != myLink:
                msg = getMessages(link)
                if msg != None:
                	checkList(msg, link[0])
        mutex.release()


#A tabela é definida na lista messages seguindo o seguinte formato:
#se há uma tabela 2x2, então a lista ficará [("","1,1;"),("","1,2;"),("","2,1;"),("","2,2;")].
#Deste modo, cada cédula da tabela é identificada pelo segunda dado das tuplas na lista.        
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
				
				
				
	#print(messages)        

x = int(sys.argv[3])
y = int(sys.argv[2])
getTableSize(x,y)

myLink = "http://localhost:" + str(sys.argv[1])
servers_list.append([myLink,2])


for i in sys.argv:
    if i != 'table.py' and i != sys.argv[1] and i!=sys.argv[2] and i!=sys.argv[3]:
        servers_list.append(["http://localhost:" +str(i),0])
       
print("lista de conhecidos inicializada\n")

mutex = Lock()
thread1 = Thread(target = serversControl, args = ("Thread 1",mutex)).start()
thread2 = Thread(target = messagesControl, args = ("Thread 2",mutex)).start()
thread2 = Thread(target = peersSynct, args = ("Thread 3",mutex)).start()

run(host='localhost', port = int(sys.argv[1]))
