import uuid
from datetime import datetime

from manage import db


class Post(db.Model):
    __tablename__ = 'posts'

    uuid = db.Column(uuid.UUID(), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.Column(uuid.UUID(), db.ForeignKey('user.uuid'), nullable=False)
    image = db.Column(db.String(50), nullable=False, default='default.png')
    content = db.Column(db.Text, nullable=False)
