import getpass
from datetime import datetime

from entities import User
from report import reporter


class Session:

    def __init__(self):
        self._user = None
        self._time_in = None

    @property
    def user(self):
        return self._user

    @property
    def time_in(self):
        return self._time_in

    def start(self):
        try:
            login = getpass.getuser()
        except Exception:
            login = "guest"
        self._user = User(login)
        self._time_in = datetime.now()
        reporter.set_user(self._user)

    def finish(self):
        reporter.finish()


session = Session()