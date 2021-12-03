from flask import render_template
from flask_login import current_user
import datetime

from .models.base_model import Product

from flask import Blueprint
bp = Blueprint('seller_order_history', __name__)

@bp.route('/seller_order_history')
def seller_order_history():
   
    # print(Sellers.get_all_sellers())
    # get all available products for sale:

    #this is referencing the function in the model folder where we're getting all the possible products
    #models are for writing sql queries, have the inits so that you can do like product.id or just use to x.y to get the specific parameter of a table



    # find the products current user has bought:
    
    if current_user.is_authenticated:
        sell_id = current_user.id
    else:
        sell_id = -1
        
    products = Product.get_seller_products(sell_id)

   

    # render the page by adding information to the index.html file
    return render_template('seller_order_history.html',
                           avail_products=products
                           #avail products is parameter name that will be passed to html, product has the actual data
)
