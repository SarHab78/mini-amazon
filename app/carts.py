from flask import render_template
from flask_login import current_user
import datetime

from .models.base_model import Product
from .models.base_model import Purchase
from .models.base_model import Orders


from flask import Blueprint
bp = Blueprint('carts', __name__)



@bp.route('/')
def carts(curr_uid):
    if current_user.is_authenticated:
        my_cart = Orders.get_cart(curr_uid)
    else:
        my_cart = None
    return render_template('carts.html', user_cart = my_cart)

@bp.route('/checkout')
def checkout():
    products = Product.get_all('Y')
    return render_template('checkout.html')


