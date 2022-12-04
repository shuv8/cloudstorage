SQLALCHEMY_DATABASE_URI = 'sqlite:///cloud.sqlite3'


def get_current_db():
    """
    Return db for current app
    :param application: current application
    :return: database
    """
    from flask import current_app
    with current_app.app_context():
        return current_app.db


