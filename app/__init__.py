import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel, gettext as _

db = SQLAlchemy()
migrate = Migrate()

babel = Babel()

login_manager = LoginManager()
login_manager.login_view = "auth.login"


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config["SECRET_KEY"] = "dev"
    
    #PostgreSQL接続
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "sqlite:///app.db"  #環境変数がなければ SQLite
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    #Babel
    app.config["BABEL_DEFAULT_LOCALE"] = "ja"
    app.config["BABEL_DEFAULT_TIMEZONE"] = "Asia/Tokyo"

    #拡張機能初期化
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    babel.init_app(app)

    app.jinja_env.globals['_'] = _

    #Blueprint
    from .routes import routes_bp
    from .auth import auth_bp
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)

    return app
