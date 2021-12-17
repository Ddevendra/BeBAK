from flask import *
from flask_socketio import SocketIO, emit, disconnect

app = Flask(__name__)

async_mode = None
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)
clients = []
users = []

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html', async_mode=socket_.async_mode)


@socket_.on('make_connection', namespace='/test')
def connect(message):

    # create list of connected users
    print("__________________________",request.sid)
    clients.append(request.sid)
    users.append(str(message['data']))

    # something to refer to specific user at the time of emit
    room = session.get('room')

    # display the connected user what user number he is
    user_number = clients.index(request.sid);
    emit('my_response',
         {'data': f"You are user number {user_number}", 'from': "SERVER"},
         room=clients[user_number])


@socket_.on('save_messages', namespace='/test')
def test_message(message):

    # global variable that contains the message (very bad, implement database)
    global last_message
    last_message = message['data']
    print("--------------------------",last_message)


@socket_.on('deliver_messages', namespace='/test')
def deliver_message(message):

    # deliver to specific user, specified by the sender
    sender = users[clients.index(str(request.sid))]
    emit('my_response',
         {'data': last_message, 'from': str(sender)},
         room=clients[int(message['data'])])


@socket_.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context   # pata nahi kyu h
    def can_disconnect():
        disconnect()

    emit('my_response',
         {'data': 'Disconnected!'},
         callback=can_disconnect)

    # TODO: remove the user from clients[],users[]


if __name__ == '__main__':
    socket_.run(app, debug=True)