from flask import Flask, render_template,session
from flask_socketio import SocketIO,send,join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html') # ВЫВЕСТИ ШАБЛОН index.html

@socketio.on('set_room') # ЗАДАТЬ ДЕЙСТВИЕ ПОДКЛЮЧИТСЯ К КОМНАТЕ
def set_room(room): # РИНИМАЕТ нАЗВАНИЕ КОМНАТЫ
    join_room(room) # ПОДКЛЮЧАЕМСЯ К КОМНАТЕ
    session['room'] = room # ДОБАВЛЯЕМ В СЕАНС ПОЛЬЗОВАТЕЛЯ
    send(f'Вы подключились к {room}') # ОТПРАВЛЯЕМ ИНФОРМАЦИЮ О ПОДКЛЮЧЕНИИ



@socketio.on('message') # ПРИ ПОЛУЧЕНИИ СООБЩЕНИЕ
def get_message_from_page(message): 
    if 'room' in session:# ПРОВЕРЯЕМ В ТЕКУЩЕМ СЕАНСЕ НАЛИЧИЕ ИНФОРМАЦИИ О КОМНАТЕ
        room = session['room'] # ПРИ НАЛИЧИИ КОМАНТЫ
        send(message,broadcast=True,to=room) # ОТПРАВИТЬ СООБЩЕНИЕ ВСЕ УЧАСТНИКАМ КОМНАТЫ
    else:  #  ЕСЛИ КОМАНТЫ НЕТ ТОГДА 
        send(message) # ООТПРАВИТЬ ТОМУ КТО ПРИСЛАЛ


if __name__ == '__main__':
    socketio.run(app)
