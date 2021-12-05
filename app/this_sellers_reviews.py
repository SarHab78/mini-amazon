from flask import session, render_template, request, redirect
from flask_login import current_user
import datetime

from .models.base_model import Product
from .models.base_model import Purchase
from .models.base_model import Product_review
from .models.base_model import Seller_review
from .models.base_model import Add_seller_review

from flask import Blueprint
bp = Blueprint('seller_review_page', __name__)

@bp.route('/<sid>/reviews')
def seller_reviews(sid):
    sellrevs = seller_review.get_seller_reviews(sid)
    avg = seller_review.avg_seller_rating(sid)
    ct = seller_review.count_seller_reviews(sid)

    return render_template('reviews_of_this_seller.html',
                           seller_reviews = sellrevs,
                           avg_seller_rating = avg,
                           num_seller_reviews = ct)