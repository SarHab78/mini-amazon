from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.base_model import User


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
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    address = StringField(_l('Address'), validators=[DataRequired()])
    balance = IntegerField(_l('Balance'), validators=[DataRequired()])
    is_seller = StringField(_l('Seller?'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
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

@bp.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile(id):
    return render_template('profile.html', id=id)

class EditProfileForm(FlaskForm):
    
    firstname = StringField(_l('First Name'), validators=[DataRequired()])
    lastname = StringField(_l('Last Name'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    address = StringField(_l('Address'), validators=[DataRequired()])
    balance = IntegerField(_l('Balance'), validators=[DataRequired()])
    is_seller = StringField(_l('Seller?'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
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
    id = IntegerField(_l('id'), validators=[DataRequired()])
    balance = IntegerField(_l('balance'), validators=[DataRequired()])
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

