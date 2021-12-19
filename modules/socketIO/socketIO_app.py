from flask_socketio import SocketIO, emit, disconnect 

from ..db_class import database

DBaccounts = database("./database/accounts",table="Accounts")
DBtokens = database(database="./database/tokens",table="CookieTokens")

clients = []
users = []


def connect(session,request,message):
    # create list of connected users
    print("__________________________",request.sid)

    # getting username
    tokens = DBtokens.read()

    read_cookie_token = str(request.cookies.get("token"))
    print("got this cookie: token=",read_cookie_token)
    for entry in tokens:
        if read_cookie_token == entry[0]:

            #check if user is already connected (implement database to resolve the multiple login issue)
            if str(entry[1]) not in users:
                users.append(entry[1])
                clients.append(request.sid)
            print("************User:",entry[1],"is Connected to socket")

    # something to refer to specific user at the time of emit
    room = session.get('room')

    # display the user is connected
    emit('my_response',
         {'data': f"You are Connected", 'from': "SERVER"},
         room=clients[clients.index(str(request.sid))])

def set_message(request,message):
    # global variable that contains the message (very bad, implement database)
    global last_message
    last_message = message['data']
    print("--------------------------",last_message)

def deliver_message(request,message):
    # deliver to specific user, specified by the sender
    sender = users[clients.index(str(request.sid))]
    reciever_index = users.index(str(message['data']))
    emit('my_response',
         {'data': last_message, 'from': str(sender)},
         room=clients[reciever_index])
    emit('self_response',
         {'data': last_message, 'to': str(users[reciever_index])},
         room=clients[clients.index(str(request.sid))])

def disconnect_request():
    @copy_current_request_context   # pata nahi kyu h
    def can_disconnect():
        disconnect()

    emit('my_response',
         {'data': 'Disconnected!'},
         callback=can_disconnect)

    # TODO: remove the user from clients[],users[]