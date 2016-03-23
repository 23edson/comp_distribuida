#Computação Distribuída
#Edson Lemes da Silva

from bottle import run, get, post, view, request, redirect, response

messages = [("Nobody", "Hello!")]

@get('/')
@view('index')
def index():
    return {'name': 'Nobody', 'messages': messages }

@get('/<name>')
@view('index')
def index(name):
    return {'name': name, 'messages': messages}

@post('/send')
def sendMessage():
    m = request.forms.get('message')
    n = request.forms.get('name')
    
    messages.append([n, m])
    redirect('/'+n)


run(host='localhost', port=8080)
