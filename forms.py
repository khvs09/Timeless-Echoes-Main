from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length, Optional, URL, Regexp
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=64, message='Username must be between 3 and 64 characters'),
        Regexp('^[A-Za-z0-9_.]+$', message='Username can only contain letters, numbers, dots and underscores')
    ])
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address')])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already taken. Please use a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is already registered. Please use a different one or login.')

class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=5, max=100, message='Title must be between 5 and 100 characters')
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(min=10, message='Description must be at least 10 characters')
    ])
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only! Supported formats: JPG, PNG, JPEG, GIF')
    ])
    state = StringField('State', validators=[DataRequired()])
    district = StringField('District', validators=[DataRequired()])
    village = StringField('Village', validators=[DataRequired()])
    address = StringField('Address (Optional)', validators=[Optional()])
    
    # Map-related fields
    location_search = StringField('Search Location')
    latitude = HiddenField('Latitude', validators=[Optional()])
    longitude = HiddenField('Longitude', validators=[Optional()])
    
    submit = SubmitField('Submit')
    
    def validate_latitude(self, latitude):
        """Validate latitude is within valid range"""
        if latitude.data:
            try:
                lat_value = float(latitude.data)
                if lat_value < -90 or lat_value > 90:
                    raise ValidationError('Latitude must be between -90 and 90 degrees')
            except ValueError:
                raise ValidationError('Please provide a valid decimal number for latitude')
                
    def validate_longitude(self, longitude):
        """Validate longitude is within valid range"""
        if longitude.data:
            try:
                lng_value = float(longitude.data)
                if lng_value < -180 or lng_value > 180:
                    raise ValidationError('Longitude must be between -180 and 180 degrees')
            except ValueError:
                raise ValidationError('Please provide a valid decimal number for longitude')

class CommentForm(FlaskForm):
    body = TextAreaField('Comment', validators=[
        DataRequired(),
        Length(min=1, max=500, message='Comment must be between 1 and 500 characters')
    ])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Change Password')

class DeleteAccountForm(FlaskForm):
    confirmation = PasswordField('Enter your password to confirm account deletion', 
                               validators=[DataRequired()])
    submit = SubmitField('Delete Account')