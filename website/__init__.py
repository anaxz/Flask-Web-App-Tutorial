from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
# from flask_mail import Mail

db = SQLAlchemy()
DB_NAME = "database.db"
# mail = Mail()

def create_app():
    app = Flask(__name__) #intialise flask
    # to encrypt a secret key
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # points to where the db is stored
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app) #use db with app
    # mail.init_app(app)

    from .views import views
    from .auth import auth

    # let app know the routes/views
    # url_prefix -> use acorindg to routes so for this case its / for home
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #not using it here but need to make this is intialised before creating db
    from .models import User, Note

    create_database(app)

    #this has to be below db creation
    login_manager = LoginManager()
    #if not logged, redirect users to here
    #name of templ & func / auth file login func
    login_manager.login_view = 'auth.login' 
    login_manager.init_app(app)

    # tells flask how to load user
    # get by default looks for PK
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# if db not created, create it
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
        # db.create_all(app=app)
        # print('Created Database!')
