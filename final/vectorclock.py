#http://www.lurklurk.org/pynamo/pynamo.html

class VectorClock(object):
    def __init__(self):
        self.clock = {}  # node => counter
        
    def getVector(self):
    	mi = '/0'
    	m = []
    	mout = []
    	mi = str(["%s:%d" % (node, self.clock[node]) for node in sorted(self.clock.keys())])
    	mi = mi + ';'
    	tam1 = len(mi)
    	m = mi.split(',')
    	#print(m)
    	#mi = aux.split(
    	i = 0
    	total = 0
    	for node in m:
    		aux = str(node)
    		#print(aux)
    		idx = aux.find(':')
    		tam = len(aux)
    		if i == 0:
    			ia = aux[2:idx]
    			ib = aux[idx+1:tam-1]
    			#ib = int(ib)
    			mout.append([ia,ib])
    			i = i+ 1
    			#total = total + tam
    		elif ';' in aux:
    			ia = aux[2:idx]
    			ib = aux[idx+1:tam-3]
    			mout.append([ia,ib])
    		else:
    			ia = aux[2:idx]
    			ib = aux[idx+1:tam-1]
    			mout.append([ia,ib])
    		
    	#print(mout)
    	return mout
    	
    def listToObj(self,m):
    	for(i,j)in m:
    		self.clock[i] = j
    		
    def getCounter(self,node):
    	if node in self.clock:
    		return self.clock[node]

    def update(self, node, counter):
        """Adicionar novo: Contador do relogio vetor."""
        if node in self.clock and counter <= self.clock[node]:
            raise Exception("Nodo %s possui clock :%d maior que %d" %
                            (node, self.clock[node], counter))
        self.clock[node] = counter
        #return self  # allow chaining of .update() operations

    def __str__(self):
        return "{%s}" % ", ".join(["%s:%d" % (node, self.clock[node])
                                   for node in sorted(self.clock.keys())])
                                   