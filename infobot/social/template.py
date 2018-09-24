class SocialPlugin():
    def __init__(self, config, name):
        "abstract"
        self.config = config
        self.socialName = name

    def status(self):
        raise NotImplementedError()

    def login(self):
        raise NotImplementedError()

    def logout(self):
        raise NotImplementedError()

    def post(self, topic, num, data):
        raise NotImplementedError()

    def list_followers(self):
        raise NotImplementedError()

    def follow(self, other):
        raise NotImplementedError()
