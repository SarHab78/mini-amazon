from flask import session, render_template, request, redirect, flash, url_for
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, NumberRange
from flask_babel import _, lazy_gettext as _l

import datetime

from .models.base_model import Product
from .models.base_model import Purchase
from .models.base_model import Orders
from .models.base_model import User
from .models.base_model import Prod_Sell_Rev_Cat_Ord

from flask import Blueprint
bp = Blueprint('seller_order_history', __name__)

class SortForm(FlaskForm):
    sort_attribute = SelectField(_l('Sort By'), choices=[('name','name'),('price','price'),('category','category'), ('rating','rating')], validators=[DataRequired()])
    up_or_down = SelectField(_l('Sort By'), validators=[DataRequired()], choices=[('high-to-low','high-to-low'),('low-to-high','low-to-high')])
    submit = SubmitField('Sort')

class FilterForm(FlaskForm):
    # get all amazon categories list by reading the amazon_categories.csv file
    filter_fields = SelectMultipleField(_l('Filter By Category'), validators=[DataRequired()], choices=[('Automotive & Powersports', 'Automotive & Powersports'),
                            ('Baby Products', 'Baby Products'),
                            ('Books', 'Books'),
                            ('Camera & Photo', 'Camera & Photo'),
                            ('Cell Phones & Accessories', 'Cell Phones & Accessories'),
                            ('Clothing', 'Clothing'),
                            ('Consumer Electronics', 'Consumer Electronics'),
                            ('Entertainment Collectibles', 'Entertainment Collectibles'),
                            ('Fine Art', 'Fine Art'),
                            ('Grocery & Gourmet Foods', 'Grocery & Gourmet Foods'),
                            ('Health & Personal Care', 'Health & Personal Care'),
                            ('Home & Garden', 'Home & Garden'),
                            ('Independent Design', 'Independent Design'),
                            ('Industrial & Scientific', 'Industrial & Scientific'),
                            ('Major Appliances', 'Major Appliances'),
                            ('Misc', 'Misc'),
                            ('Music and DVD', 'Music and DVD'),
                            ('Musical Instruments', 'Musical Instruments'),
                            ('Office Products', 'Office Products'),
                            ('Outdoors', 'Outdoors'),
                            ('Personal Computers', 'Personal Computers'),
                            ('Pet Supplies', 'Pet Supplies'),
                            ('Software', 'Software'),
                            ('Sports', 'Sports'),
                            ('Sports Collectibles', 'Sports Collectibles'),
                            ('Tools & Home Improvement', 'Tools & Home Improvement'),
                            ('Toys & Games', 'Toys & Games'),
                            ('Video DVD & Blu-ray', 'Video DVD & Blu-ray'),
                            ('Video Games', 'Video Games'),
                            ('Watches', 'Watches')])
    submit = SubmitField('Filter by Category')

@bp.route('/order_history', methods=['GET', 'POST'])
def order_history():
    if current_user.is_authenticated:
        sell_id = current_user.id
    else:
        sell_id = -1
    # get all available products for sale:
    products = Prod_Sell_Rev_Cat_Ord.get_all(sell_id)
   
    # render the page by adding information to the index.html file

    sortform = SortForm()
    filterform = FilterForm()

    if sortform.validate_on_submit():
        order_by = sortform.sort_attribute.data
        session['order_by'] = order_by
        direc = sortform.up_or_down.data
        session['direc'] = direc

        search_str = ''
        filter_fields = 'all'
        if 'current_query' in session:
            search_str = session['current_query']
        if 'filter_fields' in session:
            filter_fields = session['filter_fields']
        searched_products = Prod_Sell_Rev_Cat_Ord.get_search_result(sell_id, search_str=search_str, order_by=order_by, direc=direc, filt_list = filter_fields)

        # If user is signed in, get all their purchases
        

        return render_template('seller_order_history.html',
                            avail_products=searched_products,
                            sortform = sortform,
                            filterform = filterform)

    elif filterform.validate_on_submit():
        search_str = ''
        if 'current_query' in session:
            search_str = session['current_query']
        order_by = 'price'
        if 'order_by' in session:
            order_by = session['order_by']
        direc = 'high-to-low'
        if 'direc' in session:
            direc = session['direc']

        filter_fields = tuple(filterform.filter_fields.data)
        #print(filter_fields)
        session['filter_fields'] = filter_fields
        searched_products = Prod_Sell_Rev_Cat_Ord.get_search_result(sell_id, search_str=search_str, order_by=order_by, direc=direc, filt_list = filter_fields)


        return render_template('seller_order_history.html',
                            avail_products=searched_products,
                            sortform = sortform,
                            filterform = filterform)


    else:
        if request.method == "POST":

            # Try adding this request.form.get line to differentiate between the two buttons
            if request.form.get("product_query"):
                product_query = request.form['product_query']
                session['current_query'] = product_query

                if product_query.lower() == "all":
                     searched_products = Prod_Sell_Rev_Cat_Ord.get_all(sell_id)
                     session['current_query'] = ''
                else:
                    searched_products = Prod_Sell_Rev_Cat_Ord.get_search_result(sell_id, search_str=product_query)
                

                return render_template('seller_order_history.html',
                                avail_products=searched_products,
                                sortform = sortform,
                                filterform = filterform)


    return render_template('seller_order_history.html',
                           avail_products=products,
                           sortform = sortform,
                           filterform = filterform)



