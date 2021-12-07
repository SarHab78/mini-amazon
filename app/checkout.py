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
bp = Blueprint('checkout', __name__)

class checkout_stuff(FlaskForm):
    submit = SubmitField('Checkout Cart')

@bp.route('/checkout')
def checkout():
    return render_template('checkout.html')
    
    
bp.route('/final_checkout')
def final_checkout():
    my_cart = Orders.get_cart(current_user.id)
    balance = current_user.balance
    price = total_price(prod_id, current_user.id)
    if form.validate_on_submit():
        if balance < total:
            flash('Insufficient Funds, you current have a balance of ${}, your cart total is ${}', balance, total)
        else:
            return Orders.checkout_cart(balance = balance, uid = current_user.id)
    if form.is_submitted() and not form.validate():

    return render_template('finalized_order.html')
