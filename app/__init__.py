import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel, gettext as _
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()

babel = Babel()

login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    from dotenv import load_dotenv
    load_dotenv()
    
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///app.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["BABEL_DEFAULT_LOCALE"] = os.getenv("BABEL_DEFAULT_LOCALE", "ja")
    app.config["BABEL_DEFAULT_TIMEZONE"] = os.getenv("BABEL_DEFAULT_TIMEZONE", "Asia/Tokyo")

    #拡張機能初期化
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    babel.init_app(app)
    
    from .models import User, Friend, Message, Talk, Talk_Member
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    app.jinja_env.globals['_'] = _

    #Blueprint
    from .routes import routes_bp
    from .auth import auth_bp
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)

    return app
