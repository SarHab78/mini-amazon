from flask import session, render_template, request, redirect
from flask_login import current_user
import datetime

from .models.base_model import Product
from .models.base_model import Purchase
from .models.base_model import Product_review

from flask import Blueprint
bp = Blueprint('users_review_page', __name__)

@bp.route('/myreviews')
def myreviews():

    myrevs = product_review.get_users_reviews(uid) #accessing their uid? - sarah?

    return render_template('users_reviews.html',
                           user_reviews = myrevs)