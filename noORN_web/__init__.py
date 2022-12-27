# from json import load
from os import getenv
from typing import Dict, Optional

from flask import Flask
from flask_login import LoginManager 

def create_app():
    app = Flask(__name__)
    # app.config["SECRET_KEY"] = getenv("SECRET_KEY", default="secret_key_example")
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    login_manager = LoginManager(app)

    # users: Dict[str, "User"] = {}

    from .User import User

    @login_manager.user_loader
    def load_user(user_id: str) -> Optional[User]:
        return User.get(user_id)

    return app



