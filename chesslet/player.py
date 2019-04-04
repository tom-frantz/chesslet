class Player:
    def __init__(self, uuid, password):
        self.uuid = uuid # (Universally Unique Identifier)
        self.password = password # NOTE: THIS WILL BE INSECURE. DO NOT USE A PROPER PASSWORD.
        self.account_name = ""
        self.score = ""
        self.highscore = ""

    def createUser(self):
        pass

    def setHighscore(self, score):
        pass
    
    def changeUuid(self, uuid):
        pass
    
    def login(self, uuid, password):
        pass
