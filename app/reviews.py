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
from .models.base_model import Add_review


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
    else: return redirect(url_for('users.login'))
    
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

    #validate reviewer
   # def validate_review(self, pid, uid):
    #    if Product.product_exists(product_name, current_user.id):
     #       #raise ValidationError(_('Already a product with this name. Update its quantity instead'))
      #      return True
       # else: 
        #    return False
    #actually submit form
    
    if form.validate_on_submit():
                rid = request.form['rid']
                print(rid)
                uid = request.form['uid']
                print(uid)
                pid = request.form['pid']
                print(pid)
                email = request.form['email']
                print(email)
                timestamp = request.form['timestamp']
                print(timestamp)
                rating = request.form['rating']
                print(rating)
                review = request.form['review']
                print(review)
                Add_review.add_review(rid,
                            uid,
                            pid,
                            email,
                            timestamp,
                            rating,
                            review)
                flash('thanks for submitting your review!')
                return redirect(url_for('index.index'))
    return render_template('review_form.html', title='reviews', form=form)
