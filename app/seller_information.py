from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.base_model import User


from flask import Blueprint
bp = Blueprint('seller_information', __name__)

@bp.route('/sellerinformation>', methods=['GET', 'POST'])
def seller_information():
    return render_template('seller_information.html')
