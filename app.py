import app.routes
from app import app, socketio


if __name__ == '__main__':
    print ("start!")
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)