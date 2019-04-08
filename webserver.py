import os

from flask import Flask
import json

from chesslet.player import Player

app = Flask(__name__)


class PlayerAlreadyExistsException(Exception):
    pass

class PlayerNotFoundException(Exception):
    pass


class ServerState:
    """
    This class will be responsible for handling all the communication to the model.
    It is also responsible for handling players logging in and out as well as many other similar concerns
    """
    def __init__(self, user_file_path):
        self.players = {}
        self.games = {}

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
        json.dump(self.players, "users.json", indent=4)

    def register_user(self, uuid, password, account_name):
        if uuid in self.players:
            raise PlayerAlreadyExistsException("Player with " + uuid + " already present!")

        self.players[uuid] = Player(
            uuid=uuid,
            password=password,
            account_name=account_name,
        )

    def login_player(self, uuid, password):
        if uuid not in self.players:
            raise PlayerNotFoundException("Player with" + uuid + " not found!")

        return self.players[uuid].login(password)


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    server_state = ServerState()
    app.run()
