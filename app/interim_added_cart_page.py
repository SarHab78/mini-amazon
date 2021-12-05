from flask import session, render_template, request, redirect
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, EqualTo, InputRequired, NumberRange
from flask_babel import _, lazy_gettext as _l


import datetime

from .models.base_model import Product
from .models.base_model import Purchase
from .models.base_model import Product_review
from .models.base_model import Prod_Sell_Rev
from .models.base_model import Orders

from flask import Blueprint
bp = Blueprint('interim', __name__)


class Ordered_date(FlaskForm):
    add_date = StringField(_l('add_date'), validators=[DataRequired()])


@bp.route('/<name>/<product_id>/<quant>successfully_added')
def interim(uid, name, product_id, quant, add_date):
    searched_products = Product.get_search_result_2(search_str='book')     
    quant = int(quant)
    purchases = None
    page_product = Prod_Sell_Rev.get_sell_rev_info(product_id = product_id)
    prod_review = Product_review.get_prod_reviews(pid = product_id)
    avg_product_rating = Product_review.avg_product_rating(pid = product_id)
    num_reviews = Product_review.count_prod_reviews(pid = product_id)
    

    time = datetime.datetime.now()
    form.add_date.data = time
    
    add_date = request.form['add_date']


    cart = Orders.add_to_cart(prod_id = product_id, quantity = quant, uid = uid, add_date = add_date)
    print(page_product)
    
    if current_user.is_authenticated:
        sell_id = current_user.id
    else:
        sell_id = -1
    
    # Return new template
    #return render_template('index.html',
    #                    avail_products=searched_products,
    #                    purchase_history=purchases)
    return render_template('interim_added_cart_page.html', 
                            product_row = page_product, 
                            product_reviews=prod_review,
                            avg_product_rating=avg_product_rating,
                            num_reviews=num_reviews,
                            sell_id = sell_id,
                            quant=quant)


