# WARNING: DON'T TOUCH NOTHING HERE!

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
from web.users.models import User
from web.posts.models import Post
db.create_all()
db.session.commit()
bcrypt = Bcrypt(app)

from web.base.routes import base
from web.users.routes import users


app.register_blueprint(base)
app.register_blueprint(users)


if __name__ == '__main__':
    app.run(debug=True)
