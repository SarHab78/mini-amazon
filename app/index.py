from flask import render_template, request, redirect
from flask_login import current_user
import datetime

from .models.base_model import Product
from .models.base_model import Purchase

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    # get all available products for sale:
    products = Product.get_all('Y')
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
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
        product_query = request.form['product_query']
        searched_products = Product.get_search_result(search_str=product_query)
        if current_user.is_authenticated:
            purchases = Purchase.get_all_by_uid_since(
                current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
        else:
            purchases = None
        return render_template('index.html',
                           avail_products=searched_products,
                           purchase_history=purchases)

    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)