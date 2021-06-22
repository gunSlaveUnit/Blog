# WARNING: DON'T TOUCH NOTHING HERE!

from flask import Flask
from flask_bcrypt import Bcrypt
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
from web.users.models import User
from web.posts.models import Post
db.create_all()
db.session.commit()
bcrypt = Bcrypt(app)
mail = Mail(app)
csrf = CSRFProtect(app)

from web.base.routes import base
from web.users.routes import users
from web.posts.routes import posts


app.register_blueprint(base)
app.register_blueprint(users)
app.register_blueprint(posts)


if __name__ == '__main__':
    app.run(debug=True)
