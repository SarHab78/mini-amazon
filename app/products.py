from flask import render_template
from flask_login import current_user
import datetime

from .models.base_model import Product
from .models.base_model import Purchase

from flask import Blueprint
bp = Blueprint('product', __name__)

@bp.route('/product')
def product_info():

    products = Product.get_all('Y')
    print(products)
    #this is just a placeholder for what will end up being product info
    #for an individual product

    
        
    # render the page by adding information to the index.html file
    return render_template('product_page.html',
                           avail_products=products)
