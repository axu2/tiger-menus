from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class AddFoodForm(FlaskForm):
    food = StringField('Food To Add:', validators=[Required()])
    submit = SubmitField('Submit')
