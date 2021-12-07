from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, EqualTo, InputRequired, NumberRange
from flask_babel import _, lazy_gettext as _l
import datetime 
import uuid

from .models.base_model import User
from .models.base_model import Product
from .models.base_model import Add_seller_review
from .models.base_model import Prod_Sell_Rev_Cat
from .models.base_model import Seller_review


from flask import Blueprint
bp = Blueprint('seller_reviews', __name__)

class seller_reviews(FlaskForm):
    rid = StringField(_l('rid'), validators=[DataRequired()])
    uid = IntegerField(_l('uid'), validators=[DataRequired()])
    sid = IntegerField(_l('sid'), validators=[DataRequired()])
    email = StringField(_l('email'), validators=[DataRequired()])
    #rev_timestamp = StringField(_l('rev_timestamp'), validators=[DataRequired()])
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

@bp.route('/<pid>/<sid>/seller_review_form', methods=['GET', 'POST'])
def add_a_seller_review(pid, sid):
    form = seller_reviews()
    #autopopulate with user id:
    if current_user.is_authenticated: 
        my_user = current_user.id
        form.uid.data = my_user
    else: return redirect(url_for('users.login'))

    #autogenerate review id here? -- needs to be unique?, don't know if this is actually a valid way of doing it but o well
    gen_rid = uuid.uuid4()
    form.rid.data = gen_rid
    
    #autopopulate seller id: -- FIX THIS
    page_product = Prod_Sell_Rev_Cat.get_sell_rev_info(product_id = pid)
    if request.method == 'GET':
        form.sid.data = page_product[0].id


    #actually submit form
    
    if form.validate_on_submit():
        #print(form.validate_review(form.pid.data))
        #if form.validate_review(form.pid.data) is False:

                rid = request.form['rid']
                print(rid)
                uid = request.form['uid']
                print(uid)
                sid = request.form['sid']
                print(sid)
                email = request.form['email']
                print(email)
                #rev_timestamp = request.form['rev_timestamp']
                #print(rev_timestamp)
                rating = request.form['rating']
                print(rating)
                review = request.form['review']
                print(review)
                #eller_review.stest()
                Seller_review.add_seller_review(rid,
                            uid,
                            sid,
                            email,
                            #rev_timestamp,
                            rating,
                            review)
                flash('thanks for submitting your review!')
                return redirect(url_for('index.index'))
    return render_template('seller_review_form.html', title='reviews', form=form, sid=sid)



class EditReviewForm(FlaskForm):
    rid = StringField(_l('rid'), validators=[DataRequired()])
    sid = IntegerField(_l('sid'), validators=[DataRequired()])
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
@bp.route('/editsellerreview/<id>', methods=['GET', 'POST'])
def editreview(id):
    #id = id
    form = EditReviewForm()
    obj = Seller_review.get(id)
    print(obj)
    rid = obj[0].rid
    uid = obj[0].uid
    sid = obj[0].sid
    email = current_user.email
    rating = obj[0].rating
    review = obj[0].review
    if form.validate_on_submit():
                rid = request.form['rid']
                print(rid)
                uid = request.form['uid']
                print(uid)
                sid = request.form['sid']
                print(sid)
                #print(type(uid))
                email = request.form['email']
                print(email)
                #rev_timestamp = request.form['rev_timestamp']
                #print(rev_timestamp)
                rating = request.form['rating']
                print(rating)
                review = request.form['review']
                print(review)
                Seller_review.edit(rid,
                            uid,
                            sid,
                            email,
                            #rev_timestamp,
                            rating,
                            review)
                flash('thanks for editing your review!')
                return redirect(url_for('users_review_page.myreviews'))
    return render_template('edit_seller_review.html', title='reviews', form=form, uid=uid, sid=sid, email=email, rid=rid, rating=rating, review=review)


@bp.route('/<rid>/delete_seller_review', methods=['GET', 'POST'])
def delete_this_review(rid):
    obj = Seller_review.get(rid)
    rid = obj[0].rid
    #print(rid)
    Seller_review.delete(rid)
    newobj = Seller_review.get_users_reviews(current_user.id)
    return redirect(url_for('users_review_page.myreviews'))
    #return render_template('review_deleted_confirmation.html', seller_reviews = newobj)
