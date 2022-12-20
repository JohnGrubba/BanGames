from flask import Flask
from flask_socketio import SocketIO

from Account import request_account, activate_account, login, accs_keys
from BanStuff import process_deposit, process_withdrawal

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


@socketio.on("status")
def status(data):
    try:
        acc = accs_keys[data["key"]]
        if not acc:
            raise Exception()
    except:
        return
    stats = {
        "balance": acc["balance"],
        "deposit_address": acc["deposit_keypair"]["address"],
        "username": acc["username"],
    }
    socketio.send(stats)


@socketio.on("deposit")
def deposit(data):
    try:
        acc = accs_keys[data["key"]]
    except:
        return
    acc["balance"] += process_deposit(acc["deposit_keypair"])
    accs_keys[data["key"]] = acc
    status(data)


@socketio.on("withdraw")
def withdraw(data):
    try:
        acc = accs_keys[data["key"]]
        amount = float(data["amount"])
        address = data["address"]
        if amount < 0.01 or acc["balance"] < amount:
            raise Exception()
    except:
        return
    acc["balance"] -= amount
    if not process_withdrawal(address, amount):
        socketio.send({"status": "error", "message": "Error when Withdrawing"})
        return
    accs_keys[data["key"]] = acc
    status(data)


@app.route("/confirm/<string:key>")
def activate(key):
    return activate_account(key)


if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=1237)
