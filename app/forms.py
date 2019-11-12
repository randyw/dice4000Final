from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    #Created a select from for permission-level. 
    # This should be changed once Admins are established 
    # so registrants cannot select "Administrator" from the list.
    permission_level = SelectField('Role', choices=[
        ('0', 'Student'),
        ('1', 'Faculty'),
        ('2', 'Administrator')
    ])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CreateUserForm(FlaskForm):
    # copy/pasted RegistrationForm with generic "Submit" button

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    #Created a select from for permission-level. 
    # This should be changed once Admins are established 
    # so registrants cannot select "Administrator" from the list.
    permission_level = SelectField('Role', choices=[
        ('0', 'Student'),
        ('1', 'Faculty'),
        ('2', 'Administrator')
    ])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditUserForm(FlaskForm):
    # stripped down version of CreateUserForm
    # only allow permission_level changes

    permission_level = SelectField('Role', choices=[
        ('0', 'Student'),
        ('1', 'Faculty'),
        ('2', 'Administrator')
    ])
    submit = SubmitField('Submit')

class EditOrgForm(FlaskForm):
    name = StringField('Organization Name', validators=[DataRequired()])
    bg_check_required = BooleanField()
    description = StringField('Description')
    keywords = StringField('Keywords')
    num_volunteers = StringField('Number of Volunteers')
    mission_statement = StringField('Mission Statement')
    website = StringField('Website', validators=[DataRequired()])
    primary_contact_name = StringField('Primary Contact Name', validators=[DataRequired()])
    primary_contact_title = StringField('Primary Contact Title')
    primary_contact_email = StringField('Primary Contact Email', validators=[DataRequired()])
    primary_contact_phone = StringField('Primary Contact Phone')
    street_address = StringField('Address')
    zip_code = StringField('Zipcode', validators=[DataRequired()])
    alt_contact_name =StringField('Alternate Contact Name')
    alt_contact_email = StringField('Alternate Contact Name')
    application_url = StringField('Application URL')
    submit = SubmitField('Save')

class CreateOrgForm(FlaskForm):
    name = StringField('Organization Name', validators=[DataRequired()])
    bg_check_required = BooleanField()
    description = StringField('Description')
    keywords = StringField('Keywords')
    num_volunteers = StringField('Number of Volunteers')
    mission_statement = StringField('Mission Statement')
    website = StringField('Website', validators=[DataRequired()])
    primary_contact_name = StringField('Primary Contact Name', validators=[DataRequired()])
    primary_contact_title = StringField('Primary Contact Title')
    primary_contact_email = StringField('Primary Contact Email', validators=[DataRequired()])
    primary_contact_phone = StringField('Primary Contact Phone')
    street_address = StringField('Address')
    zip_code = StringField('Zipcode', validators=[DataRequired()])
    alt_contact_name =StringField('Alternate Contact Name')
    alt_contact_email = StringField('Alternate Contact Name')
    application_url = StringField('Application URL')
    
    # Defined fields from models, add validations
    # then this class to routes.py
    submit = SubmitField('Save')

class DeleteOrgForm(FlaskForm):
    submit = SubmitField('Delete')

class DeleteUserForm(FlaskForm):
    submit = SubmitField('Delete')