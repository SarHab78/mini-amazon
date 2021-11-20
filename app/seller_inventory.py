from flask import render_template
from flask_login import current_user
import datetime

from .models.base_model import Product
from .models.base_model import Purchase

from flask import Blueprint
bp = Blueprint('seller_inventory', __name__)

@bp.route('/inventory')
def inventory():
    # print(Sellers.get_all_sellers())
    # get all available products for sale:
    products = Product.get_all('Y')
    print(products)
    #this is referencing the function in the model folder where we're getting all the possible products
    #models are for writing sql queries, have the inits so that you can do like product.id or just use to x.y to get the specific parameter of a table



    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('seller_inventory.html',
                           avail_products=products,
                           #avail products is parameter name that will be passed to html, product has the actual data

                           purchase_history=purchases)

