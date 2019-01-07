import secrets
from PIL import Image
import os
from flask import render_template, url_for, flash, redirect, request
from gameapp import app, bcrypt, mail
from gameapp.forms import (RegistrationForm, LoginForm, UpdateAccount, RequestResetForm, ResetPasswordForm,
                           WonderForm, GameForm)
from gameapp.models import *
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/sessions")
def sessions():
    return render_template('sessions.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for { form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You have been successfully logged out', 'success')
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for('static', filename='profile_pics/' + current_user.img_file)
    return render_template('account.html', title='Account', img_file=img_file, form=form)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='tabletopscore@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this email and no changes will be made.
'''
    mail.send(msg)



@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Rest Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated, You are now able to log in!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/wonder/new", methods=['GET', 'POST'])
@login_required
def new_wonder():
    form = WonderForm()
    if form.validate_on_submit():
        wonder = Wonder(wonder_name=form.wonder.data)
        db.session.add(wonder)
        db.session.commit()
        flash('A New Wonder Has Been Created', 'success')
        return redirect(url_for('home'))
    return render_template('create_wonder.html', title='New Wonder', form=form)


@app.route("/wonder")
@login_required
def wonders():
    wonder = Wonder.query.all()
    return render_template('wonders.html', title='Wonders', wonders=wonder)


def save_game_picture(game_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(game_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/game_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(game_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/game/new", methods=['GET', 'POST'])
@login_required
def new_game():
    img = ''
    form = GameForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_game_picture(form.picture.data)
            img = picture_file
        game = Game(gamename=form.game_name.data, minplayers=form.minplayers.data, maxplayers=form.maxplayers.data,
                    description=form.description.data, publisher=form.publisher.data, img_file=img)
        db.session.add(game)
        db.session.commit()
        flash('This Game Has Been Added', 'success')
        return redirect(url_for('show_games'))
    img_file = url_for('static', filename='game_pics/' + img)
    return render_template('create_game.html', title='Add New Game', form=form, img_file=img_file)


@app.route("/game")
def show_games():
    game = Game.query.all()
    return render_template('games.html', title='Games', games=game)
