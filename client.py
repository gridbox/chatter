class Client:
    """A class to represent a Chatter client"""

    def __init__(self, id, display_name, connection):
        self.id = id
        self.display_name = display_name
        self.connection = connection