from database.database import DataBaseTemporary

mock_web_app_state = DataBaseTemporary()


def init_state():
    global state
    state = mock_web_app_state
