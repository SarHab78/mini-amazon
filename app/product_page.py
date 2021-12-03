from flask import session, render_template, request, redirect
from flask_login import current_user
import datetime

from .models.base_model import Product
from .models.base_model import Purchase
from .models.base_model import Product_review
from .models.base_model import Orders


from flask import Blueprint
bp = Blueprint('product_page', __name__)

@bp.route('/<name>/<product_id>')
def product_page(name, product_id):
    name = name
    product_id = product_id
    searched_products = Product.get_search_result_2(search_str='book')     
    purchases = None
    products_by_other_sellers = Product.get_products_by_other_sellers(product_id=product_id)
    page_product = Product.get_product_for_page(product_id = product_id)
    prod_review = Product_review.get_prod_reviews(pid = product_id)
    avg_product_rating = Product_review.avg_product_rating(pid = product_id)
    num_reviews = Product_review.count_prod_reviews(pid = product_id)
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
                            product_id = product_id)
