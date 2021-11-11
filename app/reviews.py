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

from .models.review import Product_review


from flask import Blueprint
bp = Blueprint('reviews', __name__)

class AddAReview(FlaskForm):
    email = StringField(_l('email'), validators=[DataRequired(), Email()])
    rating = IntegerField(_l('rating'), validators=[DataRequired()])
    pid = IntegerField(_l('rating'), validators=[DataRequired()])
    review = StringField(_l('rating'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    # def validate_email(self, email): when we have cart functionality - Jo?

@bp.route('/review_form', methods=['GET', 'POST'])
def post_review():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = AddAReview()
    if form.validate_on_submit():
        if Product_review.get_prod(
                         form.pid.data,
                         form.email.data,
                         form.rating.data,
                         form.review.data):
            flash('Review Posted')
            return redirect(url_for('index.index'))
    return render_template('review_form.html', title='AddAReview', form=form)
