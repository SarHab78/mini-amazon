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

    from .users_review_page import bp as users_reviews_bp
    app.register_blueprint(users_reviews_bp)

    from .add_items import bp as add_bp
    app.register_blueprint(add_bp)

    from .seller_inventory import bp as si_bp
    app.register_blueprint(si_bp)

    from .carts import bp as carts_bp
    app.register_blueprint(carts_bp)

    from .interim_added_cart_page import bp as interim_bp
    app.register_blueprint(interim_bp)

    from .seller_order_history import bp as soh_bp
    app.register_blueprint(soh_bp)

    from .this_sellers_reviews import bp as sellers_reviews_bp
    app.register_blueprint(sellers_reviews_bp)

    from .seller_reviews import bp as seller_reviews_bp
    app.register_blueprint(seller_reviews_bp)

    from .checkout import bp as checkout_bp
        app.register_blueprint(checkout_bp)


    return app


