from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from gameapp.models import User, Wonder, Game
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The User Already Exists, please choose a different name')

    def validate_email(self, email):

        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('An account already exists with this email address.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccount(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The User Already Exists, please choose a different name')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('An account already exists with this email address.')


class WonderForm(FlaskForm):
    wonder = StringField('Wonder Name', validators=[DataRequired()])
    submit = SubmitField('Create')

    def validate_wonder(self, wonder):
        wonder = Wonder.query.filter_by(wonder_name=wonder.data).first()
        if wonder:
            raise ValidationError('Wonder already in database.')


class SessionForm(FlaskForm):
    date = DateField('Game Date', validators=[DataRequired()])
    game_played = IntegerField('Game Played', validators=[DataRequired()])
    players = IntegerField('Players', validators=[DataRequired()])
    create_session = SubmitField('Create Session')


class GameForm(FlaskForm):
    game_name = StringField('Game Name', validators=[DataRequired()])
    minplayers = IntegerField('Min Players', validators=[DataRequired()])
    maxplayers = IntegerField('Max Players', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    picture = FileField('Game Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save Game')

    def validate_gamename(self, game):
        game = Game.query.filter_by(gamename=game.data).first()
        if game:
            raise ValidationError('Game already in database.')
