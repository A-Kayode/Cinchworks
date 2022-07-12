from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class Signup(FlaskForm):
    username= StringField(validators=[DataRequired(message="You must fill this field")])
    fname= StringField(validators=[DataRequired(message="You must fill this field")])
    lname= StringField(validators=[DataRequired(message="You must fill this field")])
    email= StringField(validators=[DataRequired(message="You must fill this field"), Email(message="Input a valid email")])
    pswd= PasswordField(validators=[DataRequired(message="You must fill this field")])
    cpswd= PasswordField(validators=[DataRequired(message="You must fill this field"), EqualTo('pswd', message="Your passwords must match")])
    submit= SubmitField("Sign Up")

class Change_password(FlaskForm):
    npswd= PasswordField()
    cnpswd= PasswordField(validators=[EqualTo('npswd', message="New passwords must match")])