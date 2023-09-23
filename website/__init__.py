from os import path

import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisissecrect'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import User, Note, Productdetails
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    return app


def create_database(app: Flask):
    if not path.exists('instance/' + DB_NAME):
        from .models import Productdetails
        with app.app_context():
            db.create_all()
            rows = pd.read_csv('products.csv', dtype=str).to_dict('records')
            for row in rows:
                print(row)
                db.session.add(Productdetails(**row))
                db.session.commit()

        print('Created database!')
    else:
        print('DB exists')
