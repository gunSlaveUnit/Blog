import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf import CSRFProtect

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

db = SQLAlchemy(app)
from web.posts.models import Post
from web.users.models import User
db.create_all()
db.session.commit()
bcrypt = Bcrypt(app)
mail = Mail(app)
csrf = CSRFProtect(app)

cache = Cache()
cache_servers = os.environ.get('MEMCACHIER_SERVERS')
if cache_servers is None:
    cache.init_app(app, config={'CACHE_TYPE': 'simple'})
else:
    cache_user = os.environ.get('MEMCACHIER_USERNAME') or ''
    cache_pass = os.environ.get('MEMCACHIER_PASSWORD') or ''
    cache.init_app(app,
                   config={'CACHE_TYPE': 'saslmemcached',
                           'CACHE_MEMCACHED_SERVERS': cache_servers.split(','),
                           'CACHE_MEMCACHED_USERNAME': cache_user,
                           'CACHE_MEMCACHED_PASSWORD': cache_pass,
                           'CACHE_OPTIONS': {'behaviors': {
                               'tcp_nodelay': True,
                               'tcp_keepalive': True,
                               'connect_timeout': 2000,
                               'send_timeout': 750 * 1000,
                               'receive_timeout': 750 * 1000,
                               '_poll_timeout': 2000,
                               'ketama': True,
                               'remove_failed': 1,
                               'retry_timeout': 2,
                               'dead_timeout': 30}}})
