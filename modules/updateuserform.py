from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class UpdateUserForm(FlaskForm):
    id = IntegerField('User ID', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Enter')
