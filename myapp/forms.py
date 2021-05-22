from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

    
class PostForm(FlaskForm):
    choices=['General', 'Python', 'DB', 'Web', 'Storage']

    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Body')
    subject = SelectField('Subject', choices=choices)
    submit = SubmitField('Post')
