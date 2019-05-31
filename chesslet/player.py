# chesslet/player.py

class InvalidPasswordException(Exception):
    pass


class AlreadyLoggedInException(Exception):
    pass


class PlayerNotLoggedIn(Exception):
    pass


class Player:
    def __init__(
            self,
            uuid,
            password,
            account_name,
            highscore=0,
            score=0,
            logged_in=False
    ):
        self.uuid = uuid  # (Universally Unique Identifier)
        self.password = password  # NOTE: THIS WILL BE INSECURE. DO NOT USE A PROPER PASSWORD.
        self.account_name = account_name
        self.score = score
        self.highscore = highscore
        self.logged_in = logged_in

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    # Logs a user in
    # Checks that the password inputed is the same as what is saved in the object.
    # If it is the same, set logged in true and return.
    # otherwise, raise invalid password exception.
    def login(self, password):
        self.logged_in = self.password == password
        if not self.logged_in:
            raise InvalidPasswordException("Invalid Password")

        return self.logged_in  # True

    # Logs a user outside
    # If a user is logged in, set self.logged_in to false, and return.
    # Else, raise PlayerNotLoggedIn exception.
    def logout(self):
        if self.logged_in:
            self.logged_in = False
            return True
        if not self.logged_in:
            raise PlayerNotLoggedIn
