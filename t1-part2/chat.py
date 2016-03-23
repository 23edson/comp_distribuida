#Computação Distribuída
#Edson Lemes da Silva

from bottle import run, get, post, view, request, redirect, response, route
import json
from threading import Thread
from threading import Lock
import requests
import sys
import time


messages = [("Nobody", "Hello!")]
messages_1 = []
servers_list = []
aux = []
mylink = None
name = "Nobody"
NO_ERROR = 200
#msgsCounter = 1

@get('/')
@view('index')
def index():
    return {'messages': messages, 'name': name }

@route('/<name>')
@view('index')
def index(name):
    return {'messages': messages, 'name': name}

@post('/send')
def sendMessage():
    name=""
    m = request.forms.get('message')
    n = request.forms.get('name')
    
    messages.append([n, m])
    messages_1.append([n,m])
    
    redirect('/'+n)

@get('/peers')
def peersMethod():
    data = json.dumps(servers_list)
    return data

@get('/msgs')
def peersMethod():
    data = json.dumps(messages_1)
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
       time.sleep(2) 

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
        time.sleep(2)

    return None


def checkList(messages, msg, host):
    url = str(host)
    qtd = None
    i = 0
    for x, y in aux:
        #print(str(x)+"\n" + str(y))
        if x == url:
            qtd = y
            break
        
    if qtd!=None and qtd < len(msg):
        for msg_1 in msg:
            if i < qtd:
                i=i+1
            else:
                messages.append(msg_1)
        for idx, row in enumerate(aux):
            hostName, count = row
            if hostName == url:
                aux[idx] = (url, qtd+1)
                break
    
    
    
#Thread para controle da lista de servidores            
def serversControl(thread_name,mutex):
    print(thread_name + " iniciada")
    while 1:
        #print("")
        mutex.acquire(1)
        time.sleep(1)
        global servers_list
        for links in servers_list:
            if links != myLink: 
                new_peer = getPeers(links)
                if new_peer != None:
                    #print(servers_list)
                    for test in new_peer:
                        if not test in servers_list:
                            servers_list.append(test)
                            msg = (test, 0)
                            aux.append(msg)
        mutex.release()
        #  time.sleep(1)

#Thread para controle da lista de mensagens
def messagesControl(thread_name,mutex):
    print(thread_name + " iniciada")
    while 1:
        #print("")
        mutex.acquire(1)
        time.sleep(1)
        global messages
        for links in servers_list:
            if links != myLink:
                msg = getMessages(links)
                if msg != None:
                    #print("entrei")
                    checkList(messages, msg, links)
        mutex.release()


myLink = "http://localhost:" + str(sys.argv[1])
servers_list.append(myLink)
for i in sys.argv:
    if i != 'chat.py' and i != sys.argv[1]:
        servers_list.append("http://localhost:" +str(i))
        msg = ("http://localhost:"+str(i),0)
        aux.append(msg)
print("lista de conhecidos inicializada\n")


    
mutex = Lock()
thread1 = Thread(target = serversControl, args = ("Thread 1",mutex)).start()
thread2 = Thread(target = messagesControl, args = ("Thread 2",mutex)).start()

run(host='localhost', port = int(sys.argv[1]))
