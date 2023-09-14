from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
import flask_monitoringdashboard as dashboard

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app(database_uri=f'sqlite:///{DB_NAME}'):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_secret_key_12'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    db.init_app(app)
    dashboard.bind(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app: Flask) -> None:
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Database created!')
