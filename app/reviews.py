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

from .models.base_model import User


from flask import Blueprint
bp = Blueprint('users', __name__)


class ReviewForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    pid = IntegerField(_l('Product ID'), validators=[DataRequired()])
    rev = StringField(_l('Review'), validators=[DataRequired()])
    rating = IntegerField(_l('Rating'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.pid.data,
                         form.rev.data,
                         form.rating.data
        ):
            flash('Congratulations, you submitted a review!')
            return redirect(url_for('users.login'))
    return render_template('review_form.html', title='review_form', form=form)
