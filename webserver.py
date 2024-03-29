# webserver.py

import random

from flask import Flask
import flask.json
from flask_socketio import SocketIO, emit, join_room
import json

from chesslet.board import Board, InvalidPieceSelectionException
from chesslet.player import Player, AlreadyLoggedInException, InvalidPasswordException, PlayerNotLoggedIn
from chesslet.point import Point
from chesslet.session import Session, PlayerAlreadyAddedException, NotCurrentPlayerTryingToMoveException

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


class PlayerAlreadyExistsException(Exception):
    pass


class PlayerNotFoundException(Exception):
    pass


def response_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            res = {"success": True}
            func_return = func(*args, **kwargs)
            res.update({} if func_return is None else func_return)
            return res
        # TODO FIND ALL EXCEPTIONS IN HERE
        except (
            PlayerNotFoundException,
            AlreadyLoggedInException,
            InvalidPasswordException,
            PlayerNotLoggedIn,
            PlayerAlreadyAddedException,
            InvalidPieceSelectionException,
            NotCurrentPlayerTryingToMoveException
        ) as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            print(e)
            return {"success": False, "error": "Server Error"}
    return wrapper


class ServerState:
    """
    This class will be responsible for handling all the communication to the model.
    It is also responsible for handling players logging in and out as well as many other similar concerns
    """
    def __init__(self, user_file_path):
        self.players = {}
        self.games = {}
        self.user_file_path = user_file_path

        # Load in the persisted users.
        with open(user_file_path) as user_file:
            players = json.load(user_file)
            for player in players.values():
                self.players[player["uuid"]] = Player(
                    uuid=player["uuid"],
                    password=player["password"],
                    account_name=player["account_name"],
                    highscore=player["highscore"]
                )

    def save_users(self):
        json.dump(self.players, self.user_file_path, indent=4)

    def register_user(self, uuid, password, account_name):
        if uuid in self.players:
            raise PlayerAlreadyExistsException("Player with " + uuid + " already present!")

        self.players[uuid] = Player(
            uuid=uuid,
            password=password,
            account_name=account_name,
        )

    def login_player(self, username, password):
        uuid = ""
        for user in self.players.values():
            if user.account_name == username:
                uuid = user.uuid
                break

        if uuid not in self.players:
            raise PlayerNotFoundException("Player with name'" + username + "' not found!")

        return self.players[uuid].login(password), uuid

    def new_game(self, user_uuid):
        game_uuid = random.randint(1000, 9999)
        game_uuid = str(game_uuid)

        self.games[game_uuid] = Session(game_uuid)
        self.games[game_uuid].add_player(self.players[user_uuid])
        return game_uuid

    def join_game(self, user_uuid, game_uuid):
        self.games[game_uuid].add_player(self.players[user_uuid])
        return


server_state = ServerState("./users.json")


class customJSONEncoder:
    @staticmethod
    def default_func(obj):
        if type(obj) is set:
            obj = list(obj)
        elif type(obj) is Point:
            obj = {"x": obj.x, "y": obj.y}
        return obj

    @staticmethod
    def dumps(obj, **kwargs):
        return flask.json.dumps(obj, **kwargs, default=customJSONEncoder.default_func)

    @staticmethod
    def loads(string, **kwargs):
        return flask.json.loads(string, **kwargs)


socketio = SocketIO(app, json=customJSONEncoder)


@socketio.on("login")
@response_decorator
def login(data):
    success, uuid = server_state.login_player(data['username'], data['password'])
    return {
        "token": uuid,
        "b": Board(Session("")).get_board_state()
    }


@socketio.on("create_game")
@response_decorator
def create_game(data):
    game_uuid = server_state.new_game(data["token"])

    join_room(game_uuid)
    return {
        "game_uuid": game_uuid
    }


@socketio.on("join_game")
@response_decorator
def join_game(data):
    game_uuid = data["game_uuid"]

    server_state.join_game(
        user_uuid=data["token"],
        game_uuid=game_uuid
    )

    join_room(game_uuid)

    emit("game start", {"b": server_state.games[game_uuid].get_game_state()}, json=True, room=game_uuid)
    return


@socketio.on("leave_game")
@response_decorator
def leave_game(data):
    pass


@socketio.on("move_piece")
@response_decorator
def move_piece(data):
    server_state.games[data["game_uuid"]].move_piece(
        data["token"],
        Point(data["from_pos"]["x"], data["from_pos"]["y"]),
        Point(data["to_pos"]["x"], data["to_pos"]["y"]),
        data["combination_state"] if data["combination_state"] else None
    )

    emit("move piece", {"b": server_state.games[data["game_uuid"]].get_game_state()}, json=True, room=data["game_uuid"])
    return


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0")
