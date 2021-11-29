from flask import render_template
from flask_login import current_user
import datetime

from .models.base_model import Product
from .models.base_model import Purchase


from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def carts():
    products = Product.get_all('Y')
    return render_template('carts.html')


@bp.route('/checkout')
def carts():
    products = Product.get_all('Y')
    return render_template('checkout.html')


