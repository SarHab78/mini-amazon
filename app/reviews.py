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

class reviews(FlaskForm):
    email = StringField(_l('email'), validators=[DataRequired()])
    rating = IntegerField(_l('rating'), validators=[DataRequired()])
    pid = IntegerField(_l('rating'), validators=[DataRequired()])
    review = StringField(_l('rating'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    # def validate_email(self, email): when we have cart functionality - Jo?

@bp.route('/review_form', methods=['GET', 'POST'])
def reviews()):
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for('index.index'))
    return render_template('reviews.html', title='reviews', form=form)

