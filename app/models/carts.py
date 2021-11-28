from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('carts', __name__)

@bp.route('/checkout')
def checkout():
    products = Product.get_all(True)
    return render_template('checkout.html')
