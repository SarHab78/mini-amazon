from flask import session, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, NumberRange
from flask_babel import _, lazy_gettext as _l

from .interim_added_cart_page import interim

import datetime

from .models.base_model import Product
from .models.base_model import Purchase
from .models.base_model import Product_review
from .models.base_model import Prod_Sell_Rev_Cat
from .models.base_model import Orders
from .models.base_model import Prod_user_rev


from flask import Blueprint
bp = Blueprint('product_page', __name__)

class QuantityForm(FlaskForm):
    #quantity = IntegerField(_l('Quantity to Purchase'), validators=[DataRequired()])
    #quantity = SelectField(_l('Quantity to Purchase'), validators=[DataRequired()], choices=choices)
    quantity = IntegerField('Enter the quantity you would like to purchase:', [ InputRequired(),
        NumberRange(min=1, max=99, message="Invalid range")
        ])
    add_date = StringField(_l('add_date'), validators=[DataRequired()])
    submit = SubmitField('Add to Cart')

@bp.route('/<name>/<product_id>', methods=['GET','POST'])
def product_page(name, product_id):
    form = QuantityForm()

    name = name
    product_id = product_id
    searched_products = Prod_Sell_Rev_Cat.get_search_result(search_str='book')     
    purchases = None
    products_by_other_sellers = Prod_Sell_Rev_Cat.get_products_by_other_sellers(product_id=product_id)
    seller = Product.get_product_for_page(product_id = product_id)
    page_product = Prod_Sell_Rev_Cat.get_sell_rev_info(product_id = product_id)
    prod_review = Product_review.get_prod_reviews(pid = product_id)
    avg_product_rating = Product_review.avg_product_rating(pid = product_id)
    num_reviews = Product_review.count_prod_reviews(pid = product_id)
    quant_options = Prod_Sell_Rev_Cat.get_quant_list(product_id = product_id)
    user_info = Prod_user_rev.get_user_info(pid = product_id)

    if current_user.is_authenticated():
        have_reviewed = Product_review.user_has_reviewed(uid = current_user.id, pid= product_id) #returns True if user has already reviewed this product before
    #have_reviewed_seller = Seller_review.user_has_reviewed(uid = current_user.id, sid = )

    time = datetime.datetime.now()
    form.add_date.data = time

    if form.validate_on_submit():
        add_date = request.form['add_date']

        quant_selected = form.quantity.data
        if quant_selected > quant_options[-1]:
            flash('Invalid - cannot purchase more than the currently available quantity')
            #return redirect(url_for('index.index'))
            return redirect(url_for('product_page.product_page', name=name, product_id=product_id))
        else:
            return redirect(url_for('interim.interim', name=name, product_id=product_id, quant=quant_selected))
    if form.is_submitted() and not form.validate():
        flash('Invalid - must enter a value between 0 and {}'.format(quant_options[-1]))

    return render_template('product_page.html', 
                            products_by_other_sellers = products_by_other_sellers,
                            product_row = page_product, 
                            product_reviews=prod_review,
                            avg_product_rating=avg_product_rating,
                            num_reviews=num_reviews,
                            seller=seller,
                            name = name,
                            product_id = product_id,
                            quant_options = quant_options,
                            have_reviewed = have_reviewed,
                            form=form,
                            user_info=user_info)


@bp.route('/sellerinfo', methods=['GET', 'POST'])
def sellerinfo(id):
    id=product_id
    return render_template('sellerinfo.html', id=id)

