from flask import *
from flask_socketio import SocketIO, emit, disconnect
import hashlib
import sqlite3 

from modules.authentication.auth import *
from modules.socketIO.socketIO_app import *

app = Flask(__name__)

async_mode = None
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)

## APP ROUTES--------------------------------
@app.route('/',methods=['GET']) 
def _root_event_():
	return authenticate_user(request)

@app.route('/register_user',methods=['GET','POST'])
def _register_event_():
	return register_user(request)

@app.route('/home_page',methods=['GET', 'POST'])
def _home_event_():
	return home_page(request)

@app.route('/verify_user',methods=['POST'])
def _verify_event_():
	return verify_user(request)

## SOCKETS--------------------------------
@socket_.on('make_connection',namespace="/chat")
def _sock_connect_(message):
	return connect(session,request,message)

@socket_.on('deliver_messages',namespace="/chat")
def _sock_deliver_(message):
	return deliver_message(request,message)

@socket_.on('disconnect_request',namespace="/chat")
def _sock_disconnect_(message):
	return disconnect_request()


if __name__ =="__main__":  
	socket_.run(app, debug=True)