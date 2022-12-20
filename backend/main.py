from flask import Flask
from flask_socketio import SocketIO

from Account import request_account, activate_account, login

app = Flask(__name__)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

# For Email Verification (Base URL of the Server)
# base_url = "http://127.0.0.1:1237/"
base_url = "http://127.0.0.1:1237/"


@socketio.on("account_request")
def acc_request(data):
    socketio.send(request_account(data, base_url))


@socketio.on("login")
def log_in(data):
    socketio.send(login(data))


@app.route("/confirm/<string:key>")
def activate(key):
    return activate_account(key)


if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=1237)
