from flask_socketio import SocketIO, emit, disconnect 

from ..db_class import database

DBaccounts = database("./database/accounts",table="Accounts")
DBtokens = database(database="./database/tokens",table="CookieTokens")
DBclients = database(database="./database/clients",table="LiveClients")

def connect(session,request,message):
    # create list of connected users
    print("__________________________",request.sid)

    tokens = DBtokens.read()
    clients = DBclients.read()

    read_cookie_token = str(request.cookies.get("token"))
    print("got this cookie: token=",read_cookie_token)
    for token_entry in tokens:
        if read_cookie_token == token_entry[0]:

            #check if user is already connected
            user_already_live = False
            for client_entry in clients:
                if str(token_entry[1]) == client_entry[1]:
                    # rewrite the client sid
                    DBclients.delete(idd=(str(client_entry[0]),)) # delete previous client ID
                    DBclients.insert(data=(str(request.sid),client_entry[1])) # insert new client ID
                    user_already_live = True
                    break

            if not user_already_live:
                DBclients.insert(data=(str(request.sid),token_entry[1]))

            print("************User:",token_entry[1],"is Connected to socket")

    # updates room each time someone connects
    room = session.get('room')

    # display the user is connected
    emit('my_response',
         {'data': f"You are Connected", 'from': "SERVER"},
         room=str(request.sid))
    
def deliver_message(request,message):
    clients = DBclients.read()

    # deliver to specific user, specified by the sender
    try:
        for client_entry in clients:
            if client_entry[1] == str(message['to']):
                reciever_sid = client_entry[0]
            if client_entry[0] == str(request.sid):
                sender = client_entry[1]

        sender_sid = request.sid

        emit('my_response',
             {'data': message['data'], 'from': sender},
             room=reciever_sid)
        emit('self_response',
             {'data': message['data'], 'to': str(message['to'])},
             room=sender_sid)
    except:
        emit('self_response',
             {'data': message['data'], 'to': "::socket opened somehere else, please use at 1 place:: last-msg"},
             room=sender_sid)


def disconnect_request():
    @copy_current_request_context   # pata nahi kyu h
    def can_disconnect():
        disconnect()

    emit('my_response',
         {'data': 'Disconnected!'},
         callback=can_disconnect)

    # TODO: remove the user from clients[],users[]