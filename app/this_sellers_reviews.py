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
#from .models.base_model import Product_review
from .models.base_model import Seller_review
from .models.base_model import Add_seller_review
from .models.base_model import Sell_user_rev
from .models.base_model import User

from flask import Blueprint
bp = Blueprint('this_sellers_reviews', __name__)


@bp.route('/<sid>/sellers_reviews')
def sellers_reviews(sid):
    sellrevs = Seller_review.get_seller_reviews(sid = sid)
    avg = Seller_review.avg_seller_rating(sid = sid)
    ct = Seller_review.count_seller_reviews(sid = sid)
    reviewer_info = Sell_user_rev.get_user_info(sid=sid)
    seller_info = User.get(sid)

    return render_template('reviews_of_this_seller.html',
                           sid = sid,
                           sellers_reviews = sellrevs,
                           avg_seller_rating = avg,
                           num_seller_reviews = ct, 
                           reviewer_info=reviewer_info,
                           seller_info = seller_info)
