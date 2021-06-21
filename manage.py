from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config
from web.base.routes import base
from web.users.routes import users

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(base)
app.register_blueprint(users)

db = SQLAlchemy(app)
db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
