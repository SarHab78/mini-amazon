from flask import render_template
from flask_login import current_user
import datetime

from .models.base_model import Product
from .models.base_model import Purchase

from flask import Blueprint
bp = Blueprint('profile', __name__)

@bp.route('/profile')
def profile():
    # print(Sellers.get_all_sellers())
    # get all available products for sale:

    #this is referencing the function in the model folder where we're getting all the possible products
    #models are for writing sql queries, have the inits so that you can do like product.id or just use to x.y to get the specific parameter of a table



    # find the products current user has bought:
    
    
    profile = User.get_user_info(2)
    

    
        
    # render the page by adding information to the index.html file
    return render_template('profile.html',
                           user_info=profile
                           #avail products is parameter name that will be passed to html, product has the actual data
