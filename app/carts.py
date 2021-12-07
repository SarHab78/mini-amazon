from flask import session, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, NumberRange
from flask_babel import _, lazy_gettext as _l

from .interim_added_cart_page import interim

import datetime

from .models.base_model import Product
from .models.base_model import Purchase
from .models.base_model import Product_review
from .models.base_model import Prod_Sell_Rev_Cat
from .models.base_model import Orders
from .models.base_model import Prod_user_rev
from .models.base_model import Seller_review


from flask import Blueprint
bp = Blueprint('carts', __name__)

class Checkout(FlaskForm):
    add_date = StringField(_l('add_date'), validators=[DataRequired()])
    submit = SubmitField('Checkout')


@bp.route('/carts')
def carts():
    if current_user.is_authenticated:
        my_cart = Orders.get_cart(current_user.id)
    else:
        my_cart = None
    return render_template('carts.html', user_cart = my_cart)

@bp.route('/checkout')
def checkout():
    form = Checkout()
    time = datetime.datetime.now()
    form.add_date.data = time

    if form.validate_on_submit():
        add_date = request.form['add_date']
    if form.is_submitted() and not form.validate():
        flash('Error, please try again later')
    checking_out = checkout_cart(uid, add_date)
    return render_template('checkout.html', checking_out)


