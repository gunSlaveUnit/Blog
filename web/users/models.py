import uuid

from manage import db


class User(db.Model):
    __tablename__ = 'users'

    uuid = db.Column(uuid.UUID(), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.String(50), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
