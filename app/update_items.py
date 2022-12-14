from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import Length, ValidationError, DataRequired, EqualTo, InputRequired, NumberRange, NoneOf
from flask_babel import _, lazy_gettext as _l

from .models.base_model import User, Add_Product, Product


from flask import Blueprint
bp = Blueprint('update_items', __name__)

class UpdateProductForm(FlaskForm):
   #only enter product ID with hardcoded falues to prevent sql injection attacks
    product_id = IntegerField(_l('Product ID'), validators=[DataRequired(), NoneOf(values=[';','--', 'DROP', 'drop', 'Drop'])])
    quantity = IntegerField(_l('Quantity'), validators=[DataRequired(), NumberRange(min=1, message="Invalid range"), NoneOf(values=[';','--', 'DROP', 'drop', 'Drop'])])
    available = StringField(_l('Available'), validators=[DataRequired(), Length(min = 1, max = 1, message = "Ensure Y or N"), NoneOf(values=[';','--', 'DROP', 'drop', 'Drop'])])
    #available = SelectField('Is this product available?', [ InputRequired()],
    #    choices=[ (''), ('Y'),
    #    ('N') ])
    submit = SubmitField(_l('Submit Product'))

    #write a function to see if the product already exists so it can be updated
    def can_update(self, product_id):
        if Product.product_can_be_updated(product_id):
            return True
        else: 
            return False
  


@bp.route('/updateItems', methods =['GET', 'POST'])
def update_items():
    if current_user.is_authenticated:
        sell_id = current_user.id
       
    else:
          flash('Please log in')
          sell_id = -1
    can_sell = User.can_sell(sell_id)

    form = UpdateProductForm()
    #get the form values and pass into function
    if form.validate_on_submit():
        if form.can_update(form.product_id.data) is True:
           
            product_id = request.form['product_id']
            print(product_id)
            quantity = request.form['quantity']
            print(quantity)
            available = request.form['available']
            print(available)
            Add_Product.update_product(product_id, 
                                        sell_id, 
                                        quantity,
                                        available)
            
        return redirect(url_for('seller_inventory.inventory'))
    else: 
        return render_template('update_items.html', title='Update Items', form=form, poss_seller = can_sell)
   




