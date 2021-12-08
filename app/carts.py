from flask import session, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, NumberRange
from flask_babel import _, lazy_gettext as _l

import datetime

from .models.base_model import Product
from .models.base_model import Purchase
from .models.base_model import Product_review
from .models.base_model import Prod_Sell_Rev_Cat
from .models.base_model import Orders
from .models.base_model import Prod_user_rev
from .models.base_model import Seller_review
from .models.base_model import Prod_Sell_Rev_Cat_Ord



from flask import Blueprint
bp = Blueprint('carts', __name__)


@bp.route('/carts')
def carts():
    if current_user.is_authenticated:
        # my_cart = Orders.get_cart(current_user.id)
        my_cart = Prod_Sell_Rev_Cat_Ord.get_cart(current_user.id)
        sellers_amounts_dict = Prod_Sell_Rev_Cat_Ord.get_sellers_and_incs(my_cart)
        buyers_amounts_dict = Prod_Sell_Rev_Cat_Ord.get_buyers_and_decs(my_cart)
        products_amounts_dict = Prod_Sell_Rev_Cat_Ord.get_products_and_decs(my_cart)

        print(sellers_amounts_dict)
        print(buyers_amounts_dict)
        print(products_amounts_dict)
    
    else:
        my_cart = None
    return render_template('carts.html', user_cart = my_cart)

@bp.route('/delete/<prod_id>/from_cart')
def delete_item(uid, prod_id):
    my_cart = Orders.delete_item(uid, prod_id)
    return render_template('item_deleted.html', my_cart = my_cart)

