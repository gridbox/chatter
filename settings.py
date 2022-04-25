import uuid
class Settings:
    """A class to store all settings for Chatter"""

    def __init__(self):
        self.client_id = str(uuid.uuid4())
        self.server_ip = "127.0.0.1"
        self.send_sound = ""
        self.notification_sound = ""
        self.host = "127.0.0.1"
        self.port = 10000


