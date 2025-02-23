import eventlet
eventlet.monkey_patch()

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask import Flask
import os
import sys
from .socket_events import register_socket_events
from dotenv import load_dotenv

load_dotenv()

socketio = SocketIO(cors_allowed_origins="*")
db = SQLAlchemy()
login_manager = LoginManager()


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
    from .auth import auth_bp
    from .routes import main_bp
    # Check if the database exists, if not create it
    if not os.path.exists(db_path):
        with app.app_context():
            db.create_all()
        print("Database created")
    login_manager.init_app(app)
    socketio.init_app(app)
    register_socket_events(socketio)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    return app


def main():
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=42069, debug=True, use_reloader=True)
