#http://www.lurklurk.org/pynamo/pynamo.html

class VectorClock(object):
    def __init__(self):
        self.clock = {}  # node => counter
        
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