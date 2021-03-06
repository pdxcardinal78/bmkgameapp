from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from gameapp.models import User, Wonder, Game, Scores
from flask_login import current_user
from wtforms.fields.html5 import DateField


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


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class WonderForm(FlaskForm):
    wonder = StringField('Wonder Name', validators=[DataRequired()])
    submit = SubmitField('Create')

    def validate_wonder(self, wonder):
        wonder = Wonder.query.filter_by(wonder_name=wonder.data).first()
        if wonder:
            raise ValidationError('Wonder already in database.')


def game_query():
    return Game.query


class SessionForm(FlaskForm):
    choices = [('0', 'Enter Players'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')]
    dateplayed = DateField('Date Played', format='%Y-%m-%d', validators=[DataRequired()])
    game_played = QuerySelectField(query_factory=game_query, allow_blank=True, blank_text='Select Game', get_label='gamename', validators=[DataRequired()])
    players = SelectField('Number of Players', choices=choices, coerce=int)
    submit = SubmitField('Create Session')


class GameForm(FlaskForm):
    game_name = StringField('Game Name', validators=[DataRequired()])
    minplayers = IntegerField('Min Players', validators=[DataRequired()])
    maxplayers = IntegerField('Max Players', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    game_picture = FileField('Game Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save Game')

    def validate_game_name(self, game_name):
        game_name = Game.query.filter_by(gamename=game_name.data).first()
        if game_name:
            raise ValidationError('Game Already Exists')


class GameUpdateForm(FlaskForm):
    game_name = StringField('Game Name', validators=[DataRequired()])
    minplayers = IntegerField('Min Players', validators=[DataRequired()])
    maxplayers = IntegerField('Max Players', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    game_picture = FileField('Game Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save Game')

    def validate_game_name(self, game_name):
        if game_name.data != 1:
            game_name = Game.query.filter_by(gamename=game_name.data).first()
            if game_name:
                raise ValidationError('Game Already Exists')


def WonderQuery():
    return Wonder.query


def PlayerQuery():
    return User.query


class ScoresForm(FlaskForm):
    player = QuerySelectField(query_factory=PlayerQuery, allow_blank=True, blank_text='Select Player', get_label='username')
    total_score = IntegerField('Total', validators=[DataRequired()])
    wonder = QuerySelectField(query_factory=WonderQuery, allow_blank=True, blank_text='Select Wonder', get_label='wonder_name')
    wonder_side = SelectField('Wonder Side', choices=[('A', 'A'), ('B', 'B')])
    war_score = IntegerField('War Score')
    gold_score = IntegerField('Gold Score')
    blue_score = IntegerField('Civic Score')
    yellow_score = IntegerField('Commerce Score')
    science_score = IntegerField('Science Score')
    purple_score = IntegerField('Guild Score')
    armada_score = IntegerField('Armada Score')
    leader_city_score = IntegerField('Leader/Cities Score')
    submit = SubmitField('Save Scores')


