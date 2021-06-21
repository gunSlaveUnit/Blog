import uuid

from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID

from manage import db, login_manager


@login_manager.user_loader
def load_user(user_uuid):
    return User.query.get(user_uuid)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.String(50), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return self.uuid
