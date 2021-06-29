import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_serializer import SerializerMixin

from services import db


class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'), nullable=False)
    image = db.Column(db.String(50), nullable=False, default='default.png')
    content = db.Column(db.Text, nullable=False)
