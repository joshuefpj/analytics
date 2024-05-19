from datetime import datetime


def warning_(func):
    def wrap(*args, **kwargs):
        print('*' * 49)
        func(*args, **kwargs)
        print('*' * 49)

    return wrap


class Logging:
    """Used for proper management of the logs.

    The structure of message will contain the time, short message and
    message's level.

    For this case we will handle 2 levels:
        - Info
        - Warning
    """

    def __init__(self, message):
        self.message = message
        ct = datetime.now()
        self.ct = ct.strftime("%Y-%m-%d %H:%M:%S")

    def info(self):
        print(f'### INFO ({self.ct}) | {self.message})')

    @warning_
    def warning(self):
        print(f'$$$ WARNING ({self.ct}) | {self.message})')


if __name__ == '__main__':
    l_i = Logging('Testing INFO Message')
    l_w = Logging('Testing WARNING Message', 'warning')

    getattr(l_i, 'info')()
    getattr(l_w, 'warning')()
