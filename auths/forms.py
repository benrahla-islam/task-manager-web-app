from flask_wtf import FlaskForm
from wtforms import StringField , EmailField , PasswordField , SubmitField , BooleanField , TextAreaField , IntegerField , SelectField
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
    id = IntegerField()
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    group = SelectField('Group', coerce=int , validators=[] , choices=[] , default= None)
    create_submit = SubmitField('Save')


class UpdateTaskForm(FlaskForm):
    id = IntegerField()
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    update_submit = SubmitField('update')

class DeleteTaskForm(FlaskForm):
    id = IntegerField()
    delete_submit = SubmitField("Delete")

class DeleteGroupForm(FlaskForm):
    id = IntegerField()
    delete_submit = SubmitField("Delete")

class CreateGroupForm(FlaskForm):
    id = IntegerField()
    name = StringField('Name', validators=[DataRequired()])
    color = StringField('Color', validators=[DataRequired()])
    create_submit = SubmitField('Create')

class UpdateGroupForm(FlaskForm):
    id = IntegerField()
    name = StringField('Name', validators=[DataRequired()])
    update_submit = SubmitField('Update')

