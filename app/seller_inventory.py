from flask import render_template
from flask_login import current_user
import datetime

from .models.base_model import Product

from flask import Blueprint
bp = Blueprint('seller_inventory', __name__)

@bp.route('/inventory')
def inventory():
   
    
    # get all available products for sale from a specific seller:

   

    
    
    if current_user.is_authenticated:
        sell_id = current_user.id
    else:
        sell_id = -1
        
    products = Product.get_seller_products(sell_id)
   

   

    # render the page by adding information to the seller_inventory.html file
    return render_template('seller_inventory.html',
                           avail_products=products
                           #avail products is parameter name that will be passed to html, product has the actual data
)

