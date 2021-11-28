from flask import Flask
from flask_login import LoginManager
from flask_babel import Babel
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'
babel = Babel()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ADD A SECRET KEY LINE - SOPHIE - this is to try to make "session" work
    app.secret_key = "any random string"

    app.db = DB(app)
    login.init_app(app)
    babel.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)
    
    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .product_page import bp as product_page_bp
    app.register_blueprint(product_page_bp)

    from .reviews import bp as reviews_bp
    app.register_blueprint(reviews_bp)

    return app


