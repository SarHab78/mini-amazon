#forms and path
#write a review
#edit
#add in access restriction to only those who have purchased

from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.base_model import Product_review


from flask import Blueprint
bp = Blueprint('reviews', __name__)

class reviewForm(FlaskForm):
    # Change strings to int at some point
    email = StringField(_l('email'), validators=[DataRequired()])
    rating = StringField(_l('rating'), validators=[DataRequired()])
    pid = StringField(_l('pid'), validators=[DataRequired()])
    review = StringField(_l('review'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    # def validate_email(self, email): when we have cart functionality - Jo?

@bp.route('/review_form', methods=['GET', 'POST'])
def write_review():
    form = reviewForm()
    if form.validate_on_submit():
        return redirect(url_for('index.index'))
    return render_template('review_form.html', title='reviews', form=form)

class sellerReviewForm(FlaskForm):
    # Change strings to int at some point
    email = StringField(_l('email'), validators=[DataRequired()])
    rating = StringField(_l('rating'), validators=[DataRequired()])
    sid = StringField(_l('sid'), validators=[DataRequired()])
    review = StringField(_l('review'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    # def validate_email(self, email): when we have cart functionality - Jo?

@bp.route('/seller_review_form', methods=['GET', 'POST'])
def write_seller_review():
    form = reviewForm()
    if form.validate_on_submit():
        return redirect(url_for('index.index'))
    return render_template('seller_review_form.html', title='reviews', form=form)
