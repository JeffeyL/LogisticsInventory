from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField("username", 
                            validators=[DataRequired(), Length(min=5, max=20)])

    password = PasswordField("password", validators=[DataRequired()])

    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])

    remember = BooleanField("Remember Me")
    
    submit = SubmitField('Sign in')

class CreateItemForm(FlaskForm):
    id = StringField("id", validators=[DataRequired()])

    name = StringField("name", validators=[DataRequired()])

    qty = StringField("quantity", validators=[DataRequired()])

    submit = SubmitField("Create")

class UpdateItemForm(FlaskForm):
    id = StringField("new id")

    name = StringField("new name")

    qty = StringField("new quantity")

    submit = SubmitField("Update")

class DeleteItemForm(FlaskForm):
    message = TextAreaField("Delete message", validators=[DataRequired()])

    submit = SubmitField("Delete")

class GetUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=20)])

    submit = SubmitField("Login")