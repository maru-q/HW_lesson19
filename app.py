from flask import Flask
from flask_restx import Api

from config import Config
from dao.model.user import User
from setup_db import db
from views.auth import auth_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns
from views.protected import protected_ns


def create_app(config_object):
    new_app = Flask(__name__)
    new_app.config.from_object(config_object)
    register_extensions(new_app)
    return new_app


def register_extensions(my_app):
    db.init_app(my_app)
    api = Api(my_app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(protected_ns)
    create_data(my_app, db)


def create_data(app, db):
    with app.app_context():
        db.create_all()

        u1 = User(username="vasya", password="my_little_pony", role="user")
        u2 = User(username="oleg", password="qwerty", role="user")
        u3 = User(username="oleg", password="P@ssw0rd", role="admin")

        with db.session.begin():
            db.session.add_all([u1, u2, u3])


app = create_app(Config())
# app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
