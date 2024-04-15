from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def chat():
    chat_info = [
        {
            'type': 'company',
            'company_name': 'Netflix',
            'company_pic': '/static/images/netflix.png',
            'recent_chat': 'We have sent the admin info via email to your registered email address.'
        }
    ]
    return render_template('/chat.html', chat_info=chat_info)

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    emit('message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)