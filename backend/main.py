from flask import Flask, request
import random, string
from flask_socketio import SocketIO, send, emit

from Account import request_account, activate_account, login, accs_keys
from BanStuff import process_deposit, process_withdrawal

from Games.tictactoe import TicTacToe

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")
socketio.init_app(app, cors_allowed_origins="*")

# For Email Verification (Base URL of the Server)
# base_url = "http://127.0.0.1:1237/"
base_url = "https://bangames.jjhost.tk/"


# ACCOUNT STUFF ------------------------------------------------------------------------------------------------------
@socketio.on("account_request")
def acc_request(data):
    send(request_account(data, base_url))


@socketio.on("login")
def log_in(data):
    send(login(data))


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
    emit("stats", stats)


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
    accs_keys[data["key"]] = acc
    if not process_withdrawal(address, amount):
        send({"status": "error", "message": "Error when Withdrawing"})
        return
    status(data)


@app.route("/confirm/<string:key>")
def activate(key):
    return activate_account(key)


# GAMES ------------------------------------------------------------------------------------------------------
ttt_games = {}
# Player on position 0 -> 0
# Player on position 1 -> X


@socketio.on("connect", namespace="/tictactoe")
def list_ttt_games():
    serialized = {}
    for key in ttt_games:
        serialized[key] = ttt_games[key].copy()
        serialized[key]["game_instance"] = serialized[key]["game_instance"].__repr__()
        serialized[key]["players"] = len(serialized[key]["players"])
    emit("games", serialized, namespace="/tictactoe")


@socketio.on("create_ttt_game", namespace="/tictactoe")
def create_ttt_game(data):
    try:
        acc = accs_keys[data["key"]]
        stake = float(data["stake"])
        if stake < 0.01 or acc["balance"] < stake:
            send(
                {"status": "error", "message": "Balance or stake too low"},
                namespace="/tictactoe",
            )
            return
    except:
        return
    # Only one game creation per account
    for game in ttt_games:
        for player in ttt_games[game]["players"]:
            if data["key"] == player:
                send(
                    {"status": "error", "message": "One game creation per user"},
                    namespace="/tictactoe",
                )
                return
    while True:
        tmpkey = "".join(random.SystemRandom().choice(string.digits) for _ in range(8))
        try:
            ttt_games[tmpkey]
        except:
            break
    # Initialize new TicTacToe Game
    ttt_games[tmpkey] = {
        "game_instance": TicTacToe(),
        "players": [data["key"]],
        "stake": stake,
    }
    send({"status": "ok", "data": {"game_id": tmpkey}}, namespace="/tictactoe")


@socketio.on("join_ttt_game", namespace="/tictactoe")
def join_ttt_game(data):
    try:
        acc = accs_keys[data["key"]]
        game_id = data["game_id"]
        ttt_games[game_id]
    except:
        return
    # Check if user is already in a game
    for game in ttt_games:
        for player in ttt_games[game]["players"]:
            if data["key"] == player:
                send(
                    {"status": "error", "message": "Already in a game"},
                    namespace="/tictactoe",
                )
                return
    # Check if user has enough stake
    if acc["balance"] < ttt_games[game_id]["stake"]:
        send({"status": "error", "message": "Balance too low"}, namespace="/tictactoe")
        return
    # Check if game is free
    if len(ttt_games[game_id]["players"]) < 2:
        if not data["key"] in ttt_games[game_id]["players"]:
            ttt_games[game_id]["players"].append({"key": data["key"]})
            send({"status": "ok"}, namespace="/tictactoe")
        else:
            send({"status": "ok"}, namespace="/tictactoe")
    else:
        send(
            {"status": "error", "message": "This room is full"}, namespace="/tictactoe"
        )


@socketio.on("place", namespace="/tictactoe")
def place_tic_tac_toe(data):
    try:
        acc = accs_keys[data["key"]]
        game = ttt_games[data["game_id"]]
        position = int(data["position"])
    except:
        return
    try:
        player = game["players"].index(data["key"])
        player = "O" if player == 0 else "X"
    except ValueError:
        send(
            {"status": "error", "message": "You are not in this Room"},
            namespace="/tictactoe",
        )
    # Check if user is in this game
    if game["game_instance"].__repr__()["currentPlayer"] == player:
        if game["game_instance"].makeMove(position):
            socketio.send(
                {"status": "ok", "data": game["game_instance"].__repr__()},
                namespace="/tictactoe",
            )
        else:
            send(
                {"status": "error", "message": "Illegal Move"},
                namespace="/tictactoe",
            )
    else:
        send(
            {"status": "error", "message": "It's not your Turn"},
            namespace="/tictactoe",
        )


if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=1237)
