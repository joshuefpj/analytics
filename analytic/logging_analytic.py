from datetime import datetime


class Logging:
    """Used for proper management of the logs.

    The structure of message will contain the time, short message and
    message's level.

    For this case we will handle 2 levels:
        - Info
        - Warning
    """

    def __init__(self, message, level='Info'):
        self.message = message
        self.level = level
        ct = datetime.now()
        self.ct = ct.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f'### ({self.level} {self.ct} | {self.message})'
