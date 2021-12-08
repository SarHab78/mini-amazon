from flask import session, render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, NumberRange
from flask_babel import _, lazy_gettext as _l

from .models.base_model import Product
from .models.base_model import Purchase
from .models.base_model import Product_review
from .models.base_model import Prod_Sell_Rev_Cat
from .models.base_model import Orders
from .models.base_model import User
from .models.base_model import Prod_Sell_Rev_Cat_Ord



from flask import Blueprint
bp = Blueprint('checkout', __name__)

# class Checkoutform(FlaskForm):
#     add_date2 = StringField(_l('add_date2'), validators=[DataRequired()])
#     submit = SubmitField('Checkout')


@bp.route('/checkout')# , methods=['GET','POST'])
def checkout():
    my_cart = Prod_Sell_Rev_Cat_Ord.get_cart(current_user.id)

    sellers_amounts_dict = Prod_Sell_Rev_Cat_Ord.get_sellers_and_incs(my_cart)
    buyers_amounts_dict = Prod_Sell_Rev_Cat_Ord.get_buyers_and_decs(my_cart)
    products_amounts_dict = Prod_Sell_Rev_Cat_Ord.get_products_and_decs(my_cart)

    print(sellers_amounts_dict)
    print(buyers_amounts_dict)
    print(products_amounts_dict)

    checking_out = Prod_Sell_Rev_Cat_Ord.checkout_cart(uid=current_user.id, sellers_amounts_dict = sellers_amounts_dict, buyers_amounts_dict = buyers_amounts_dict, products_amounts_dict = products_amounts_dict)
    # form1 = Checkoutform()
    # my_cart = Order.get_cart(current_user.id)
    # balance = current_user.balance
    # price = Order.total_price(current_user.id)
    # time = datetime.datetime.now()
    # form.add_date2.data = time

    # if form.validate_on_submit():
    #     print('made it')
    #     add_date2 = request.form['add_date2']
    # else:        
    #     print('not submitted')
    #     flash('Error, please try again later')
    return render_template('checkout.html', 
    checking_out=checking_out)



# @bp.route('/final_checkout')
# def final_checkout():
    
#     if form.validate_on_submit():
#         if balance < total:
#             flash('Insufficient Funds, you current have a balance of ${}, your cart total is ${}', balance, total)
#         else:
#             return Order.checkout_cart(balance = balance, uid = current_user.id)
#     if form.is_submitted() and not form.validate():

#         return render_template('finalized_order.html')
