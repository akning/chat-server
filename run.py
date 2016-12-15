# -*- coding: utf-8 -*-
import eventlet
eventlet.monkey_patch()
from flask import Flask, session, render_template, request, url_for, redirect
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms
from datetime import datetime
# 为了生成动态密钥
import os
# 仅供调试使用，禁止生成pyc文件
import sys
sys.dont_write_bytecode = True

# 初始化
async_mode = 'eventlet'

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app, async_mode=async_mode)


# 首页和输入用户名后登陆
@app.route('/')
def index():
    return render_template('index.html')


# socketio事件
@socketio.on('connect')
def user_connect():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' - Server connected successfully.')

# 下线
@socketio.on('disconnect')
def user_disconnect():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' - Client disconnected.')

# 输入用户名后按回车
@socketio.on('is_online')
def user_joined(name):
    print('User [' + name + '] is online. I will check every 3 seconds.' + ' - ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    emit('online_name', name, broadcast=True)

# 用户inviter在列表中选择guest聊天，双方加入房间
@socketio.on('build_private_room')
def creat_private_room(names):
    print('The inviter is: [' + names['inviter'] + '], the guest is: [' + names['guest'] + ']')
    r = [names['inviter'], names['guest']]
    r.sort()
    room = ''.join(r)
    join_room(room)
    emit('invite_match_user', {
        'inviter': names['inviter'],
        'guest': names['guest'],
        'room': room
    }, broadcast=True)

# 处理客户端传来的message
@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg + ' - ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 调试指令，查询是否登陆成功
@app.route('/login')
def login():
    if session.get('user'):
        return session.get('user')

    return 'Not logged in!'

@app.route('/logout')
def logout():
    session.pop('user', None)

    return redirect(url_for('index'))

# 启动
if __name__ == '__main__':
    socketio.run(app, debug=True)
