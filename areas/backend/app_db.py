SQLALCHEMY_DATABASE_URI = 'sqlite:///cloud.sqlite3'


def get_current_db(app):
    """
    Return db for current app
    :return: database
    """
    with app.app_context():
        return app.db
