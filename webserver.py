from flask import Flask
app = Flask(__name__)


class ServerState:
    """
    This class will be responsible for handling all the communication to the model.
    It is also responsible for handling players logging in and out as well as many other similar concerns
    """
    def __init__(self):
        self.players = {}
        self.games = {}


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    server_state = ServerState()
    app.run()
