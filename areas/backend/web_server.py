from flask import Flask, make_response, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy

import app_state
import app_db

app_state.init_state()

from rest.routes import user, admin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cloud.sqlite3'

""" ----------------
    swagger specific 
    ---------------- """

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_UI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Cloud service"
    }
)

app.register_blueprint(SWAGGER_UI_BLUEPRINT, url_prefix=SWAGGER_URL)

# ROUTES

app.register_blueprint(user.get_blueprint())
app.register_blueprint(admin.get_blueprint())

""" --------------------
    end swagger specific 
    -------------------- """


@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(403)
def handle_403_error(_error):
    """Return a http 403 error to client"""
    return make_response(jsonify({'error': 'Forbidden'}), 403)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)


if __name__ == '__main__':
    db = SQLAlchemy(app)
    app_db.init_db(db)
    with app.app_context():
        from database.users.user_model import UserORM
        db.create_all()

    app.run()  # TODO USE PRODUCTION SERVER
