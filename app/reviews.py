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
import datetime 
import uuid

from .models.base_model import Product_review
from .models.base_model import User
from .models.base_model import Product


from flask import Blueprint
bp = Blueprint('reviews', __name__)

class reviews(FlaskForm):
    rid = StringField(_l('rid'), validators=[DataRequired()])
    email = StringField(_l('email'), validators=[DataRequired()])
    rating = IntegerField(_l('rating'), validators=[DataRequired()])
    pid = IntegerField(_l('pid'), validators=[DataRequired()])
    review = StringField(_l('review'), validators=[DataRequired()])
    uid = IntegerField(_l('uid'), validators=[DataRequired()])
    timestamp = StringField(_l('timestamp'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    # def validate_email(self, email): when we have cart functionality?

@bp.route('/<product_id>/review_form', methods=['GET', 'POST'])
def add_review(product_id):
    form = reviews()
    #autopopulate with user id:
    if current_user.is_authenticated: 
        my_user = current_user.id
        form.uid.data = my_user
    
    #autopopulate timestamp
    ct = datetime.datetime.now()
    form.timestamp.data = ct

    #autogenerate review id here? -- needs to be unique?, don't know if this is actually a valid way of doing it but o well
    gen_rid = uuid.uuid4()
    form.rid.data = gen_rid
    
    #autopopulate product id:
    page_product = Product.get_product_for_page(product_id = product_id)
    if request.method == 'GET':
        form.pid.data = page_product[0].product_id

    if form.validate_on_submit():
        if Product_review.add_review(
            form.rid.data,
            form.uid.data,
            form.pid.data,
            form.email.data,
            form.timestamp.data,
            form.rating.data,
            form.review.data):
            
            flash('thanks for submitting your review!')
            return redirect(url_for('index.index')) ##product_page.<product> maybe
    return render_template('review_form.html', title='reviews', form=form)



