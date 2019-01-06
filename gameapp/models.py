from gameapp import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    sessions = db.relationship('Session', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.img_file}')"


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gamename = db.Column(db.String(50), unique=True, nullable=False)
    minplayers = db.Column(db.Integer, nullable=False)
    maxplayers = db.Column(db.Integer, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='game.jpg')
    description = db.Column(db.String(200))
    publisher = db.Column(db.String(50))

    def __repr__(self):
        return f"Games('{self.gamename}', '{self.maxplayers}', '{self.img_file}')"


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players = db.Column(db.Integer, nullable=False)
    play_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

    def __repr__(self):
        return f"Session('{self.game_name}', '{self.play_date}', '{self.players}')"


class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seat_position = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    seven_wonder = db.Column(db.Integer, db.ForeignKey('wonder.id'))
    wonder_side = db.Column(db.String(10))
    war_score = db.Column(db.Integer)
    gold_score = db.Column(db.Integer)
    blue_score = db.Column(db.Integer)
    yellow_score = db.Column(db.Integer)
    science_score = db.Column(db.Integer)
    purple_score = db.Column(db.Integer)
    armada_score = db.Column(db.Integer)
    leader_city_score = db.Column(db.Integer)


class Wonder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wonder_name = db.Column(db.String(20), nullable=False, unique=True)
