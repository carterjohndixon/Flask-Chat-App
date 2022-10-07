from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'ban the wind'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

socketio = SocketIO(app, manage_session=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/room', methods=['GET', 'POST'])
def room():
    all_chat = request.form.get("all_chat")
    chatting_room = request.form.get("chatting_room")
    if(all_chat):
        return render_template('join_all_chat.html', session=session)
    elif(chatting_room):
        return render_template('join_room.html', session=session)


@app.route('/chat_all', methods=['GET', 'POST'])
def chat_all():
    if (request.method == 'POST'):
        username = request.form['username']
        return render_template('chat_all.html', session=session)
    else:
        print("HELLO")

@socketio.on('join', namespace='/chat_all')
def join_all_chat(message):
    room = "1"
    join_room(room)
    username = session.get('username')
    print(username)
    print(room)
    # emit('status', {'msg': session.get('username') +
    #      ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat_all')
def text_all_chat(message):
    room = "1"
    print(room)
    username = session.get('username')
    print(username)
    # emit('message', {'msg': session.get('username') +
    #      ': ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat_all')
def left_all_chat(message):
    room = "1"
    username = session.get('username')
    print(username)
    print(room)
    leave_room(room)
    session.clear()
    # emit('status', {'msg': username + ' has left the chat.'}, room=room)

if __name__ == '__main__':
    socketio.run(app)
