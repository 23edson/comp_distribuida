from bottle import run,get,put,request
import requests
import json
import sys
import hashlib
import os

CONST = 30


class MERKLE:
	def __init__(self,k):
		self.tam = CONST
		self.root  = k
		self.tree = {}
		self.hashf = {}
		self.hashinit = ''
		self.__MERKLETREE__()
	
	
	def MERKLETREE(self):
		for valor, hash in self.tree.iteritems():
			items = self.getFromDir(valor)
			val = []
			val.append(valor)
			list = {}
			for i in items:
				if valor == self.root:
					list[self.hashf[i]] = i
				else:
					list[self.hashf[os.path.join(valor,i)]] = os.path.join(valor,i)
			val.append(list)
			self.tree[hash] = val
		self.hashinit = self.hashf[self.root]
	
	def __MERKLETREE__(self):
		self.tree(self.root)
		self.MERKLETREE()
	
	def getTree(self):
		return self
	
	def getMD5(self, valor):
		hasht = md5()
		arq = os.path.join(self.root,valor)
		if os.path.isfile(arq):
			arq1 = file(arq, 'rb')
			while 1:
				dado = arq1.read(8000)
				if not dado:
					break
				hasht.update(dado)
			arq1.close()
		else:
			hasht.update(valor)
		return hasht.hexdigest()
		
	def getFromDir(self, dirname):
		list_1 = []
		if dirname != self.root:
			dirname = os.path.join(self.root,dirname)
		if os.path.isdir(dirname):
			valor = os.listdir(dirname)
			for i in valor:
				list_1.append(i)
			list_1.sort()
		return list_1
		
		
	def hashf(self, root):
		self.Child(root)
		valor = self.getFromDir(root)
		if not valor:
			self.hashf[root] = ''
			return
		str1 = ''
		for i in valor:
			str1 = str1 + self.hashf[i]
		self.hashf[root] = self.getMD5(str1)
		
	def Child(self, root):
		valor = getFromDir(root)
		if not valor:
			self.hashf[root] = ''
			return
		for i in valor:
			nome = os.path.join(root,i)
			if os.path.isdir(nome):
				self.Child(i)
				sub = self.getFromDir(i)
				string = ''
				for subi in sub:
					string = string+self.hashf[os.path.join(i,subi)]
				if root == self.root:
					self.hashf[i]=self.getMD5(string)
				else:
					self.hashf[nome] = self.getMD5(string)
			else:
				if root == self.root:
					self.hashf[i] = self.getMD5(i)
				else:
					self.hashf[nome] = self.getMD5(nome)
					
	#def compare(tree1,head1,tree2,head2):
	#	if head1 == head2:
	#		print("Os hash de ambas as arvores sao o mesmo")
	#	else:
	#		valor1 = tree1.tree[head1]
	#		child1 = valor1[1]
	#		valor2 = tree2.tree[head2]
	#		child2 = valor2[1]

		
	#	for i,j in child1.iteritems():
		
@get('/merkle')
def getTree():
	global mt_1
	return json.dumps(mt_1.getTree())			

mt_1 = MERKLE('dir');
#mt_2 = MERKLE('dir1');
#mt_3 = MERKLE('dir2');

run(host='localhost',port=int(sys.argv[1]))