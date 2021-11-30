#forms and path
#write a review
#edit
#add in access restriction to only those who have purchased

from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.base_model import Product_review
from .models.base_model import User


from flask import Blueprint
bp = Blueprint('reviews', __name__)

class reviews(FlaskForm):
    rid = IntegerField(_l('rid'), validators=[DataRequired()])
    email = StringField(_l('email'), validators=[DataRequired()])
    rating = IntegerField(_l('rating'), validators=[DataRequired()])
    pid = IntegerField(_l('pid'), validators=[DataRequired()])
    review = StringField(_l('review'), validators=[DataRequired()])
    uid = IntegerField(_l('uid'), validators=[DataRequired()])
    timestamp = StringField(_l('timestamp'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    # def validate_email(self, email): when we have cart functionality?

@bp.route('/review_form', methods=['GET', 'POST'])
def add_review():
    form = reviews()
    #if current_user.is_authenticated: #import addtl things?
    my_user = User.get(id) #fix these lines - but attempting to autopopulate uid
    #i still don't know how to access uid - may not work until login working
    if request.method == 'GET':
        form.uid.data = my_user.id
    if form.validate_on_submit():
        if Product_review.add_review(
            form.rid.data,
            form.uid.data,
            form.pid.data,
            form.rating.data,
            form.review.data,
            form.email.data,
            form.timestamp.data):
            
            flash("thanks for submitting your review!")
            return redirect(url_for('product_page.product_page')) ##product_page.<product> maybe
    return render_template('review_form.html', title='reviews', form=form)



