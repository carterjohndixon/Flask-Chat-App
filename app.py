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
        # username = request.form['username']
        return render_template('chat_all.html', session=session)
    else:
        return redirect(url_for('index'))

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if(request.method == 'POST'):
        username = request.form['username']
        room = request.form['room']
        session['username'] = username
        print(username)
        session['room'] = room
        return render_template('chat.html', session=session)
    else:
        if(session.get('username') is not None):
            return render_template('chat.html', session=session)
        else:
            return redirect(url_for('index'))


# socketio for chat room
@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('username') +
         ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') +
         ': ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    print(username)
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the chat.'}, room=room)


# socketio for all chat
@socketio.on('join', namespace='/chat_all')
def join_all_chat(message):
    room = "1"
    join_room(room)
    emit('status', {'msg': 'anonymous' +
         ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat_all')
def text_all_chat(message):
    room = "1"
    emit('message', {'msg': 'anonymous' +
         ': ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat_all')
def left_all_chat(message):
    # username = session.get('username')
    # print(username)
    room = "1"
    leave_room(room)
    session.clear()
    emit('status', {'msg': 'anonymous' + ' has left the chat.'}, room=room)

if __name__ == '__main__':
    socketio.run(app)

# Using flask and socketio for a project I'm doing and I have two forms of sockets in my app.py file. Once is for the user joining, sending a chat, and leaving, all for the user chatting in a room, and the other for the user joining, sending a chat, and leaving, all for the user chatting in my all chat room. For the socket in which I'm using for all chat, I need to access the users inputed value in an input field in a from, in html, and once I try to access it getting session.get it returns none. I'm pretty sure this is because it's trying to get it from another file the user isn't on but I'm not sure how to get the variable from a different file, but same session