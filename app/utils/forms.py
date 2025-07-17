from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, IntegerField, SubmitField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User
from flask_wtf.file import FileField


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    graduation_year = IntegerField('Graduation Year')
    degree = StringField('Degree Program')
    current_job_title = StringField('Current Job Title')
    location = StringField('Location')
    bio = TextAreaField('Bio')
    profile_image = FileField('Profile Image')
    submit = SubmitField('CREATE ACCOUNT')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('LOGIN')
        
class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Reset Password')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    graduation_year = IntegerField('Graduation Year')
    degree = StringField('Degree Program')
    current_job_title = StringField('Current Job Title')
    location = StringField('Location')
    bio = TextAreaField('Bio')
    profile_image = FileField('Profile Image')

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Message')

class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    requirements = TextAreaField('Requirements')
    location = StringField('Location')
    job_type = SelectField('Job Type', choices=[
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('internship', 'Internship'),
        ('contract', 'Contract')
    ], validators=[DataRequired()])
    salary_range = StringField('Salary Range')
    application_url = StringField('Application URL')
    contact_email = StringField('Contact Email', validators=[Email()])
    deadline = DateTimeField('Application Deadline', format='%Y-%m-%d')

class RSVPForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    status = SelectField('Status', choices=[('attending', 'Attending'), ('not_attending', 'Not Attending'), ('maybe', 'Maybe')], validators=[DataRequired()])
    submit = SubmitField('Submit RSVP')
    
class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    event_date = DateTimeField('Event Date', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    venue = StringField('Venue', validators=[DataRequired()])
    max_attendees = IntegerField('Max Attendees')
    event_image = FileField('Event Image')
    submit = SubmitField('Create Event')
    
class TestimonialForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Your Experience', validators=[DataRequired(), Length(min=50)])
    rating = IntegerField('Rating (1-5)', validators=[DataRequired()])
    

