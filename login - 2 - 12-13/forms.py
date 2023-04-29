from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField, EmailField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = EmailField('Login / email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    r_password = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    login = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class JobForm(FlaskForm):
    team_leader = IntegerField("Team leader ID", validators=[DataRequired()])
    job = StringField('Job title', validators=[DataRequired()])
    work_size = IntegerField('Work size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    hazard = StringField('Hazard level', validators=[DataRequired()])
    is_finished = BooleanField('Is it finished?')
    submit = SubmitField('Add job')


class DepartmentForm(FlaskForm):
    chief = IntegerField("Chief ID", validators=[DataRequired()])
    title = StringField('Department title', validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Add job')
