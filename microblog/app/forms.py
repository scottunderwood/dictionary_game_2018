from flask_wtf import FlaskForm
# imports specific form fields from flask_wtf that are then used below in the creation of forms
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
# imports specific form validation tools that are then applied to forms below
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

# example of a form being created as a copy of the FlaskForm class
# form fields / buttons are created as variables which have a type,
# a name, and potentially a validaton rule


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[
                              DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    # Introduces logic to prevent a non-unique username error on the edit profile form
    # No will prevent submit and issue an error notification if user attempts to change user name to one that already exists

    # Establishes the active users username as original_username when loading the EditProfileForm
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    # Checks if the username submitted through EditProfileForm equals original_username
    # If not euqal querys the User db table to see if the name exists and raises a ValidationError if True
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


# Creates a new form class for users to submit new posts
class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[
                         DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')


# Initial attempt at creating a basic game form that makes you ener your name and then press a button to start the game script
class GameForm(FlaskForm):
    player_name = TextAreaField('Player Name', validators=[
                                DataRequired(), Length(min=1, max=24)])
    start_game = SubmitField('Start Game!')
