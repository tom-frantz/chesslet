class InvalidPassword(Exception):
    pass


class Player:
    def __init__(
            self,
            uuid,
            password,
            account_name,
            highscore=0
    ):
        self.uuid = uuid  # (Universally Unique Identifier)
        self.password = password  # NOTE: THIS WILL BE INSECURE. DO NOT USE A PROPER PASSWORD.
        self.account_name = account_name
        self.score = 0
        self.highscore = highscore
        self.logged_in = False

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self.__dict__)

    def login(self, password):
        self.logged_in = self.password == password
        if not self.logged_in:
            raise InvalidPassword

        return self.logged_in
