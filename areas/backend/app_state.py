from collections import namedtuple

from database.database import DataBaseTemporary

ServerDatabase = namedtuple("Database", "prod test")
mock_web_app_state = ServerDatabase(DataBaseTemporary(), DataBaseTemporary())


def init_state():
    global state
    state = mock_web_app_state
