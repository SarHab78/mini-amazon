from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DecimalField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, AnyOf, NoneOf
from flask_babel import _, lazy_gettext as _l

from .models.base_model import User
from .models.base_model import Past_Order_Info


from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)



class RegistrationForm(FlaskForm):
    firstname = StringField(_l('First Name'), validators=[DataRequired(), NoneOf(values=[';','--', 'DROP', 'drop', 'Drop'])])
    lastname = StringField(_l('Last Name'), validators=[DataRequired(), NoneOf(values=[';','--', 'DROP', 'drop', 'Drop'])])
    email = StringField(_l('Email'), validators=[DataRequired(), Email(), NoneOf(values=[';','--', 'DROP', 'drop', 'Drop'])])
    address = StringField(_l('Address'), validators=[DataRequired(), NoneOf(values=[';','--', 'DROP', 'drop', 'Drop'])])
    balance = IntegerField(_l('Balance'), validators=[DataRequired()])
    is_seller = StringField(_l('Are you a Seller?'), validators=[DataRequired(), AnyOf(values=['Y','N'])])
    password = PasswordField(_l('Password'), validators=[DataRequired(), NoneOf(values=[';','--', 'DROP', 'drop', 'Drop'])])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError(_('Already a user with this email.'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data,
                         form.balance.data,
                         form.is_seller.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


class SortForm(FlaskForm):
    sort_attribute = SelectField(_l('Sort By'), choices=[('name','name'),('price','price'),('category','category')], validators=[DataRequired()])
    up_or_down = SelectField(_l('Sort By'), validators=[DataRequired()], choices=[('high-to-low','high-to-low'),('low-to-high','low-to-high')])
    submit = SubmitField('Sort')

class FilterForm(FlaskForm):
    # get all amazon categories list by reading the amazon_categories.csv file
    filter_fields = SelectMultipleField(_l('Filter By Category'), validators=[DataRequired()], choices=[('Automotive & Powersports', 'Automotive & Powersports'),
                            ('Baby Products', 'Baby Products'),
                            ('Books', 'Books'),
                            ('Camera & Photo', 'Camera & Photo'),
                            ('Cell Phones & Accessories', 'Cell Phones & Accessories'),
                            ('Clothing', 'Clothing'),
                            ('Consumer Electronics', 'Consumer Electronics'),
                            ('Entertainment Collectibles', 'Entertainment Collectibles'),
                            ('Fine Art', 'Fine Art'),
                            ('Grocery & Gourmet Foods', 'Grocery & Gourmet Foods'),
                            ('Health & Personal Care', 'Health & Personal Care'),
                            ('Home & Garden', 'Home & Garden'),
                            ('Independent Design', 'Independent Design'),
                            ('Industrial & Scientific', 'Industrial & Scientific'),
                            ('Major Appliances', 'Major Appliances'),
                            ('Misc', 'Misc'),
                            ('Music and DVD', 'Music and DVD'),
                            ('Musical Instruments', 'Musical Instruments'),
                            ('Office Products', 'Office Products'),
                            ('Outdoors', 'Outdoors'),
                            ('Personal Computers', 'Personal Computers'),
                            ('Pet Supplies', 'Pet Supplies'),
                            ('Software', 'Software'),
                            ('Sports', 'Sports'),
                            ('Sports Collectibles', 'Sports Collectibles'),
                            ('Tools & Home Improvement', 'Tools & Home Improvement'),
                            ('Toys & Games', 'Toys & Games'),
                            ('Video DVD & Blu-ray', 'Video DVD & Blu-ray'),
                            ('Video Games', 'Video Games'),
                            ('Watches', 'Watches')])
    submit = SubmitField('Filter by Category')

@bp.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    sortform = SortForm()
    filterform = FilterForm()
    ordered = Past_Order_Info.get_user_orders(uid=id)

    if sortform.validate_on_submit():
        order_by = sortform.sort_attribute.data
        session['order_by'] = order_by
        direc = sortform.up_or_down.data
        session['direc'] = direc

        search_str = ''
        filter_fields = 'all'
        if 'current_query' in session:
            search_str = session['current_query']
        if 'filter_fields' in session:
            filter_fields = session['filter_fields']
        searched_products = Past_Order_Info.past_order_search(search_str=search_str, order_by=order_by, direc=direc, filt_list = filter_fields)

        return render_template('profile.html',ordered=ordered, id=id)

    #elif filterform.validate_on_submit():
    else:
        search_str = ''
        if 'current_query' in session:
            search_str = session['current_query']
        order_by = 'price'
        if 'order_by' in session:
            order_by = session['order_by']
        direc = 'high-to-low'
        if 'direc' in session:
            direc = session['direc']

        filter_fields = tuple(filterform.filter_fields.data)
        #print(filter_fields)
        session['filter_fields'] = filter_fields
        searched_products = Past_Order_Info.past_order_search(search_str=search_str, order_by=order_by, direc=direc, filt_list = filter_fields)

        # If user is signed in, get all their purchases

        return render_template('profile.html',ordered=ordered, id=id)

    # else:
    #     if request.method == "POST":

    #         # Try adding this request.form.get line to differentiate between the two buttons
    #         if request.form.get("product_query"):
    #             product_query = request.form['product_query']
    #             session['current_query'] = product_query

    #             if product_query.lower() == "all":
    #                  searched_products = Prod_Sell_Rev_Cat.get_all()
    #                  session['current_query'] = ''
    #             else:
    #                 searched_products = Prod_Sell_Rev_Cat.get_search_result(search_str=product_query)
                
    #             if current_user.is_authenticated:
    #                 user = current_user.id
    #                 purchases = Purchase.get_all_by_uid_since(
    #                     current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    #             else:
    #                 user = None
    #                 purchases = None

    #             return render_template('profile.html',ordered=ordered, id=id)


class EditProfileForm(FlaskForm):
    
    firstname = StringField(_l('First Name'), validators=[DataRequired(), NoneOf(values=[';','--', 'DROP', 'drop', 'Drop'])])
    lastname = StringField(_l('Last Name'), validators=[DataRequired(), NoneOf(values=[';','--', 'DROP', 'drop', 'Drop'])])
    email = StringField(_l('Email'), validators=[DataRequired(), Email(), NoneOf(values=[';','--', 'DROP', 'drop', 'Drop'])])
    address = StringField(_l('Address'), validators=[DataRequired(), NoneOf(values=[';','--', 'DROP', 'drop', 'Drop'])])
    balance = DecimalField(_l('Balance'), validators=[DataRequired()], places=2)
    is_seller = StringField(_l('Are you a Seller?', validators=[DataRequired(), AnyOf(values=['Y','N'], message=('Must indicate Y for yes seller or N for not seller'))]))
    password = PasswordField(_l('Password'), validators=[DataRequired(), NoneOf(values=[';','--', 'DROP', 'drop', 'Drop'])])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('Update Profile')

@bp.route('/editprofile/<int:id>', methods=['GET', 'POST'])
def editprofile(id):
    form = EditProfileForm()
    if form.validate_on_submit():
        if User.edit(
                        current_user.id,
                        form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data,
                         form.address.data,
                         form.balance.data,
                         form.is_seller.data):
    
            return render_template("profile.html") 
    return render_template("edit.html", form=form, id=id)

class EditFirstnameForm(FlaskForm):
    id = IntegerField(_l('id'), validators=[DataRequired()])
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    submit = SubmitField('Update First Name')

@bp.route('/editfirstname/<int:id>', methods=['GET', 'POST'])

def editfirstname(id):
    print ('start')
    form = EditFirstnameForm()
    if form.validate_on_submit():
        if User.edit_firstname(
                        form.id.data,
                         form.firstname.data):
            print ('if two')
            flash('First name has been updated!')
            return render_template("profile.html") 
    return render_template("editfirstname.html", form=form, id=id)

class EditBalanceForm(FlaskForm):
    
    balance = DecimalField(_l('New Balance'), validators=[DataRequired()], places=2)
    submit = SubmitField('Update Balance')

@bp.route('/editbalance/<int:id>', methods=['GET', 'POST'])
def editbalance(id):
    
    form = EditBalanceForm()
    if form.validate_on_submit():
        if User.edit_balance(
                        current_user.id,
                         form.balance.data):
           
           
            return render_template("profile.html") 
    return render_template("editbalance.html", form=form, id=id)

