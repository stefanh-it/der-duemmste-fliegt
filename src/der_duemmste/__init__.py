import os
import sys

import eventlet
eventlet.monkey_patch()

from flask import Flask
from .extensions import db, login_manager, socketio
from .socket_events import register_socket_events
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_name = os.getenv("DB_NAME")
    if not db_name or db_name == "":
        sys.exit("No database name provided")
    db_path = os.path.join(base_dir, '../..', 'db', db_name)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    from .routes import register_blueprints
    register_socket_events(socketio)
    register_blueprints(app)

    # # Check if the database exists, if not create it
    # if not os.path.exists(db_path):
    #     with app.app_context():
    #         db.create_all()
    #     print("Database created")
    return app


def main():
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=42069, debug=True, use_reloader=True)
