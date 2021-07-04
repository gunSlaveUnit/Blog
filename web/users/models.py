import uuid

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer import SerializerMixin

from services import db, login_manager
from config import Config


@login_manager.user_loader
def load_user(user_uuid):
    return User.query.get(user_uuid)


class User(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-posts.author.posts',)

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

    def get_reset_token(self, expires_sec=30*60):
        s = Serializer(Config.SECRET_KEY, expires_sec)
        return s.dumps({'user_uuid': self.uuid}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            user_uuid = s.loads(token)['user_uuid']
        except:
            return None
        return User.query.get(user_uuid)
