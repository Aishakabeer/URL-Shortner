from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class URLForm(FlaskForm):
    url = StringField('Enter URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Shorten')