from flask import render_template
from flask_login import current_user
import datetime

from .models.base_model import Product
from .models.base_model import Purchase


from flask import Blueprint
bp = Blueprint('index', __name__)






