import os
from collections import defaultdict

from flask import render_template
from flask_socketio import emit

from app import app, socketio
from . import converter

root_url = "http://localhost:5000/"
load_id_dict = defaultdict(lambda: 0)
save_id_dict = defaultdict(lambda: 0)


@app.route("/")
@app.route("/index")
def index():
    return "HELLO WORLD!"


@app.route("/player/<int:id>")
def player(id):
    return render_template('player.html', id=id, root_url=root_url)


@app.route("/playground/<int:id1>")
def play_ground(id1):
    return render_template('play_ground.html', id1=id1, root_url=root_url)


@socketio.on("test", namespace="/test")
def test():
    print("test", "connected")
    emit('my response', {'data': 'Connected'})


@socketio.on('testing', namespace='/test')
def test_message(message):
    print(message)


@socketio.on('send image', namespace='/test')
def save_image(message):
    id, img = message['id'], message['img']

    dir = f"./app/resources/user/{id}/"
    if not os.path.exists(os.path.dirname(dir)):
        try:
            os.makedirs(os.path.dirname(dir))
        except:
            emit('save image response', {'status': False, 'msg': 'Fail to make a directory'}, broadcast=True)

    trimmed_img_base64 = img.replace('data:image/png;base64,', '')
    probability, idx = converter.convert_from_base64(trimmed_img_base64)

    emit('convert image', {
        'status': True,
        'msg': f'Successfully convert image',
        'probability': probability,
        'label': idx},
         broadcast=True)
#
#
# @socketio.on('convert image', namespace='/test')
# def convert_image(message):
#     id = message['id']
#     file_path = f'./app/resources/user/{id}/{load_id_dict[id]}.png'
#     if not os.path.exists(file_path):
#         emit('convert image response', {'status': False, 'msg': 'No image to process'}, broadcast=True)
#         return
#
#     try:
#         probability, idx = converter.convert(file_path)
#         os.remove(file_path)
#         emit('convert image response',
#              {'status': True,
#               'probability': probability,
#               'label': idx,
#               'msg': f'Successfully convert image {file_path}'},
#              broadcast=True)
#
#     except:
#         emit('convert image response',
#              {'status': False, 'msg': f'Fail to convert image {file_path}'},
#              broadcast=True)
#     load_id_dict[id] += 1