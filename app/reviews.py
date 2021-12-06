#forms and path
#write a review
#edit
#add in access restriction to only those who have purchased

from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, EqualTo, InputRequired, NumberRange
from flask_babel import _, lazy_gettext as _l
import datetime 
import time
import uuid
from wtforms.fields import DateTimeField

from .models.base_model import Product_review
from .models.base_model import User
from .models.base_model import Product
from .models.base_model import Add_review


from flask import Blueprint
bp = Blueprint('reviews', __name__)

class reviews(FlaskForm):
    rid = StringField(_l('rid'), validators=[DataRequired()])
    pid = IntegerField(_l('pid'), validators=[DataRequired()])
    uid = IntegerField(_l('uid'), validators=[DataRequired()])
    email = StringField(_l('email'), validators=[DataRequired()])
    #rev_timestamp = DateTimeField(_l('rev_timestamp'), validators=[DataRequired()])
    rating = IntegerField(_l('rating'), validators=[DataRequired(), NumberRange(min=1, max = 5, message="Invalid range")])
    review = StringField(_l('review'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))
    # def validate_email(self, email): when we have cart functionality?

    #validate review 
    #def validate_review(self, pid):
     #   if Product_review.review_exists(pid, current_user.id):
      #      return True
       # else: 
        #    return False

@bp.route('/<product_id>/review_form', methods=['GET', 'POST'])
def add_a_review(product_id):
    form = reviews()
    #autopopulate with user id:
    if current_user.is_authenticated: 
        my_user = current_user.id
        form.uid.data = my_user
    else: return redirect(url_for('users.login'))
    
    #autopopulate timestamp
    #ct = datetime.datetime.now()
    #form.rev_timestamp.data = ct
    #print(type(ct))

    #autogenerate review id here? -- needs to be unique?, don't know if this is actually a valid way of doing it but o well
    gen_rid = uuid.uuid4()
    form.rid.data = gen_rid
    
    #autopopulate product id:
    page_product = Product.get_product_for_page(product_id = product_id)
    if request.method == 'GET':
        form.pid.data = page_product[0].product_id


    #actually submit form
    
    if form.validate_on_submit():
        #print(form.validate_review(form.pid.data))
        #if form.validate_review(form.pid.data) is False:

                rid = request.form['rid']
                print(rid)
                pid = request.form['pid']
                print(pid)
                uid = request.form['uid']
                print(uid)
                print(type(uid))
                email = request.form['email']
                print(email)
                #rev_timestamp = request.form['rev_timestamp']
                #print(rev_timestamp)
                #print(type(rev_timestamp))
                rating = request.form['rating']
                print(rating)
                review = request.form['review']
                print(review)
                Add_review.add_review(rid,
                            pid,
                            uid,
                            email,
                            #rev_timestamp,
                            rating,
                            review)
                #print('review submitted')
                flash('thanks for submitting your review!')
                return redirect(url_for('users_review_page.myreviews'))
    return render_template('review_form.html', title='reviews', form=form)


@bp.route('/editreview/<int:id>', methods=['GET', 'POST'])
def editreview(id):
    form = EditReviewForm()
    if form.validate_on_submit():
                rid = request.form['rid']
                print(rid)
                pid = request.form['pid']
                print(pid)
                uid = request.form['uid']
                print(uid)
                print(type(uid))
                email = request.form['email']
                print(email)
                #rev_timestamp = request.form['rev_timestamp']
                #print(rev_timestamp)
                rating = request.form['rating']
                print(rating)
                review = request.form['review']
                print(review)
                Add_review.edit_review(rid,
                            pid,
                            uid,
                            email,
                            rev_timestamp,
                            rating,
                            review)
                flash('thanks for editing your review!')
                return redirect(url_for('users_review_page.myreviews'))
    return render_template('review_form.html', title='reviews', form=form)