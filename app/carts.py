from flask import session, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, NumberRange
from flask_babel import _, lazy_gettext as _l

from .models.base_model import Product
from .models.base_model import Purchase
from .models.base_model import Product_review
from .models.base_model import Prod_Sell_Rev_Cat
from .models.base_model import Orders
from .models.base_model import User



from flask import Blueprint
bp = Blueprint('carts', __name__)



@bp.route('/carts')
def carts():
    if current_user.is_authenticated:
        print('getting to my caart')

        my_cart = Orders.get_cart(current_user.id)
        print('getting to my caart 2')

    else:
        my_cart = None
    return render_template('carts.html', user_cart = my_cart)




