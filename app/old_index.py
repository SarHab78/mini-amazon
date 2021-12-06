from flask import session, render_template, request, redirect, flash, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, NumberRange
from flask_babel import _, lazy_gettext as _l

import datetime

from .models.base_model import Product
from .models.base_model import Purchase
from .models.base_model import Orders
from .models.base_model import User

from flask import Blueprint
bp = Blueprint('index', __name__)

class SortForm(FlaskForm):
    sort_attribute = SelectField(_l('Sort By'), choices=[('name','name'),('price','price'),('category','category'), ('rating','rating')], validators=[DataRequired()])
    up_or_down = SelectField(_l('Sort By'), validators=[DataRequired()], choices=[('high-to-low','high-to-low'),('low-to-high','low-to-high')])
    submit = SubmitField('Sort')

@bp.route('/', methods=['GET', 'POST'])
def index():
    # get all available products for sale:
    products = Product.get_all('Y')
    # find the products current user has bought:
    if current_user.is_authenticated:
        user = current_user.id
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
        user = None
    # render the page by adding information to the index.html file

    # form = create some form
    # if form.validate_on_submit
    # return render_template with what I want which could be index page with products swapped
    # could use an if else statement in index.html where if u have a search result u display it
    # else display the normal index page   
    #form = searchForm()
    #if form.validate_on_submit():
    #    res = get_search_result()
    #    return render_template('index.html', avail_products=res)  

    if request.method == "POST":
        user = current_user.id

        # Try adding this request.form.get line to differentiate between the two buttons
        if request.form.get("product_query"):
            user = current_user.id
            product_query = request.form['product_query']
            session['current_query'] = product_query
            searched_products = Product.get_search_result_2(search_str=product_query)
            
            if current_user.is_authenticated:
                user = current_user.id
                purchases = Purchase.get_all_by_uid_since(
                    current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
            else:
                user = None
                purchases = None

            return render_template('index.html',
                            avail_products=searched_products,
                            purchase_history=purchases,
                            curr_uid = user,
                            sortform = sortform)

        if request.form.get("sort_query"):
            search_str = ''
            order_by = request.form['sort_query']
            if 'current_query' in session:
                search_str = session['current_query']
            searched_products = Product.get_search_result_2(search_str=search_str, order_by=order_by)
            
            # If user is signed in, get all their purchases
            if current_user.is_authenticated:
                user = current_user.id

                purchases = Purchase.get_all_by_uid_since(
                    current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
            else:
                purchases = None
                user = None

            # Return new template
            return render_template('index.html',
                                avail_products=searched_products,
                                purchase_history=purchases,
                                curr_uid = user,
                                sortform = sortform)

    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           curr_uid = user,
                           sortform = sortform)

#@bp.route('/', methods=['GET', 'POST'])
#def search_sort():
#    print('hi')

# @bp.route('/item_successfully_added')
# def interim():
#      return render_template('interim_added_cart_page.html')


