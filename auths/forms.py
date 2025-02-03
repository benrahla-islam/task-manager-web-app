from flask_wtf import FlaskForm
from wtforms import StringField , EmailField , PasswordField , SubmitField , BooleanField , TextAreaField , HiddenField
from wtforms.validators import DataRequired ,InputRequired , Email 

class SigninForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[Email() , DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    terms = BooleanField('Accept Terms', validators=[InputRequired()])
    signup = SubmitField('signup')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Email() , DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('login')

class CreateTaskForm(FlaskForm):
    id = HiddenField()
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    create_submit = SubmitField('Save')


class UpdateTaskForm(FlaskForm):
    id = HiddenField()
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    update_submit = SubmitField('Save')

class DeleteTaskForm(FlaskForm):
    id = HiddenField()
    delete_submit = SubmitField()