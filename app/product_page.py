from flask import session, render_template, request, redirect, flash, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, NumberRange
from flask_babel import _, lazy_gettext as _l
from flask_login import current_user
from .interim_added_cart_page import interim

import datetime

from .models.base_model import Product
from .models.base_model import Purchase
from .models.base_model import Product_review
from .models.base_model import Prod_Sell_Rev
from .models.base_model import Orders


from flask import Blueprint
bp = Blueprint('product_page', __name__)

class QuantityForm(FlaskForm):
    #quantity = IntegerField(_l('Quantity to Purchase'), validators=[DataRequired()])
    #quantity = SelectField(_l('Quantity to Purchase'), validators=[DataRequired()], choices=choices)
    quantity = IntegerField('Enter the quantity you would like to purchase:', [ InputRequired(),
        NumberRange(min=1, max=99, message="Invalid range")
        ])
    submit = SubmitField('Add to Cart')

@bp.route('/<name>/<product_id>', methods=['GET','POST'])
def product_page(name, product_id):
    name = name
    product_id = product_id
    searched_products = Product.get_search_result_2(search_str='book')     
    purchases = None
    products_by_other_sellers = Prod_Sell_Rev.get_products_by_other_sellers(product_id=product_id)
    #page_product = Product.get_product_for_page(product_id = product_id)
    page_product = Prod_Sell_Rev.get_sell_rev_info(product_id = product_id)
    prod_review = Product_review.get_prod_reviews(pid = product_id)
    avg_product_rating = Product_review.avg_product_rating(pid = product_id)
    num_reviews = Product_review.count_prod_reviews(pid = product_id)
    quant_options = Prod_Sell_Rev.get_quant_list(product_id = product_id)

    form = QuantityForm()
    if form.validate_on_submit():
        quant_selected = form.quantity.data
        if quant_selected > quant_options[-1]:
            flash('Invalid - cannot purchase more than the currently available quantity')
            #return redirect(url_for('index.index'))
            return redirect(url_for('product_page.product_page', name=name, product_id=product_id))
        else:
            print("here is the error")
            return interim(current_user.id, name, product_id, quant_selected)
            # return redirect(url_for('interim.interim',  uid = current_user.id, name=name, product_id=product_id, quant=quant_selected))

    # Return new template
    #return render_template('index.html',
    #                    avail_products=searched_products,
    #                    purchase_history=purchases)
    return render_template('product_page.html', 
                            products_by_other_sellers = products_by_other_sellers,
                            product_row = page_product, 
                            product_reviews=prod_review,
                            avg_product_rating=avg_product_rating,
                            num_reviews=num_reviews,
                            name = name,
                            product_id = product_id,
                            quant_options = quant_options,
                            form=form)
