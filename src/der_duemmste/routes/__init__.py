from .auth import auth_bp
from .routes import main_bp
from .questions import questions_bp
from .user import user_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(questions_bp, url_prefix="/questions")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")
