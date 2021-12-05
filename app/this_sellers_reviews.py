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

from flask import Blueprint
bp = Blueprint('sellers_reviews', __name__)

#not importing anything here - whyyyy

@bp.route('/<sid>/seller_reviews')
def seller_reviews(sid):
    sellrevs = Seller_review.get_seller_reviews(sid = sid)
    avg = Seller_review.avg_seller_rating(sid = sid)
    ct = Seller_review.count_seller_reviews(sid = sid)

    return render_template('reviews_of_this_seller.html',
                           sid = sid,
                           seller_reviews = sellrevs,
                           avg_seller_rating = avg,
                           num_seller_reviews = ct)