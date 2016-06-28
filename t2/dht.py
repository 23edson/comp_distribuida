from bottle import run, get, put, request
import requests
import json
import sys
from hashf import hashFunction

MOD = 3
NO_ERROR = 200
PROTOCOL = "http://"
myLink = "localhost:" + str(sys.argv[1])
# BUGLIST
# - insercao da mesma chave 2 vezes, possibilita inserir o mesmo par de chave/valer em posicoes diferentes da DHT
# - necessario cria uma maneira para inicializar a DHT, a partir de uma chave inicial
# - necessario implementar comunicacao em grupo, e propagar os inserts e lookups

#def hashFunction(key):
   # out = md5(key.encode('utf-8')).hexdigest()
   # out_1 = '\0'
   # for character in out:
    #    out_1 = str(out_1) + str(ord(character)%MOD)
  #  return out_1

def subkeys(k):
    for i in range(len(k), 0, -1):
        yield k[:i]
    yield ""


class DHT:
    def __init__(self, k):
        self.k = k
        self.h = {}

        for sk in subkeys(self.k):
            self.h[sk] = None

    def insertPropagate(self,k,v,kaux,vaux):
        data = '\0'
        flag = 0
        #if not v.find("localhost:"):
         #   print("ooo")
          #  return None
        #print("ok")
        #string = v[0:]

        url = PROTOCOL + vaux + '/dht/' + k+ '/' + v[0:]
        #print("url " + url)
        try:
            req = requests.put(url)
            if req.status_code == NO_ERROR:
                return vaux
        except requests.exceptions.RequestException as e:
            print(e)
            return None
    
    def insert(self, k, v):
        for sk in subkeys(k):
            if sk in self.h:
                if not self.h[sk]:
                    self.h[sk] = (k, v)
                    #print("aqqqq")
                    return sk
                else:
                    (kaux,vaux) = self.h[sk]
                    #print("problem")
                    if self.insertPropagate(k,v,kaux,vaux):
                        return vaux
                    #return None
                    
        
        
    #def lookup(self, k):
     #   print(list(subkeys(k)))
      #  for sk in subkeys(k):
       #     print(sk)
        #    print(self.h)
         #   if sk in self.h:
          #      if self.h[sk]:
           #         (ki, vi) = self.h[sk]
            #        if ki == k:
             #           return vi
        #return None
    def lookup(self,k):
         keys = []
         #find = 1
         
         #print(list(subkeys(k)))
         for sk in subkeys(k):
             #print(sk)
             #print(self.h)
             if sk in self.h:
                 if self.h[sk]:
                     (ki, vi) = self.h[sk]
                     if ki == k:
                         #keys.append([1,vi,0])
                         return [1,vi,0]
                     else:
                         #keys.append([0,vi,len(sk)])
                         return [0,vi,len(sk)]
                    

    def lookup_dist(self,k):
        find = self.lookup(k)
        a = find[0]
        b = find[1]
        c = find[2]
        #print("enc " + str(a)+" "+ str(b) + " " + str(c))
        #(s,t,v) = find
        if a:
            return [a,b,c,myLink]

        while True:
            try:
                req = requests.get(PROTOCOL + str(b) + '/dht/lookup/' + k)
                who = b
                if req.status_code == NO_ERROR:
                    data = json.loads(req.text)
                    #print(str(data[0])+ " yy")
                    a1 = data[0]
                    b1 = data[1]
                    c1 = data[2]
                    if a1:#se flag for positiva, encontrou o server
                    	return [2,b1,c1,who]
                    elif c1 > c:#se tamanho da chave for maior que a ja tem
                        a = a1
                        b = b1
                    else: #em último caso, retorna falso
                        print("Key not found")
                        return None
            except requests.exceptions.RequestException as e:
                print(e)
                return None

    def __repr__(self):
        return "<<DHT:"+ repr(self.h) +">>"

#dht = DHT("abcd")

@get('/dht/lookup/<key>')
def dht_lookup(key):
    global dht
    #global PROTOCOL
    aux = dht.lookup(key)
    if aux[0]:
    	return json.dumps(myLink)
    	
    return json.dumps("Not Found")

@get('/dht/lookup_dist/<key>')
def dht_lookup_dist(key):
    global dht
    #global PROTOCOL
    aux = []
    aux=dht.lookup_dist(key)
    if aux == None:
    	return json.dumps("Not Found")
    if aux[0]==1:
    	return json.dumps(aux[3])
    	
    return json.dumps(aux[3])

@put('/dht/<key>/<value>')
def dht_insert(key, value):
    global dht
    
    
    return json.dumps(dht.insert(key, value))

valor = hashFunction("http://localhost:"+ str(sys.argv[1]),MOD)
dht = DHT(valor)
#print("DHT : " + valor)
#Inicializa o servidor em uma porta x
run(host='localhost', port=int(sys.argv[1]))
