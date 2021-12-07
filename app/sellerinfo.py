from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l

from .models.base_model import User


from flask import Blueprint
bp = Blueprint('sellerinfo/<int:id>', __name__)

@bp.route('/sellerinfo', methods=['GET', 'POST'])
def sellerinfo(id):
    return render_template('sellerinfo.html', id=id)
