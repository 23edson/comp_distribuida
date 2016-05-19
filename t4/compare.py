from bottle import run,get,put,request
import requests
import json
import sys
import hashlib
import os
import merkle

#ports = ['8080','8081']


link = "http://localhost:"

	dado = requests.get(link+'8080'+'/merkle')
	mt1 = json.loads(dado.text)
	dado = requests.get(link+'8081'+'/merkle')
	mt2 = json.loads(dado.text)
